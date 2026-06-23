from kafka import KafkaConsumer
import json
from datetime import datetime
from parquet_writer import write_parquet
from schema_store import init_db, register_schema

init_db()

consumer = KafkaConsumer(
    "dbserver1.inventory.products",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
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

    table_name = "products"

    schema_definition = {
        k: str(type(v).__name__)
        for k, v in data.items()
    }

    schema_version = register_schema(
        table_name,
        schema_definition
    )

    data["schema_version"] = schema_version
    data["event_timestamp"] = datetime.utcnow().isoformat()
    data["op_type"] = op

    file_path = write_parquet(
        data,
        table_name,
        op
    )

    lineage_record = {
        "source_table": table_name,
        "schema_version": schema_version,
        "active_from": datetime.utcnow().isoformat(),
        "output_partitions": [
            f"/data_lake/{table_name}/{datetime.now().strftime('%Y-%m-%d')}/{op}/"
        ],
        "output_schema": schema_definition
    }

    try:
        with open(
            "/app/output/lineage_report.json",
            "a"
        ) as f:
            f.write(json.dumps(lineage_record))
            f.write("\n")
    except Exception as e:
        print("Lineage error:", e)

    print(
        f"Saved {file_path} | schema_version={schema_version}"
    )