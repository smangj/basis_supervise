# coding: utf-8
# Author: smangj
import tushare as ts
import typing
import pandas as pd

ts.set_token('9c3ae560d921c9d885e5d8a15431f3c09938e64ac2e019762ce8338c')
pro = ts.pro_api()


def index_future_basic(date: str) -> pd.DataFrame:
    """
    返回日期当天 中金所 能看到的合约信息
    """
    df = pro.fut_basic(exchange='CFFEX', fields='ts_code,d_month,list_date,delist_date')
    mask = (df['list_date'] <= date) & (df['delist_date'] >= date)
    target = df.loc[mask]
    return target


def index_price(index_name: str, date: str) -> typing.Union[float, None]:
    """
    返回股指期货合约的现货指数价格
    """
    if 'IC' in index_name:
        spot = '399905.SZ'
    elif 'IF' in index_name:
        spot = '399300.SZ'
    elif 'IH' in index_name:
        spot = '000016.SH'
    else:
        raise ValueError('未纳入考虑的指数！')

    df = pro.index_daily(ts_code=spot)
    target_data = df[df['trade_date'] == date]
    if target_data.empty:
        return None
    else:
        return target_data['close'].iloc[0]


def future_date_price(code: str, date: str) -> typing.Union[float, None]:
    """
    返回期货合约某一天的close
    """
    df = pro.fut_daily(ts_code=code, trade_date=date, fields='ts_code,trade_date,close')
    if df.empty:
        return None
    else:
        return float(df['close'].iloc[0])


if __name__ == '__main__':
    pass
