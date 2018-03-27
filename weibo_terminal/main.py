#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Baoyi on 2018/3/26

import configparser
import os
import re

from login import get_token
from set_color import *
from detail import weibo_detail
from timeline import home_operation
from collections import deque
from help import func_help

cf = configparser.ConfigParser()
cf.read("ConfigParser.conf")

if __name__ == '__main__':
    user = cf.get('user', 'user')
    password = cf.get('user', 'password')

    # 设置一个op队列用于存储命令
    deque_home = deque(maxlen=1)
    deque_detail = deque(maxlen=1)

    token = get_token(user=user, password=password)

    # 设计一个全局变量position 来标记当前所在位置
    global position, home_arg
    position = 'home'

    while True:
        op = input(remind_color("Operate$ "))
        if op.startswith('home') or op == '\n':
            # 将position 置位为home
            position = 'home'
            deque_home.append(op)
            home_arg = home_operation(token, op)

        elif op == 'clear':
            os.system('clear')
        elif op == 'pwd':
            print(position)
        elif '0' <= op[:1] <= '9':
            # 将position 置位为detail
            position = 'detail'
            deque_detail.append(op)

            if 0 < int(op.split(' ')[0]) <= len(home_arg):
                weibo_detail(token, home_arg, op)
            else:
                print(termcolor.colored('序号错误', 'red', attrs=['bold']))
        elif op == 'n':
            # 判断当前所在位置, 若为home则主页翻页，若为detail则微博评论页翻页
            if position == 'home':
                # 如果position在home, 更新page实现home翻页
                last_op = deque_home.popleft()
                if '-p' in last_op:
                    page = re.search(r'-p=\d+', last_op).group(0).split('=')[-1]
                    new_op = last_op.replace('-p=' + str(page), '-p=' + str(int(page) + 1))
                else:
                    new_op = last_op + ' -p=2'

                deque_home.append(new_op)
                home_arg = home_operation(token, new_op)

            elif position == 'detail':
                last_op = deque_detail.popleft()
                if '-p' in last_op:
                    page = re.search(r'-p=\d+', last_op).group(0).split('=')[-1]
                    new_op = last_op.replace('-p=' + str(page), '-p=' + str(int(page) + 1))
                else:
                    new_op = last_op + ' -p=2'

                deque_detail.append(new_op)
                weibo_detail(token, home_arg, new_op)

        elif op == 'p':
            # 判断当前所在位置, 若为home则主页翻页，若为detail则微博评论页翻页
            if position == 'home':
                # 如果position在home, 更新page实现home翻页
                last_op = deque_home.popleft()
                if '-p' in last_op:
                    page = re.search(r'-p=\d+', last_op).group(0).split('=')[-1]
                    if int(page) > 1:
                        new_op = last_op.replace('-p=' + str(page), '-p=' + str(int(page) - 1))
                    else:
                        new_op = last_op + ' -p=1'
                else:
                    new_op = last_op + ' -p=2'

                deque_home.append(new_op)
                home_arg = home_operation(token, new_op)

            elif position == 'detail':
                last_op = deque_detail.popleft()
                if '-p' in last_op:
                    page = re.search(r'-p=\d+', last_op).group(0).split('=')[-1]
                    if int(page) > 1:
                        new_op = last_op.replace('-p=' + str(page), '-p=' + str(int(page) - 1))
                    else:
                        new_op = last_op + ' -p=1'
                else:
                    new_op = last_op + ' -p=2'

                deque_detail.append(new_op)
                weibo_detail(token, home_arg, new_op)

        elif op == 'help':
            func_help()

        elif op == 'exit':
            exit()
