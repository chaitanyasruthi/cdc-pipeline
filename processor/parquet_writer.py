import pandas as pd
import os
import time
from datetime import datetime

def write_parquet(data, table, op):
    date = datetime.now().strftime("%Y-%m-%d")

    folder = f"/app/data_lake/{table}/{date}/{op}/"
    os.makedirs(folder, exist_ok=True)

    df = pd.DataFrame([data])

    file_path = folder + f"data_{int(time.time())}.parquet"
    df.to_parquet(file_path, engine="pyarrow", index=False)

    return file_path