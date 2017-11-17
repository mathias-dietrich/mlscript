
import time
from datetime import datetime
import pika
import json 

# http://10.0.0.5:15672/#/queues

def run():
    parameters = pika.URLParameters('amqp://pip:pip@10.0.0.5')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(callback,
                      queue='pip',
                      no_ack=True)


    channel.start_consuming()
    print ("done")


if __name__ == '__main__':
    run()