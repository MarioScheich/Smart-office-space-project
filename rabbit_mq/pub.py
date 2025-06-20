import grovepi
import time
import pika

port = 4# The Sensor goes on digital port 4.
sensor = 0 # The Blue colored sensor code.
timeout = 1

credentials = pika.PlainCredentials('sciot', 'Us47*nHgD')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.3', 5672, '/', credentials))
channel = connection.channel()
channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False)

while True:
    [temperature, humidity] = grovepi.dht(port, sensor)
    message = time.ctime() + ' Temperature = ' + str(temperature) + ' C, humidity = ' + str(humidity) + ' %'
    channel.basic_publish(exchange='sciot.topic', routing_key='u38.0.353.window.temperature.12345',body=message)
    print('Sent ' + message)
    time.sleep(timeout)