# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def capture_stock_code():
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    driver.get("http://quotes.money.163.com/old#query=EQA&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0")

    page = 0
    while 1:
        html = driver.page_source
        f = open("./stock-code-src-pages/page_%03d" % (page + 1), "w")
        f.write(html)
        f.close()
        flip_page_btn = driver.find_element(By.CLASS_NAME, "pages_flip")
        if flip_page_btn.is_enabled():
            flip_page_btn.click()
            page += 1
            time.sleep(1)
        else:
            break

if __name__ == "__main__":
    capture_stock_code()
