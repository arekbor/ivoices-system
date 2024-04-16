FROM python:3.10
WORKDIR /code 
RUN mkdir /var/invoices
RUN apt-get update
RUN apt-get install wkhtmltopdf -y
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --upgrade pip
COPY . /code/app
WORKDIR /code/app
CMD ["python3", "main.py"]