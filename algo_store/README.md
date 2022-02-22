算法仓库存放各种自研股票粗搜算法

各个股票粗搜算法实现需要满足如下标准接口


```python
def algo_xxx(stock_code: str, stock_data: list) -> (str, bool):
    '''
    @输入参数:
        stock_code: 股票代码, 股票唯一标识
        stock_data: 股票历史数据, XXXX年XX月XX日 ~ YYYY年YY月YY日的历史数据, 每天一条
    @输出参数:
        stock_code: 股票代码, 股票唯一标识
        should_be_recommended: 是否需要被推荐, 满足算法筛选条件为True, 否则为False
    '''
    should_be_recommended = False
    
    # TOOD

    return stock_code, should_be_recommended
```
