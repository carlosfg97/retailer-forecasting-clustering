from confluent_kafka import Consumer, KafkaException
import sys
import getopt
import json
import logging
from pprint import pformat
import pandas as pd
from sqlalchemy import create_engine
import os

kafka_username = os.environ.get("KAFKA_USERNAME")
kafka_pw = os.environ.get("KAFKA_PASSWORD")
pg_pass = os.environ.get("PG_PASS")
engine = create_engine(
    f"postgresql://postgres:{pg_pass}@database-1.c1llvpvqgckd.us-east-1.rds.amazonaws.com:5432/postgres",
    echo=False,
)


def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    print("\nKAFKA Stats: {}\n".format(pformat(stats_json)))


def print_usage_and_exit(program_name):
    sys.stderr.write(
        "Usage: %s [options..] <bootstrap-brokers> <group> <topic1> <topic2> ..\n"
        % program_name
    )
    options = """
 Options:
  -T <intvl>   Enable client statistics at specified interval (ms)
"""
    sys.stderr.write(options)
    sys.exit(1)


def deserialize(msg: bytes):
    return json.loads(msg.decode("utf-8"))


if __name__ == "__main__":
    # optlist, argv = getopt.getopt(sys.argv[1:], 'T:')
    # if len(argv) < 3:
    #     print_usage_and_exit(sys.argv[0])

    broker = "pkc-2396y.us-east-1.aws.confluent.cloud:9092"
    group = "3"
    topics = ["favorita-sales-model"]
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {
        "bootstrap.servers": broker,
        "group.id": group,
        "session.timeout.ms": 6000,
        "auto.offset.reset": "earliest",
        "sasl.mechanism": "PLAIN",
        "security.protocol": "SASL_SSL",
        "sasl.username": kafka_username,
        "sasl.password": kafka_pw,
        "enable.auto.commit": "false",
    }

    # Create logger for consumer (logs will be emitted when poll() is called)
    logger = logging.getLogger("consumer")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
    )
    logger.addHandler(handler)

    # Create Consumer instance
    # Hint: try debug='fetch' to generate some log messages
    c = Consumer(conf, logger=logger)

    def print_assignment(consumer, partitions):
        print("Assignment:", partitions)

    # Subscribe to topics
    c.subscribe(topics, on_assign=print_assignment)

    # Read messages from Kafka, print to stdout
    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write(
                    "%% %s [%d] at offset %d with key %s:\n"
                    % (msg.topic(), msg.partition(), msg.offset(), str(msg.key()))
                )
                record = deserialize(msg.value())
                with engine.begin() as conn:
                    pd.DataFrame([record]).set_index(["store_nbr", "yearweek"]).to_sql(
                        "sales", con=conn, if_exists="append"
                    )
                    print(f"Inserted row(s)")

    except KeyboardInterrupt:
        sys.stderr.write("%% Aborted by user\n")

    finally:
        # Close down consumer to commit final offsets.
        c.close()
