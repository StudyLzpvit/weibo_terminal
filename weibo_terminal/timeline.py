#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Baoyi on 2018/3/23

import configparser
import requests
import re

from func import trans_date
from img import img_printer
from set_color import *

cf = configparser.ConfigParser()
cf.read("ConfigParser.conf")

HOME_TIMELINE_URL = cf.get('url', 'HOME_TIMELINE_URL')
STATUSES_SHOW_URL = cf.get('url', 'STATUSES_SHOW_URL')
COMMENT_SHOW_URL = cf.get('url', 'COMMENT_SHOW_URL')

session = requests.session()


def home_timeline(access_token, page=1, count=10, feature=0, mode=1):
    """

    :param mode: 设置图片模式
    :param access_token: 用户的access_token, 用于验证权限获取数据
    :param page: 数据的页数，默认为1
    :param count: 每页返回的数量，默认为20，最大为100
    :param feature: 过滤类型ID，0：全部、1：原创、2：图片、3：视频、4：音乐，默认为0。
    :return: 返回用户的home_timeline, 获取当前登录用户及其所关注（授权）用户的最新微博
    """
    params = {
        'access_token': access_token,
        'page': page,
        'count': count,
        'feature': feature
    }

    j = session.get(url=HOME_TIMELINE_URL, params=params).json()

    """

        :param j: 请求返回的json数据
        :param mode: 选择图片显示的模式，0为忽略图片，1为显示图片url, 2为显示字符图片
        :return: 返回mid和uid数组组成的dict
        """
    statuses = j['statuses']
    return_list = []

    for i, status in enumerate(statuses):
        created_at = trans_date(status['created_at'])
        mid = status['id']
        uid = status['user']['id']
        user_name = status['user']['name']
        reposts_count = status['reposts_count']
        comments_count = status['comments_count']
        geo = status['geo']
        attitudes_count = status['attitudes_count']
        text = status['text']
        # 图片链接
        pic_urls = '\n'.join([i.get('thumbnail_pic') for i in status['pic_urls'] if status['pic_urls']])

        insert_data = {
            'created_at': created_at,
            'mid': mid,
            'uid': uid,
            'user_name': user_name,
            'reposts_count': reposts_count,
            'comments_count': comments_count,
            'attitudes_count': attitudes_count,
            'text': text,
            'pic_urls': pic_urls

        }

        return_list.append(insert_data)

        print(num_color('【' + str(i + 1) + '】'), user_name_color(user_name) + '  ' * 2 + created_at_color(created_at))
        print(text_color(text))

        if mode == 1:
            print(pic_urls)

        elif mode == 2:
            # 添加缩略图
            try:
                if status['pic_urls']:
                    [img_printer(i.get('thumbnail_pic')) for i in status['pic_urls']]
                    print('\n')
            except:
                pass

        elif mode == 3:
            # 添加原图
            try:
                if status['pic_urls']:
                    [img_printer(i.get('thumbnail_pic').replace('thumbnail', 'large')) for i in status['pic_urls']]
                    print('')
            except:
                pass
        else:
            pass

        print('转发: ' + str(reposts_count) + '  ' + '评论: ' + str(comments_count) + '  ' + '点赞: ' + str(attitudes_count))
        if geo:
            print('位置: ' + str(geo['coordinates'][0]) + ',' + str(geo['coordinates'][1]))
        print('*' * 35)

    return return_list


def home_operation(token, op):
    # 初始化参数
    page = 1,
    count = 10,
    feature = 0,
    mode = 0
    # 正则验证参数是否正确
    pattern = re.match(r'home( \-[pcfm]\=[0-9]+)*', op).group(0)
    if pattern == op:
        arg = op.split(' ')[1:]

        for a in arg:
            if a.startswith('-p'):
                page = int(a.split('=')[-1])
            elif a.startswith('-c'):
                count = int(a.split('=')[-1])
            elif a.startswith('-f'):
                feature = int(a.split('=')[-1])
                if feature in range(5):
                    pass
                else:
                    feature = 0
            elif a.startswith('-m'):
                mode = int(a.split('=')[-1])
        home_arg = home_timeline(token, page=page, count=count, feature=feature,
                                 mode=mode)

        return home_arg
    else:
        print(termcolor.colored('参数传入错误', 'red'))
