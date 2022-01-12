# -*- coding: utf-8 -*-
from .mysqlcli import MySQLConnector

db_connector = MySQLConnector.instance()
db_connector.init_conn("stock_history_data")


def load_stock_data_file(db_table, csv_file):
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
