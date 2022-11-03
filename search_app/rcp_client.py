import json
import uuid

import pika


class RpcClient:
    def __init__(self, host, queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue=queue)
        self.queue = queue
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, data):
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                expiration="300000",
            ),
            body=json.dumps({"text": data}),
        )
        while self.response is None:
            self.connection.process_data_events()
        return self.response
