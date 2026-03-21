# 🚀 CDC Data Pipeline with Kafka, Debezium, and Parquet

## 📌 Project Overview

This project implements a **real-time Change Data Capture (CDC) pipeline** that captures database changes from MySQL and streams them through Kafka. The data is then processed using Python and stored in a data lake in **Parquet format** for analytics.

---

## 🏗️ Architecture

MySQL → Debezium → Kafka → Python Processor → Data Lake (Parquet)

---

## ⚙️ Technologies Used

* **MySQL** – Source database
* **Debezium** – CDC engine (captures DB changes)
* **Apache Kafka** – Streaming platform
* **Python** – Data processing (kafka-python, pandas, pyarrow)
* **Docker** – Containerized environment
* **Parquet** – Efficient columnar storage format

---

## 📂 Project Structure

```
cdc-pipeline/
│
├── docker-compose.yml
├── mysql/init/
│   ├── 01-schema.sql
│   ├── 02-data.sql
│   └── 03-users.sql
│
├── processor/
│   ├── processor.py
│   ├── parquet_writer.py
│   └── lineage_report.py
│
├── data_lake/
├── output/
└── state/
```

---

## 🚀 How to Run

### 1️⃣ Start services

```
docker-compose down -v
docker-compose up --build -d
```

---

### 2️⃣ Create Kafka Connector

```
curl -X POST http://localhost:8083/connectors \
-H "Content-Type: application/json" \
-d '{
"name": "mysql-connector",
"config": {
"connector.class": "io.debezium.connector.mysql.MySqlConnector",
"database.hostname": "mysql",
"database.port": "3306",
"database.user": "debezium_user",
"database.password": "debezium_pw",
"database.server.id": "184054",
"topic.prefix": "dbserver1",
"database.include.list": "inventory",
"table.include.list": "inventory.products",
"schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
"schema.history.internal.kafka.topic": "schema-changes.inventory"
}
}'
```

---

### 3️⃣ Insert Data

```
docker exec -it mysql mysql -u root -proot
```

```
USE inventory;

INSERT INTO products(name,description,price)
VALUES ('TEST','WORKING',1000);
```

---

### 4️⃣ Check Output

```
docker logs -f processor
```

---

## 📊 Features

* Real-time CDC pipeline
* Kafka-based streaming architecture
* Supports INSERT, UPDATE, DELETE events
* Parquet file storage (optimized for analytics)
* Partitioned data lake design
* Schema evolution support
* Lineage tracking

---

## ⚡ Output Example

```
data_lake/
  products/
    2026-03-21/
      c/
        data_123.parquet
```

---

## 🧠 Key Concepts

* Change Data Capture (CDC)
* Event-driven architecture
* Stream processing
* Data lake design

---

## 🚀 Future Improvements

* Add monitoring and alerting
* Implement batch processing
* Deploy on AWS (S3, MSK)
* Build dashboard for visualization

---
