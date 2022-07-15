# coding: utf-8
# Author: smangj
from chinese_calendar import is_holiday
import datetime as dt
import typing
import pandas as pd

NUM_WORKDAYS_PER_YEAR = 252


def get_num_workdays(from_dt: dt.date, to_dt: dt.date) -> int:
    """
    根据中国的节假日计算两个日期之间的工作日（周末调休不算）
    使用这个函数来计算衍生品到期日的长度时意味着from_dt的00：00到to_dt的24：00
    """
    return len(workdays_between(from_dt, to_dt))


def workdays_between(from_dt: dt.date, to_dt: dt.date) -> typing.List[dt.date]:
    """
    根据中国的节假日返回两个日期之间的所有工作日（周末调休不算））
    使用这个函数来计算衍生品到期日的长度时意味着from_dt的00：00到to_dt的24：00
    当两个日期之间没有工作日时返回空列表
    """
    date_l = [
        dt.datetime.strftime(date_time, "%Y-%m-%d") for date_time in list(pd.date_range(start=from_dt, end=to_dt))
    ]
    weekdays = list()
    for date_str in date_l:
        date = dt.datetime.strptime(date_str, "%Y-%m-%d")
        flag_weekday = date.weekday() <= 4
        try:
            flag_holiday = is_holiday(date)
        except NotImplementedError:
            # BUG FIXES: 当日期超过chinese_calendar库所支持的范围时，抛出的异常并不是ValueError
            flag_holiday = False
        if flag_weekday and not flag_holiday:
            weekdays.append(date.date())
    return weekdays


if __name__ == '__main__':
    pass
