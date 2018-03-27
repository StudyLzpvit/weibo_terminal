#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Baoyi on 2018/3/26

import termcolor

# 定义文本颜色
num_color = lambda x: termcolor.colored(x, 'red')
user_name_color = lambda x: termcolor.colored(x, 'blue')
created_at_color = lambda x: termcolor.colored(x, 'green')
text_color = lambda x: termcolor.colored(x, 'yellow')
remind_color = lambda x: termcolor.colored(x, 'blue')
weibo_user_name_color = lambda x: termcolor.colored(x, 'red', 'on_cyan')
comment_text_color = lambda x: termcolor.colored(x, 'white')
