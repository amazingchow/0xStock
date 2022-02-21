# -*- coding: utf-8 -*-
from .mysqlcli import MySQLConnector

db_connector = MySQLConnector.instance()
db_connector.init_conn("stock_history_data")


def query_stock_data(passed_days, stock_code):
    pass
