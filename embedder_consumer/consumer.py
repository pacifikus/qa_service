import logging

import pika
import tensorflow_hub as hub
from flask import jsonify

MODEL_PATH = "models/use"
embedder = hub.load(MODEL_PATH)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def generate_embedding(text):
    return embedder([text]).numpy().tolist()


def on_request(ch, method, props, body):
    result = generate_embedding(body["text"])
    logging.info(result)
    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=jsonify(outputs=[result]),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))

channel = connection.channel()
channel.queue_declare(queue="embedding_queue")
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="embedding_queue", on_message_callback=on_request)
channel.start_consuming()
