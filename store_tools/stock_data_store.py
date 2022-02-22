# -*- coding: utf-8 -*-
import argparse
import glob
import os
import pathlib
import sys
import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from store_tools import MySQLConnector

db_connector = MySQLConnector.instance()
db_connector.init_conn("stock_history_data")


def load_stock_data_file(db_table: str, csv_file: str):
    db_connector.load_data_infile(
        """LOAD DATA LOCAL INFILE "{}" """.format(csv_file) +
        "INTO TABLE stock_history_data.{} ".format(db_table) +
        "FIELDS TERMINATED BY ',' " +
        """ENCLOSED BY '"' """ +
        "LINES TERMINATED BY '\n' " +
        "IGNORE 1 LINES " +
        "(capture_date, stock_code, stock_name, " +
        "t_close_price, t_hi_price, t_lo_price, t_open_price, t_minus_one_close_price, " +
        "chg, pchg, voturnover, vaturnover);"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", type=str, help="list of stock-data csv files")
    args = parser.parse_args()
    stock_data_dir = args.data
    for csv_file in tqdm.tqdm(glob.glob("{}/*.csv".format(stock_data_dir))):
        load_stock_data_file("stock_code_prefix_{}".format(pathlib.Path(csv_file).stem[:3]), csv_file)
