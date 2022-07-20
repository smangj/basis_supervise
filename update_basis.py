# coding: utf-8
# Author: smangj
import click
import logging
import datetime as dt
import typing

import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from chinese_calendar import is_holiday

from app.common.log import init_logging
from app.db.session import session_scope
from app.db.sheet_class import BasisSupervise
from app.common.utils import to_pydatetime


def update_basis(date_range: typing.List[dt.date] = None):
    logger = logging.getLogger()

    if date_range is None:
        date_range = [dt.datetime.now().date()]

    reports = []
    for date in date_range:
        date = to_pydatetime(date).date()
        if is_holiday(date):
            continue

        reports += BasisSupervise.date_report(date)

    if len(reports) > 0:
        with session_scope() as session:
            for report in reports:
                session.add(report)

        logger.info("写入数据库成功...")
    else:
        logger.info("本次任务无数据...")


@click.command()
@click.option('--mode', default='task', type=click.Choice(['task', 'once']), help='task: cron task; once: run once')
def main(mode: str):
    logger = logging.getLogger()
    init_logging(logger, 'update_basis')
    if mode == 'once':
        update_basis()
    elif mode == 'task':
        scheduler = BlockingScheduler()
        scheduler.add_job(func=update_basis, trigger='cron', hour=18, minute=18)
        scheduler.start()


if __name__ == '__main__':
    main()
