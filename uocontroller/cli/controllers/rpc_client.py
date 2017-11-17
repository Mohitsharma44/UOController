import pika
from pika.exceptions import ConnectionClosed
import time
import uuid
import sys

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.connection.add_timeout(2, self.connection_timeout)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def connection_timeout(self):
        """
        If the connection timesout, close the connection
        Returns
        -------
        True: If connection close was successful else raises Exception
        """
        try:
            print("Could not establish connection")
            self.channel.queue_delete(queue='rpc_queue')
            self.connection.close()
            return True
        except ConnectionClosed as ex:
            pass
    
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        print('Correlation Id: ', self.corr_id)
        try:
            if self.connection.is_open:
                self.channel.basic_publish(exchange='',
                                           routing_key='rpc_queue',
                                           properties=pika.BasicProperties(
                                               reply_to=self.callback_queue,
                                               correlation_id=self.corr_id),
                                           body=str(n))
                while self.response is None:
                    self.connection.process_data_events()
                return int(self.response)
            else:
                return None
        except ConnectionClosed as cc:
            print("Connection is not Open!")
            sys.exit(1)

if __name__ == "__main__":
    start_time = time.time()
    fibonacci_rpc = FibonacciRpcClient()
    print(' [x] Requesting fib(30)')
    for i in range(20, 30):
        response = fibonacci_rpc.call(i)
        print(' [.] Got %r' %response)
    print(' [x] Done.')
    print("--- %s seconds ---" % (time.time() - start_time))
