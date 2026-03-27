import configparser
import os
import pandas as pd
from db import PGDatabase

config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
config.read(os.path.join(dirname, "config.ini"))

DATABASE_CREDS = config["Database"]

database = PGDatabase(
    host=DATABASE_CREDS["HOST"],
    database=DATABASE_CREDS["DATABASE"],
    user=DATABASE_CREDS["USER"],
    password=DATABASE_CREDS["PASSWORD"],
)

sales_df = pd.DataFrame()
if os.path.exists('data'):
    for root, dirs, files in os.walk('data'):
        for file in files:
            file_path = os.path.join(root, file)
            sales_df = pd.read_csv(file_path)
            for i, row in sales_df.iterrows():
                try:
                    query = f"insert into sales values ('{row['date']}', {row['shop']}, {row['cash']}, '{row['doc_id']}', '{row['item']}', '{row['category']}', {row['amount']}, {row['price']}, {row['discount']})"
                    database.post(query)
                except Exception as e:
                    print(f"Ошибка при обработке файла {file}: {e}")
            try:
                os.remove(file_path)
                print(f"Файл {file} был успешно удалён.")
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")
