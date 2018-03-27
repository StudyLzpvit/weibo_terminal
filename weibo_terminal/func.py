#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Baoyi on 2018/3/26

import datetime

# 转化时间格式
def trans_date(d: str) -> str:
    n = d.replace(' +0800', '')
    dt_obj = datetime.datetime.strptime(n, "%a %b %d %H:%M:%S %Y")
    date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    return date_str
