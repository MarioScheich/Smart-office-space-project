import pika
import os
from dotenv import load_dotenv

load_dotenv()

# Load RabbitMQ configuration from .env
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
EXCHANGE_NAME = "sciot.topic"

def callback(ch, method, properties, body):
    print(f"Received [{method.routing_key}]: {body.decode()}")

def start_subscriber(binding_keys=None):
    if binding_keys is None:
        binding_keys = ["#"]  # Default: receive all topics

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST, 5672, '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True, auto_delete=False)
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    for key in binding_keys:
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=key)

    print(f"Waiting for messages on exchange '{EXCHANGE_NAME}' with keys: {binding_keys}. Press Ctrl+C to exit.")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    # Subscribe to all topics by default, or modify to filter specific routing keys
    start_subscriber(binding_keys=[
        "sensor.dht.environment",
        "sensor.weatherbit.environment",
        "sensor.openmeteo.co2",
        "google.calendar.events"
    ])
