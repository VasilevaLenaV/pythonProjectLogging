# Импорт данных в телефонный справочник
import crud as crud
import logger as log
import csv

global logger

logger = log.init(__name__)


def import_from_csv():
    logger.info(f"start import from csv")

    file = open("files\\import.csv", mode='r', encoding='utf-8-sig')

    for str_row in file:

        data_to_import = str_row.replace("\n", "").split(";")

        if data_to_import:
            if data_to_import[0] == "fullname":
                continue
            else:
                logger.info(data_to_import)
                crud.import_employee(data_to_import)

    logger.info(f"end import from file")
    file.close()
