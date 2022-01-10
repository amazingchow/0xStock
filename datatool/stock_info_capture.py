# -*- coding: utf-8 -*-
import time
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def capture_stock_info():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=options)
    driver.get("http://quotes.money.163.com/old#query=EQA&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0")

    f = open("./stock_info/stock_info.txt", "w")

    page = 1
    while 1:
        try:
            time.sleep(3)
            stock_info_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "stocks-info-table"))
            )
            stock_info_tbody = WebDriverWait(stock_info_table, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "tbody"))
            )
            stock_info_trs = WebDriverWait(stock_info_tbody, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
            )
            for tr in stock_info_trs:
                stock_info_tds = WebDriverWait(tr, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                )
                f.write("{}, {}\n".format(
                    stock_info_tds[1].text,
                    stock_info_tds[2].text,
                ))
                f.flush()

            next_page_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "下一页"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_page_btn)
            driver.execute_script("arguments[0].click();", next_page_btn)
            page += 1
            print("next page: %d" % page)
        except Exception as e:
            print(e)
            break

    driver.close()
    f.close()


def classify_stock_info():
    f = open("./stock_info/stock_info.txt", "r")
    stock_info_classify_table = defaultdict(list)
    for line in f:
        parts = line.split(", ")
        stock_code, stock_name = parts[0].strip(), parts[1].strip()
        stock_info_classify_table[stock_code[:3]].append((stock_code, stock_name))
    f.close()

    hu_shi_a_stock = ["600", "601", "603", "605"]
    f_hu_shi_a_stock = open("./stock_info/hu_shi_a_stock_info.txt", "w")
    shen_shi_a_stock = ["000"]
    f_shen_shi_a_stock = open("./stock_info/shen_shi_a_stock_info.txt", "w")
    for k, v in stock_info_classify_table.items():
        for vv in v:
            if k in hu_shi_a_stock:
                f_hu_shi_a_stock.write("{}, {}\n".format(vv[0], vv[1]))
                f_hu_shi_a_stock.flush()
            if k in shen_shi_a_stock:
                f_shen_shi_a_stock.write("{}, {}\n".format(vv[0], vv[1]))
                f_shen_shi_a_stock.flush()
    f_hu_shi_a_stock.close()
    f_shen_shi_a_stock.close()


if __name__ == "__main__":
    capture_stock_info()
    classify_stock_info()
