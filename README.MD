# World Happiness ETL & Streaming Analytics Pipeline
# Juan Pablo COll
## Project Description

This project implements a complete Data Engineering and Analytics pipeline using the World Happiness Report datasets from 2015 to 2019.

The system extracts, cleans, transforms, streams, stores, and analyzes happiness data from multiple CSV files using modern data engineering tools and concepts such as ETL pipelines, Apache Kafka, PostgreSQL, Docker, Machine Learning, and Power BI dashboards.

Additionally, a simple Machine Learning regression model was trained to predict the Happiness Score based on socioeconomic indicators such as GDP, health, family support, freedom, trust, and generosity.

The main objective of the project is to demonstrate the integration of multiple technologies into a unified end-to-end data pipeline.

---

# Architecture Explanation

The project follows a streaming-based architecture:

```text
Raw CSV Files
       ->
ETL Cleaning & Preprocessing
       ->
Unified Dataset
       ->
Kafka Producer
       ->
Apache Kafka Topic
       ->
Kafka Consumer
       ->
Machine Learning Prediction
       ->
PostgreSQL Storage
       ->
Power BI Dashboard
```

## Components

### ETL Layer
Responsible for:
- extracting raw CSV datasets,
- cleaning inconsistent columns,
- standardizing data,
- generating a unified dataset.

### Kafka Producer
Reads records from the processed dataset and sends them as streaming events to a Kafka topic.

### Kafka Consumer
Consumes messages from Kafka, preprocesses the incoming data, generates predictions using the ML model, and stores the results into PostgreSQL.

### PostgreSQL Database
Stores the final streamed records and analytical views (KPIs).

### Power BI Dashboard
Visualizes KPIs, correlations, trends, and country-level analytics.

---

# Data Cleaning Decisions

Several preprocessing decisions were required because the datasets from different years had inconsistent schemas.

## Removed Columns

The following columns were removed because they were either incompatible across datasets or not necessary for the analysis:

- Region
- Standard Error
- Lower Confidence Interval
- Upper Confidence Interval
- Whisker.high
- Whisker.low
- Dystopia Residual
- Dystopia.Residual

## Column Standardization

Different datasets used different naming conventions for similar variables. The datasets were standardized to ensure compatibility during concatenation.

## Missing Values

Missing numerical values were handled using:

```python
df.fillna(0)
```

This was necessary to avoid errors during Machine Learning prediction and streaming operations.

---

# Feature Engineering Decisions

## Target Variable

The target variable selected for prediction was:

```text
Happiness_score
```

## Selected Features

The following features were selected because they are strongly related to happiness according to the World Happiness methodology:

- Economy (GDP per Capita)
- Family
- Health (Life Expectancy)
- Freedom
- Trust (Government Corruption)
- Generosity

## Feature Scaling

Feature normalization was performed using:

```python
StandardScaler()
```

This ensures numerical stability and improves model consistency.

## Avoiding Target Leakage

The target variable (`Happiness_score`) was excluded from the feature matrix during training to prevent target leakage.

## Machine Learning Model

A simple Linear Regression model was used:

```python
LinearRegression()
```

The focus of the project was pipeline integration rather than model optimization.

---

# Kafka Pipeline Explanation

The Kafka pipeline simulates real-time streaming analytics.

## Producer Workflow

The producer:
1. reads the processed CSV dataset,
2. converts each row into JSON format,
3. sends each message to the Kafka topic:

```text
happiness_topic
```

## Consumer Workflow

The consumer:
1. listens to the Kafka topic,
2. receives streaming messages,
3. preprocesses the incoming data,
4. scales the features using the trained scaler,
5. generates happiness predictions using the ML model,
6. inserts the results into PostgreSQL.

This architecture demonstrates real-time streaming ingestion and analytics.

---

# Database Schema

## Main Table

```sql
CREATE TABLE happiness_predictions (
    Country TEXT,
    Year INT,
    Happiness_score FLOAT,
    GDP FLOAT,
    Family FLOAT,
    Health FLOAT,
    Freedom FLOAT,
    Trust FLOAT,
    Generosity FLOAT,
    Predicted_score FLOAT
);
```

## Analytical SQL Views (KPIs)

Several SQL views were created for analytical purposes:

- kpi_top10_happiest
- kpi_biggest_movers
- kpi_factor_correlation
- kpi_country_volatility
- kpi_global_trend

These views are directly consumed by Power BI.

---

# Dashboard Explanation

The Power BI dashboard was connected directly to PostgreSQL.

## Main Visualizations

### Top 10 Happiest Countries
Displays the countries with the highest average happiness scores.

### Global Happiness Trend
Shows how happiness evolved globally between 2015 and 2019.

### GDP vs Happiness Correlation
Scatter plot showing the relationship between economic prosperity and happiness.

### Country Volatility
Identifies countries with the most unstable happiness scores across years.

### Biggest Movers
Shows countries with the greatest improvement or decline in happiness.

### Correlation Analysis
Displays the correlation between happiness and different socioeconomic factors.

---

# Execution Instructions

## 1. Start Docker Containers

Navigate to the docker directory:

```bash
cd docker
```

Run:

```bash
docker compose up -d
```

---

# 2. Verify Containers

```bash
docker ps
```

The following containers should be running:

- zookeeper
- kafka
- postgres

---

# 3. Run Kafka Consumer

Navigate to:

```bash
cd src/kafka
```

Run:

```bash
python consumer.py
```

---

# 4. Run Kafka Producer

Open another terminal and run:

```bash
python producer.py
```

---

# 5. Connect Power BI

Connect Power BI to PostgreSQL using:

```text
Server: localhost:5432
Database: happiness_db
```

Authentication credentials:

```text
User: admin
Password: admin
```

---

# Technologies Used

- Python
- Pandas
- Scikit-learn
- Apache Kafka
- PostgreSQL
- Docker
- Power BI
- SQL

---

# Project Structure

```text
project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── streaming/
│
├── notebooks/
│   ├── eda.ipynb
│   └── model_training.ipynb
│
├── kafka/
│   ├── producer.py
│
├── models/
│   └── model.pkl
│
├── sql/
│   ├── create_tables.sql
│   └── kpis.sql
│
├── dashboards/
│
├── docker-compose.yml
│
├── requirements.txt
│
└── README.md


---

# Project Startup Guide

## 1. Clone or Download the Project

Place the project folder in your local machine.

Example:

```bash
World-Happiness/
```

---

## 2. Install Python Dependencies

Install all required libraries:

```bash
pip install pandas numpy scikit-learn kafka-python psycopg2-binary sqlalchemy joblib jupyter matplotlib seaborn
```

---

## 3. Verify Docker Installation

Check Docker installation:

```bash
docker --version
docker compose version
```

Also ensure Docker Desktop is running before starting the containers.

---

## 4. Start Infrastructure Containers

Navigate to the docker directory:

```bash
cd docker
```

Run:

```bash
docker compose up -d
```

---

## 5. Verify Running Containers

```bash
docker ps
```

The following services should be active:

- PostgreSQL
- Kafka
- Zookeeper

---

## 6. Create Kafka Topic

Enter Kafka container:

```bash
docker exec -it kafka bash
```

Create topic:

```bash
kafka-topics \
--create \
--topic happiness_topic \
--bootstrap-server localhost:9092 \
--partitions 1 \
--replication-factor 1
```

Verify topic:

```bash
kafka-topics \
--list \
--bootstrap-server localhost:9092
```

---

## 7. Run Kafka Consumer

Open a terminal:

```bash
cd src/kafka
python consumer.py
```

Expected output:

```text
Consumer listening...
```

---

## 8. Run Kafka Producer

Open another terminal:

```bash
cd src/kafka
python producer.py
```

Expected output:

```text
All messages sent.
```

---

## 9. Connect Power BI

Connect PostgreSQL using:

```text
Server: localhost:5432
Database: happiness_db
```

Credentials:

```text
User: admin
Password: admin123
```

---

# Required Libraries

## Data Processing
- pandas
- numpy

## Machine Learning
- scikit-learn
- joblib

## Streaming
- kafka-python

## Database
- psycopg2-binary
- sqlalchemy

## Visualization & Analysis
- matplotlib
- seaborn
- Power BI

## Environment & Infrastructure
- Docker
- Docker Compose
- PostgreSQL
- Apache Kafka
- Zookeeper

---

# Suggested requirements.txt

```text
pandas
numpy
scikit-learn
kafka-python
psycopg2-binary
sqlalchemy
joblib
jupyter
matplotlib
seaborn
```
