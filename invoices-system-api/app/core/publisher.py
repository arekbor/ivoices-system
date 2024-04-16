import pika
from app.core.settings import get_settings 

class Publisher:
    def __init__(self) -> None:
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
            queue=settings.RABBITMQ_ORDER_CREATED_QUEUE_NAME
        )
        self._channel.queue_bind(
            queue=settings.RABBITMQ_ORDER_CREATED_QUEUE_NAME,
            exchange=settings.RABBITMQ_ORDER_EXCHANGE_NAME,
            routing_key=settings.RABBITMQ_ORDER_CREATED_QUEUE_ROUTING_KEY
        )

    def publish_created_order(self, serialized_object: str) -> None:
        settings = get_settings()
        self._channel.basic_publish(
            exchange=settings.RABBITMQ_ORDER_EXCHANGE_NAME,
            routing_key=settings.RABBITMQ_ORDER_CREATED_QUEUE_ROUTING_KEY,
            body=serialized_object
        )

    def close(self) -> None:
        self._connection.close()