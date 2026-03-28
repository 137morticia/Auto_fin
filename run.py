import configparser
import os
import pandas as pd
from db import PGDatabase
import logging
import traceback
from datetime import datetime

LOGGER = logging.getLogger(__name__)

logging.basicConfig(filename="/home/Auto_fin/logs/db_writer.log", level=logging.DEBUG)

LOGGER.debug(f"\n\n\n\n\nLaunch script. {datetime.now()}")

data_folder_path: str = "/home/Auto_fin/data"

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


if os.path.exists(data_folder_path):
    for root, dirs, files in os.walk(data_folder_path):
        LOGGER.debug(f"root: {root}, dirs: {dirs}, files: {files}")
        for file in files:
            file_path = os.path.join(root, file)
            sales_df = pd.read_csv(file_path)
            for i, row in sales_df.iterrows():
                try:
                    LOGGER.debug(f"INSTERING into database next row: {row}")
                    query = f"insert into sales values ('{row['date']}', {row['shop']}, {row['cash']}, '{row['doc_id']}', '{row['item']}', '{row['category']}', {row['amount']}, {row['price']}, {row['discount']})"
                    database.post(query)
                    LOGGER.debug("row was insterted")
                except Exception as e:
                    LOGGER.debug(f"Insterting failed: {e}, {traceback.format_exc()}")
                    print(f"Ошибка при обработке файла {file}: {e}")
            try:
                LOGGER.debug(f"removing file_path: {file_path}")
                os.remove(file_path)
                print(f"Файл {file} был успешно удалён.")
                LOGGER.debug(f"removing was successfully done.")
            except Exception as e:
                LOGGER.debug(f"failed to remove file: {file_path}")
                print(f"Ошибка при удалении файла {file_path}: {e}")
