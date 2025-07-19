import pika
import os
import json
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
EXCHANGE_NAME = "sciot.topic"

def publish_message(routing_key: str, message):
    """
    Publish message to RabbitMQ topic exchange.
    Safely opens/closes connection per call.
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBITMQ_HOST, 5672, '/', credentials)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

    if isinstance(message, dict):
        message = json.dumps(message)
    elif not isinstance(message, str):
        raise TypeError("Message must be a dict or str")

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=message.encode("utf-8")
    )
    print(" Sent:", message)

    connection.close()
