from functools import lru_cache
import threading
import pika 
from pydantic_settings import BaseSettings, SettingsConfigDict
import jinja2
import pdfkit
import json
import os

class Settings(BaseSettings):
    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    RABBITMQ_ORDER_EXCHANGE_NAME: str
    RABBITMQ_ORDER_EXCHANGE_TYPE: str
    RABBITMQ_ORDER_CREATED_QUEUE_NAME: str
    RABBITMQ_ORDER_CREATED_QUEUE_ROUTING_KEY: str

    RAPORT_DIR_LOCATION: str

    model_config = SettingsConfigDict(env_file='.env')

@lru_cache
def get_settings():
    return Settings()

class Consumer(threading.Thread):
    def __init__(self, *args, **kwargs) -> None:
        super(Consumer, self).__init__(*args, **kwargs)
        
    def run(self) -> None:
        print("Start consuming messages...")
        settings = get_settings()
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD
        )
        connection_parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials
        )
        self._connection = pika.BlockingConnection(connection_parameters)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=settings.RABBITMQ_ORDER_EXCHANGE_NAME,
            exchange_type=settings.RABBITMQ_ORDER_EXCHANGE_TYPE
        )
        self._channel.queue_declare(
            queue=settings.RABBITMQ_ORDER_CREATED_QUEUE_NAME,
        )
        self._channel.queue_bind(
            queue=settings.RABBITMQ_ORDER_CREATED_QUEUE_NAME,
            exchange=settings.RABBITMQ_ORDER_EXCHANGE_NAME,
            routing_key=settings.RABBITMQ_ORDER_CREATED_QUEUE_ROUTING_KEY
        )
        self._channel.basic_consume(
            queue=settings.RABBITMQ_ORDER_CREATED_QUEUE_NAME,
            on_message_callback=self.callback,
        )
        self._channel.start_consuming()

    def callback(self, channel, method, properties, body) -> None:
        print("{} received '{}'".format(self.name, body))
        try:
            decoded_json = json.loads(body)
            invoice_id = decoded_json.get('id', '')
            context = {
                'id': invoice_id,
                'user_id': decoded_json.get('user_id', ''),
                'name': decoded_json.get('name', ''),
                'email': decoded_json.get('email', ''),
                'address': decoded_json.get('address', ''),
                'order_items': decoded_json.get('order_items', ''),
                'total_due': decoded_json.get('total_due', ''),
                'date': decoded_json.get('created_at', '')
            }
            template_loader = jinja2.FileSystemLoader("./")
            template_environment = jinja2.Environment(loader=template_loader)
            template = template_environment.get_template("pdf-template.html")
            output_text = template.render(context)
            config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

            settings = get_settings()
            path_to_save = os.path.join(settings.RAPORT_DIR_LOCATION, f'invoice_{invoice_id}.pdf')
            pdfkit.from_string(output_text, path_to_save, configuration=config)
        except Exception as e:
            print("Something went wrong while generating a pdf: ", e)
            return 
        channel.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    Consumer().start()