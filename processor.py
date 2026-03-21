from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'dbserver1.inventory.products',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='test-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

print("Listening for CDC events...\n")

for message in consumer:
    print("\nEVENT:\n", json.dumps(message.value, indent=2))