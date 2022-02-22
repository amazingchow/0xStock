# -*- coding: utf-8 -*-
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from store_tools import MySQLConnector

db_connector = MySQLConnector.instance()
db_connector.init_conn("stock_history_data")


def query_stock_data(passed_days: int, stock_code: str):
    # TODO: "http://quotes.money.163.com/service/chddata.html?code={}{}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER" 为什么只返回2021-12-31之前的数据了？
    # stmt = "SELECT * FROM stock_code_prefix_{} WHERE stock_code = '{}' AND capture_date >= '{}' AND capture_date < '{}';".format(
    #     stock_code[:3], stock_code,
    #     (datetime.datetime.today() - datetime.timedelta(days=passed_days)).strftime("%Y-%m-%d"),
    #     datetime.datetime.today().strftime("%Y-%m-%d"),
    # )
    stmt = "SELECT * FROM stock_code_prefix_{} WHERE stock_code = '{}' LIMIT {};".format(
        stock_code[:3], stock_code, passed_days
    )

    needed_ret = []
    ret = db_connector.query(stmt)
    for x in ret:
        needed_ret.append(
            {
                "capture_date": x[1],            # 抓取日期
                "stock_code": x[2],              # 股票代码
                "stock_name": x[3],              # 股票名称
                "t_close_price": x[4],           # 收盘价
                "t_hi_price": x[5],              # 最高价
                "t_lo_price": x[6],              # 最低价
                "t_open_price": x[7],            # 开盘价
                "t_minus_one_close_price": x[8], # 前收盘价
                "chg": x[9],                     # 涨跌额
                "pchg": x[10],                   # 涨跌幅
                "voturnover": x[11],             # 成交量
                "vaturnover": x[2],              # 成交金额
            }
        )
    return needed_ret
