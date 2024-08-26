import os
import pandas as pd

DATA_DIR = "data"

def get_csv_data(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_name} not found.")
    return pd.read_csv(file_path)

def save_csv_data(file_name, data):
    file_path = os.path.join(DATA_DIR, file_name)
    data.to_csv(file_path, index=False)

def append_to_csv(file_name, row):
    data = get_csv_data(file_name)
    new_data = data.append(row, ignore_index=True)
    save_csv_data(file_name, new_data)
