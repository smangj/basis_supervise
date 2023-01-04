# coding: utf-8
# Author: smangj
import logging

import numpy as np
import sqlalchemy as sa
import typing
import pandas as pd
import datetime as dt

from sqlalchemy.ext.declarative import declarative_base

from app.algorithm.basis import compute_basis
from app.db.session import project_engine, Session
from app.tushare import index_future_basic, index_price, future_date_price
from app.common.utils import to_pydatetime

Base = declarative_base()
INDEX_LIST = ['IC', 'IF', 'IH']


class BasisSupervise(Base):
    __tablename__ = 'basis_supervise'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    date = sa.Column(sa.DateTime, comment='日期')
    va_type = sa.Column(sa.String(32), comment='交易品种')
    spot_price = sa.Column(sa.FLOAT, comment='现货价格')
    future_1_id = sa.Column(sa.String(32), comment='当月期货交易代码')
    future_2_id = sa.Column(sa.String(32), comment='近月期货交易代码')
    future_3_id = sa.Column(sa.String(32), comment='季月期货交易代码')
    future_4_id = sa.Column(sa.String(32), comment='远月期货交易代码')
    future_1_price = sa.Column(sa.FLOAT, comment='当月期货价格')
    future_2_price = sa.Column(sa.FLOAT, comment='近月期货价格')
    future_3_price = sa.Column(sa.FLOAT, comment='季月期货价格')
    future_4_price = sa.Column(sa.FLOAT, comment='远月期货价格')
    future_1_basis = sa.Column(sa.FLOAT, comment='当月期货基差')
    future_2_basis = sa.Column(sa.FLOAT, comment='近月期货基差')
    future_3_basis = sa.Column(sa.FLOAT, comment='季月期货基差')
    future_4_basis = sa.Column(sa.FLOAT, comment='远月期货基差')
    future_1_cost = sa.Column(sa.FLOAT, nullable=True, comment='当月期货基差贴水率（年化）')
    future_2_cost = sa.Column(sa.FLOAT, comment='近月期货基差贴水率（年化）')
    future_3_cost = sa.Column(sa.FLOAT, comment='季月期货基差贴水率（年化）')
    future_4_cost = sa.Column(sa.FLOAT, comment='远月期货基差贴水率（年化）')

    __table_args__ = (
        sa.Index('ix_date', date),
        sa.Index('ix_va_type_date', va_type, date),
    )

    @classmethod
    def date_report(cls, date: typing.Union[dt.datetime, dt.date, str, pd.Timestamp, None]) -> typing.List[
        "BasisSupervise"]:
        """
        返回股指期货某个日期的监控表
        """
        logger = logging.getLogger()
        reports = []
        format_date = to_pydatetime(date)
        basic_info = index_future_basic(format_date.strftime('%Y%m%d'))
        for va_type in INDEX_LIST:
            spot_price = index_price(va_type, format_date.strftime('%Y%m%d'))
            if spot_price is None:
                continue
            # 筛选信息并排序
            va_type_mask = basic_info['ts_code'].str.contains(va_type)
            va_type_basic_info = basic_info.loc[va_type_mask].sort_values(by='delist_date', ascending=True)
            # 获得期货代码
            future_id = va_type_basic_info['ts_code'].str.split(pat=r'\.', expand=True).iloc[:, 0].values
            future_price = []
            basis = []
            cost = []
            for i in range(len(va_type_basic_info)):
                fp = future_date_price(va_type_basic_info['ts_code'].iloc[i], format_date.strftime('%Y%m%d'))
                end_date = va_type_basic_info['delist_date'].iloc[i]
                future_price.append(fp)
                basis.append(spot_price - fp)
                year_cost = compute_basis(spot_price, fp, format_date.date(), to_pydatetime(end_date).date())
                cost.append(year_cost)
            report = BasisSupervise(date=format_date,
                                    va_type=va_type,
                                    spot_price=spot_price,
                                    future_1_id=future_id[0],
                                    future_2_id=future_id[1],
                                    future_3_id=future_id[2],
                                    future_4_id=future_id[3],
                                    future_1_price=future_price[0],
                                    future_2_price=future_price[1],
                                    future_3_price=future_price[2],
                                    future_4_price=future_price[3],
                                    future_1_basis=basis[0],
                                    future_2_basis=basis[1],
                                    future_3_basis=basis[2],
                                    future_4_basis=basis[3],
                                    future_1_cost=None if cost[0] is np.nan else cost[0],
                                    future_2_cost=cost[1],
                                    future_3_cost=cost[2],
                                    future_4_cost=cost[3])
            logger.info("[{}]-[{}]-的贴水幅度为[{}%,{}%,{}%,{}%]".format(date, va_type,
                                                                   'nan' if cost[0] is np.nan else round(cost[0] * 100),
                                                                   round(cost[1] * 100),
                                                                   round(cost[2] * 100),
                                                                   round(cost[3] * 100)))
            reports.append(report)

        return reports

    @classmethod
    def get_newest_data(cls) -> pd.DataFrame:
        max_date_query = Session.query(sa.func.max(cls.date).label('date')).subquery()
        query = Session.query(cls).join(max_date_query, max_date_query.c.date == cls.date)

        return pd.read_sql(query.statement, Session.connection())

    @classmethod
    def get_newest_date(cls) -> dt.datetime:
        data = cls.get_newest_data()
        return to_pydatetime(data['date'].iloc[0])


if __name__ == '__main__':
    BasisSupervise.__table__.create(project_engine, checkfirst=True)
