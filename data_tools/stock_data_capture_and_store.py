# -*- coding: utf-8 -*-
import csv
import datetime
import glob
import logging
import os
import requests
import shutil
import sys
import tqdm

from ratelimit import limits, RateLimitException, sleep_and_retry

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from store_tools import load_stock_data_file

__Logger = logging.getLogger("stock_data_capture")
__Logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler("{}/0xStock-logs/stock_data_capture.log".format(os.path.expanduser("~")), "w")
__FileHandler.setFormatter(__Formatter)
__Logger.addHandler(__FileHandler)


@sleep_and_retry
@limits(calls=90, period=270)
def http_request(session, flag, stock_code, stock_name, date):
    url = "http://quotes.money.163.com/service/chddata.html?code={}{}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER".format(
        flag, stock_code, date.strftime("%Y-%m-%d"))
    response = session.get(url=url)

    __Logger.info("fetch stock data on <{}>".format(response.url))
    if response.status_code == 200:
        __Logger.info("response status code: {}".format(response.status_code))
    elif response.status_code == 429:
        raise RateLimitException("api response: 429", 5)
    else:
        __Logger.warning("failed to fetch, response status code: {}".format(response.status_code))
        return

    if response.text == "":
        return

    response.encoding = "gbk"
    f = open("{}/0xStock-data/history-data/{}_{}.csv".format(os.path.expanduser("~"), stock_code, stock_name), "w")
    f.write(response.text)
    f.close()


'''
抓取沪/深A股股票数据（全量数据）
'''
def capture_stock_data():
    with requests.Session() as session:
        stock_list = []
        f = open("./stock_code/hu_shi_a_stock_code.txt", "r")
        for line in f:
            parts = line.split(", ")
            stock_code, stock_name = parts[0].strip(), parts[1].strip()
            stock_list.append((0, stock_code, stock_name))
        f.close()
        f = open("./stock_code/shen_shi_a_stock_code.txt", "r")
        for line in f:
            parts = line.split(", ")
            stock_code, stock_name = parts[0].strip(), parts[1].strip()
            stock_list.append((1, stock_code, stock_name))
        f.close()

        for stock in tqdm.tqdm(stock_list):
            http_request(session, stock[0], stock[1], stock[2], datetime.date.today())


'''
存储沪/深A股股票数据（全量数据）
'''
def store_stock_data():
    csvfiles = glob.glob("{}/0xStock-data/history-data/*.csv".format(os.path.expanduser("~")))
    for csvfile in tqdm.tqdm(csvfiles):
        stock_code = ""

        fw = open(csvfile + ".tmp", "w", encoding="utf-8-sig")
        csv_writer = csv.writer(fw, delimiter=",")
        with open(csvfile, "r", encoding="utf-8-sig") as fd:
            csv_reader = csv.reader(fd, delimiter=",")
            line = 0
            for row in csv_reader:
                if line > 0:
                    stock_code = row[1][1:]
                    row[1] = stock_code
                csv_writer.writerow(row)
                line += 1
        fw.close()
        shutil.move(csvfile + ".tmp", csvfile)

        load_stock_data_file("stock_code_prefix_{}".format(stock_code[0:3]), csvfile)


if __name__ == "__main__":
    capture_stock_data()
    store_stock_data()
