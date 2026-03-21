import json

report = [{
"source_table": "inventory.products",
"schema_version": 1,
"output_partitions": [
"/data_lake/products/2026-03-16/c/"
]
}]

with open("../output/lineage_report.json","w") as f:
    json.dump(report,f,indent=2)