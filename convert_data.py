#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/4/4 16:16
# @Author   : wsy
# @email    : 631535207@qq.com
import os

import pandas as pd
from qlib_scripts import dump_bin
from utils.path import check_and_mkdirs, PROJ_ROOT_DIR

raw_path = str(PROJ_ROOT_DIR.joinpath("data/basis_supervise.csv"))
csv_output_dir = str(PROJ_ROOT_DIR.joinpath("data/csv_data"))
qlib_dir = str(PROJ_ROOT_DIR.joinpath("data/qlib_data"))
check_and_mkdirs(csv_output_dir)
check_and_mkdirs(qlib_dir)


def raw_to_csv():
    raw = pd.read_csv(raw_path)
    raw.groupby()

def csv_to_bin():
    dump_bin.DumpDataAll(
        csv_path=csv_output_dir, qlib_dir=qlib_dir, date_field_name="date"
    ).dump()


if __name__ == "__main__":
    raw_to_csv()
