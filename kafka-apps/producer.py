from threading import local
from kafka import KafkaProducer
import json
import pandas as pd
import os

kafka_username = os.environ.get("KAFKA_USERNAME")
kafka_pw = os.environ.get("KAFKA_PASSWORD")
server = "pkc-2396y.us-east-1.aws.confluent.cloud:9092"
topic = "favorita-daily-sales"
import time

from confluent_kafka import Producer, Consumer, KafkaError, KafkaException


def error_cb(err):
    """ The error callback is used for generic client errors. These
        errors are generally to be considered informational as the client will
        automatically try to recover from all errors, and no extra action
        is typically required by the application.
        For this example however, we terminate the application if the client
        is unable to connect to any broker (_ALL_BROKERS_DOWN) and on
        authentication errors (_AUTHENTICATION). """

    print("Client error: {}".format(err))
    if (
        err.code() == KafkaError._ALL_BROKERS_DOWN
        or err.code() == KafkaError._AUTHENTICATION
    ):
        # Any exception raised from this callback will be re-raised from the
        # triggering flush() or poll() call.
        raise KafkaException(err)


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))


def main():
    p = Producer(
        {
            "bootstrap.servers": server,
            "sasl.mechanism": "PLAIN",
            "security.protocol": "SASL_SSL",
            "sasl.username": kafka_username,
            "sasl.password": kafka_pw,
            "error_cb": error_cb,
        }
    )
    # s3_uri = "s3://favorita-8d838/train_2015-06-01_onwards.csv"
    local_uri = (
        "/Users/sg/projects/EDS-I-Group-Project/data/train_2015-06-01_onwards.csv"
    )
    df = pd.read_csv(local_uri).sort_values(by="date")
    for record in df.to_dict(orient="records"):
        print(json.dumps(record))
        # Trigger any available delivery report callbacks from previous produce() calls
        p.poll(0)

        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        p.produce(topic, json.dumps(record), callback=delivery_report)

        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        p.flush()

        time.sleep(1)


if __name__ == "__main__":
    main()
