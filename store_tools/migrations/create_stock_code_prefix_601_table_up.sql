CREATE TABLE IF NOT EXISTS stock_history_data.stock_code_prefix_601 (
    id                      INT      NOT NULL AUTO_INCREMENT,
    capture_date            CHAR(10) NOT NULL, /* 抓取日期 */
    stock_code              CHAR(6)  NOT NULL, /* 股票代码 */
    stock_name              CHAR(26) NOT NULL, /* 股票名称 */
    t_close_price           FLOAT    NOT NULL, /* 收盘价 */
    t_hi_price              FLOAT    NOT NULL, /* 最高价 */
    t_lo_price              FLOAT    NOT NULL, /* 最低价 */
    t_open_price            FLOAT    NOT NULL, /* 开盘价 */
    t_minus_one_close_price FLOAT    NOT NULL, /* 前收盘价 */
    chg                     FLOAT    NOT NULL, /* 涨跌额 */
    pchg                    FLOAT    NOT NULL, /* 涨跌幅 */
    voturnover              FLOAT    NOT NULL, /* 成交量 */
    vaturnover              FLOAT    NOT NULL, /* 成交金额 */
    PRIMARY KEY (id),
    KEY (capture_date, stock_code)
) ENGINE=InnoDB;
