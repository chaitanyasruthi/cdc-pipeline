from kafka import KafkaConsumer
import json
import pandas as pd
import os
import time
from datetime import datetime

consumer = KafkaConsumer(
    'dbserver1.inventory.products',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening for CDC events...")

for message in consumer:
    event = message.value
    payload = event.get("payload")

    if not payload:
        continue

    op = payload.get("op")

    if op in ["c", "u", "r"]:
        data = payload.get("after")
    elif op == "d":
        data = payload.get("before")
    else:
        continue

    if not data:
        continue

    # add metadata
    data["op"] = op
    date = datetime.now().strftime("%Y-%m-%d")

    df = pd.DataFrame([data])

    # partitioned folder
    folder = f"/app/data_lake/products/{date}/{op}/"
    os.makedirs(folder, exist_ok=True)

    file_path = folder + f"data_{int(time.time())}.parquet"

    df.to_parquet(file_path, engine="pyarrow", index=False)

    print("Saved Parquet:", file_path)
    lineage = {
    "source": "inventory.products",
    "operation": op,
    "timestamp": str(datetime.now())
}

with open("/app/data_lake/lineage.json", "a") as f:
    f.write(json.dumps(lineage) + "\n")