import pika
import json

queue_name = "uoir_queue"
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue_name)

def on_request(ch, method, props, body):
    data = json.loads(body)
    print("Correlation id: ", props.correlation_id)
    print("Received: ", data)
    response = "Recevied!"
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=queue_name)

print(' [x] Awaiting RPC requests')
channel.start_consuming()
