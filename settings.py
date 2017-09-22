# -*- coding: utf-8 -*-
import os

STATIC_PATH = os.path.join(os.path.dirname(__file__),'static')
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__),'templates')
LOG_LEVAL = 'debug'
LOG_FILE = os.path.join(os.path.dirname(__file__),'logs/log.log')
#app基本设置
app_settings = dict(
    static_path=STATIC_PATH,
    debug=True,
    xsrf_cookies = True,
    cookie_secret='PQvw9USaSwWuPNrs6m6x/MsurHFz6UjGrqOXeK4GAoU=',
    login_url = '/login',#设置用户验证未通过时 跳转到的页面
)

#数据库设置
MYSQL_SETTINGS=dict(
    database='TORNADO',
    # max_connections=20,timeout=60,
    host='127.0.0.1',
    user='root',
    password='g123567G'
)

REDIS_SETTINGS = dict(
    host='127.0.0.1',
    port = 6379
)


