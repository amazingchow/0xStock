# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algo_store import algo_nothing
from store_tools import query_stock_data


class TestAlgo(unittest.TestCase):
    def setUp(self):
        # 所有股票代码在 ./data_tools/stock_code/hu_shi_a_stock_code.txt, shen_shi_a_stock_code.txt
        self.stock_data = query_stock_data(passed_days=30, stock_code="600300")

    def test_algo_nothing(self):
        _, should_be_recommended = algo_nothing("600300", self.stock_data)
        self.assertEqual(should_be_recommended, True, "算法输出不符合预期")
    
    def tearDown(self):
        pass


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestAlgo("test_algo_nothing"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
