# -*- coding: utf-8 -*-
import datetime
import logging
__Logger = logging.getLogger('stock_data_capture')
__Logger.setLevel(logging.INFO)
__Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
__FileHandler = logging.FileHandler('logs/stock_data_capture.log', 'w')
__FileHandler.setFormatter(__Formatter)
__Logger.addHandler(__FileHandler)
import requests
import tqdm
from ratelimit import limits, RateLimitException, sleep_and_retry


@sleep_and_retry
@limits(calls=90, period=270)
def http_request(session, flag, stock_code, stock_name, date):
    url = "http://quotes.money.163.com/service/chddata.html?code={}{}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER".format(
        flag, stock_code, date.strftime("%Y-%m-%d"))
    response = session.get(url=url)

    __Logger.info('fetch stock data on <{}>'.format(response.url))
    if response.status_code == 200:
        __Logger.info('response status code: {}'.format(response.status_code))
    elif response.status_code == 429:
        raise RateLimitException("api response: 429", 5)
    else:
        __Logger.warning('failed to fetch, response status code: {}'.format(response.status_code))
        return

    if response.text == "":
        return

    response.encoding = "gbk"
    f = open("./stock_data/{}_{}.csv".format(stock_code, stock_name), "w")
    f.write(response.text)
    f.close()


def capture_stock_data():
    with requests.Session() as session:
        stock_list = []
        f = open("./stock_info/hu_shi_a_stock_info.txt", "r")
        for line in f:
            parts = line.split(", ")
            stock_code, stock_name = parts[0].strip(), parts[1].strip()
            stock_list.append((0, stock_code, stock_name))
        f.close()
        f = open("./stock_info/shen_shi_a_stock_info.txt", "r")
        for line in f:
            parts = line.split(", ")
            stock_code, stock_name = parts[0].strip(), parts[1].strip()
            stock_list.append((1, stock_code, stock_name))
        f.close()

        for stock in tqdm.tqdm(stock_list):
            http_request(session, stock[0], stock[1], stock[2], datetime.date.today())


if __name__ == "__main__":
    capture_stock_data()
