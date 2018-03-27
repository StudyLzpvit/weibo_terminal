#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Baoyi on 2018/3/24

import termcolor
import configparser
import base64
import rsa
import binascii
import requests
import json

cf = configparser.ConfigParser()
cf.read("ConfigParser.conf")

# 读取配置
APP_KEY = cf.get("weibo", "APP_KEY")
MY_APP_SECRET = cf.get("weibo", "MY_APP_SECRET")
REDIRECT_URL = cf.get("weibo", "REDIRECT_URL")

TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'


def get_token(user, password):
    try:
        print(termcolor.colored("正在尝试从配置文件中获取token...", "magenta"))
        token = cf.get('weibo', 'TOKEN')
        print(termcolor.colored("获取code成功", "green"))
        print(termcolor.colored("登陆成功!", "green"))

        return token
    except:
        print(termcolor.colored('配置文件中不存在token', 'red'))
        print(termcolor.colored("正在为您登录微博...", "magenta"))

        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=openapi&callback=sinaSSOController.preloginCallBack&su={su}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)&_=1450667794267'
        su = base64.b64encode(user.encode('utf-8'))

        pre = requests.get(url=url.format(su=su)).content.decode('utf-8')
        step_one_call_back = json.loads(pre[35:-1])

        servertime = step_one_call_back['servertime']
        nonce = step_one_call_back['nonce']
        pubkey = step_one_call_back['pubkey']
        rsakv = step_one_call_back['rsakv']

        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        sp = rsa.encrypt(message.encode('utf-8'), key)  # 加密
        sp = binascii.b2a_hex(sp)  # 将加密信息转换为16进制。

        postPara = {
            'entry': 'openapi',
            'gateway': '1',
            'from': '',
            'savestate': '0',
            'userticket': '1',
            'pagerefer': '',
            'ct': '1800',
            's': '1',
            'vsnf': '1',
            'vsnval': '',
            'door': '',
            'appkey': '52laFx',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': sp,
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'cdult': '2',
            'domain': 'weibo.com',
            'prelt': '2140',
            'returntype': 'TEXT',
        }
        get_ticket_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=1450667802929'
        headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Referer": url,
            "Content-Type": "application/x-www-form-urlencoded",
            'Connection': 'close'}
        step_two_call_back = requests.post(get_ticket_url, postPara, headers=headers).json()

        ticket = step_two_call_back['ticket']

        fields = {
            'action': 'login',
            'display': 'default',
            'withOfficalFlag': '0',
            'quick_auth': 'null',
            'withOfficalAccount': '',
            'scope': '',
            'ticket': ticket,
            'isLoginSina': '',
            'response_type': 'code',
            'regCallback': 'https://api.weibo.com/2/oauth2/authorize?client_id=' + APP_KEY + '&response_type=code&display=default&redirect_uri=' + REDIRECT_URL + '&from=&with_cookie=',
            'redirect_uri': REDIRECT_URL,
            'client_id': APP_KEY,
            'appkey62': '52laFx',
            'state': '',
            'verifyToken': 'null',
            'from': '',
            'switchLogin': '0',
            'userId': '',
            'passwd': ''
        }
        post_url = 'https://api.weibo.com/oauth2/authorize'

        try:
            requests.post(post_url, data=fields, headers=headers)
        except Exception as e:
            # 由于网页不存在所有从错误信息中获取code
            code = str(e).split('code=')[-1].split(' (Caused')[0]

            params = {
                'client_id': APP_KEY,
                'client_secret': MY_APP_SECRET,
                'code': code,
                'redirect_uri': REDIRECT_URL
            }
            token = requests.post(url=TOKEN_URL, params=params).json()['access_token']
            print(termcolor.colored("登陆成功!", "green"))

            print(termcolor.colored('正在写入配置', 'yellow'))
            cf.set("weibo", 'token', token)
            with open("ConfigParser.conf", "w+") as f:
                cf.write(f)
            print(termcolor.colored("写入配置成功!", "green"))

            return token
