#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Baoyi on 2018/3/26

import os
import requests
from img import img_printer
from set_color import *
import configparser
from func import trans_date
import re

cf = configparser.ConfigParser()
cf.read("ConfigParser.conf")

COMMENT_SHOW_URL = cf.get('url', 'COMMENT_SHOW_URL')


# weibo 具体页面和前5条评论
def weibo_detail(token, home_arg, op):
    """
    :param home_arg:
    :param op:
    :return:
    """
    count = 5
    page = 1
    index = int(op.split(' ')[0]) - 1
    os.system('clear')

    text = home_arg[index]['text']
    created_at = home_arg[index]['created_at']
    user_name = home_arg[index]['user_name']
    reposts_count = home_arg[index]['reposts_count']
    comments_count = home_arg[index]['comments_count']
    attitudes_count = home_arg[index]['attitudes_count']

    if len(op) > 3:
        try:
            arg = op.split(' ')[1:]

            for a in arg:
                if a.startswith('-p'):
                    page = int(a.split('=')[-1])
                elif a.startswith('-c'):
                    count = int(a.split('=')[-1])
        except Exception as e:
            print(termcolor.colored('参数错误', 'red'))

    params = {
        'access_token': token,
        'id': home_arg[index]['mid'],
        'count': count,
        'page': page
    }

    c = requests.get(url=COMMENT_SHOW_URL, params=params).json()

    print(weibo_user_name_color(user_name) + '  ' * 2 + created_at_color(created_at))
    print(text_color(text))
    print('转发: ' + str(reposts_count) + '  ' + '评论: ' + str(comments_count) + '  ' + '点赞: ' + str(attitudes_count))
    if home_arg[index]['pic_urls']:
        [img_printer(i) for i in home_arg[index]['pic_urls'].split('\n')]

    print('*' * 35)

    for i, t in enumerate(c['comments']):
        comment_user_name = t['user']['name']
        comment_text = t['text']
        comment_created_at = trans_date(t['created_at'])
        print(termcolor.colored(str(i + 1) + '. ', 'magenta') + user_name_color(
            comment_user_name) + '  ' * 2 + created_at_color(
            comment_created_at))
        print(comment_text_color(comment_text))
        print('-' * 35)
