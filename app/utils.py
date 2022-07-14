# coding: utf-8
# Author: smangj
import typing
import datetime as dt
import pandas as pd


def to_pydatetime(src_dt: typing.Union[dt.datetime, str, pd.Timestamp, dt.date, None]) -> typing.Optional[dt.datetime]:
    dst_dt = None if src_dt is None else pd.to_datetime(src_dt).to_pydatetime()
    return dst_dt


if __name__ == '__main__':
    pass
