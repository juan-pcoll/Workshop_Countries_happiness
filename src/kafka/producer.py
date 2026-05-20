import json
import time

import pandas as pd

from kafka import KafkaProducer


# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',

    value_serializer=lambda v:
        json.dumps(v).encode('utf-8')
)


# Read dataset
df = pd.read_csv(
    '../../data/processed/happiness_unified.csv'
)

df = pd.read_csv(
    '../../data/processed/happiness_unified.csv'
)

df = df.fillna(0)


# Kafka topic
TOPIC = 'happiness_topic'


print("Starting producer...\n")


# Send rows one by one
for _, row in df.iterrows():

    message = row.to_dict()

    producer.send(
        TOPIC,
        value=message
    )

    print(f"Sent: {message}")

    # Simulate streaming
    time.sleep(1)


producer.flush()

print("\nAll messages sent.")