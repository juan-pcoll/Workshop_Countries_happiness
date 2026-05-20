import json

import joblib
import pandas as pd

from kafka import KafkaConsumer

from sqlalchemy import create_engine


# Load model and scaler
model = joblib.load(
    '../../models/model.pkl'
)

scaler = joblib.load(
    '../../models/scaler.pkl'
)


# PostgreSQL connection
engine = create_engine(
    'postgresql://admin:admin@localhost:5432/happiness_db'
)


# Kafka consumer
consumer = KafkaConsumer(
    'happiness_topic',

    bootstrap_servers='localhost:9092',

    auto_offset_reset='earliest',

    value_deserializer=lambda x:
        json.loads(x.decode('utf-8'))
)


FEATURES = [
    "Economy_(GDP_per_Capita)",
    "Family",
    "Health_(Life_Expectancy)",
    "Freedom",
    "Trust_(Government_Corruption)",
    "Generosity"
]


print("Consumer listening...\n")


for message in consumer:

    data = message.value

    print(f"Received: {data}")


    # Convert to dataframe
    df = pd.DataFrame([data])


    # Select features
    X = df[FEATURES]

    X = X.fillna(0)
    
    # Scale
    X_scaled = scaler.transform(X)


    # Prediction
    prediction = model.predict(X_scaled)[0]


    # Add prediction
    data['predicted_happiness_score'] = float(prediction)


    print(f"Prediction: {prediction}")


    # Save to PostgreSQL
    pd.DataFrame([data]).to_sql(
        'happiness_predictions',

        engine,

        if_exists='append',

        index=False
    )


    print("Saved to PostgreSQL\n")