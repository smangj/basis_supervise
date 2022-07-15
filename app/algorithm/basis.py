# coding: utf-8
# Author: smangj
import datetime as dt
import numpy as np

from app.common.holidays import get_num_workdays, NUM_WORKDAYS_PER_YEAR


def compute_basis(spot: float, futures: float, today: dt.date, end_date: dt.date) -> float:
    workdays_to_maturity = get_num_workdays(today, end_date) - 1
    if workdays_to_maturity == 0:
        return np.nan
    else:
        basis = spot - futures
        yearly = NUM_WORKDAYS_PER_YEAR / workdays_to_maturity
        return basis / spot * yearly


if __name__ == '__main__':
    pass
