# coding: utf-8
# Author: smangj
import typing
import datetime as dt
import pandas as pd
import os


def to_pydatetime(src_dt: typing.Union[dt.datetime, str, pd.Timestamp, dt.date, None]) -> typing.Optional[dt.datetime]:
    dst_dt = None if src_dt is None else pd.to_datetime(src_dt).to_pydatetime()
    return dst_dt


def check_and_mkdirs(dir_path):
    if dir_path is None:
        return

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


if __name__ == '__main__':
    pass
