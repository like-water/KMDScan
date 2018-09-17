#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# 这里ip、数据库等信息都是瞎写的，大家按照自己实际情况填写
class Config_Dev(object):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:zxc123zxc@1.1.7.6/kmd_scan?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 要比数据库 wait_timeout 参数要小
    SQLALCHEMY_POOL_RECYCLE = 50
    SQLALCHEMY_ECHO = True
    ID_TOKEN_DEFAULT_EXPIRES = 8640000

    ACCESS_TOKEN_DEFAULT_EXPIRES = 86400
    CORS_ORIGINS = "*"

    APP_ID = "3d0ca0517d9211e7bc3fac87a304fa2e"
    APP_SECRET = "J4SlsHZ9lXrtd2C5tWlh1Xvljf6YBUcu5e4gfRdM"

    AUTH_SERVER_HOST = "http://12.18.7.60:6200"
    AUTH_SERVER_LOGIN_URL = "http://12.168.7.60:6200/login"
    AUTH_SERVER_LOGOUT_URL = "http://12.168.7.60:6200/logout"

    REDIS_HOST = "192.168.7.60"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_AUTH = ""

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_IGNORE_RESULT = True
    CELERY_RESULT_BACKEND = "redis://192.168.7.60:6379/0"
    CELERY_TASK_RESULT_EXPIRES = 18000

    # CELERY_BROKER_URL = "amqp://admin:zxc123zxc@192.168.6.60/kmdscan"
    CELERY_BROKER_URL = "redis://192.168.7.60:6379/0"

    POWERS = {
        "WritePOC": ["ADMIN"]
    }

    SUPERVISORMAN_HOST = "http://192.168.7.60:6215"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    POCS_DIR = BASE_DIR + '/pocs/'
    PLUGINS_DIR = BASE_DIR + '/plugins/'

    DATA_SOURCE_PROXY_TEMPLATE = "/Users/Bevis/.pyenv/versions/3.6.0/bin/python " \
                                 "/Users/Bevis/.pyenv/versions/3.6.0/bin/mitmweb " \
                                 "--web-port {web_port} --port {proxy_port} " \
                                 "--web-iface 0.0.0.0 " \
                                 "-s /Users/Bevis/Documents/Projects/Git/komondorScan/tools/proxy_script.py " \
                                 "--client-certs /Users/Bevis/.mitmproxy " \
                                 "--cert *.apitops.com=/Users/Bevis/.mitmproxy/apitops.com.pem " \
                                 "--cert *.tops001.com=/Users/Bevis/.mitmproxy/tops001.com.pem "

    SWAGGER = {
        'uiversion': 3,
        'title': 'KomondorScan',
        'description': 'KomondorScan Api',
        "version": "0.0.1"
    }


class Config_Ga(Config_Dev):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://opskit:bLKGLQBtdxBVDqsk5Jy73RBkifbNML@mysql.00.upanb.cn/kk_opskit?charset=utf8mb4"
    SQLALCHEMY_ECHO = False
    AUTH_SERVER_HOST = "http://alopex.apitops.com"
    AUTH_SERVER_LOGIN_URL = "http://alopex.apitops.com/login"
    AUTH_SERVER_LOGOUT_URL = "http://alopex.apitops.com/logout"

    APP_ID = "3f6fe0f28bbd11e7962000163e133b79"
    APP_SECRET = "u4qjdhXQLpFLVfNizyFZzpEH0brVpd90KX2iesSQ"

    CELERY_BROKER_URL = "redis://:VKbyBfgZ4Y4gx3mEfqCLnSeJSppCLu@redis.901.upanb.cn:6379/20"
    CELERY_RESULT_BACKEND = "redis://:VKbyBfgZ4Y4gx3mEfqCLnSeJSppCLu@redis.901.upanb.cn:6379/20"

    REDIS_HOST = "redis.901.upanb.cn"
    REDIS_PORT = 6379
    REDIS_DB = 20
    REDIS_AUTH = "VKbyBfgZ4Y4gx3mEfqCLnSeJSppCLu"

    SUPERVISORMAN_HOST = "http://127.0.0.1:6215"

    CORS_ORIGINS = ["http://kmdscan.apitops.com"]

    DATA_SOURCE_PROXY_TEMPLATE = "/home/admin/.pyenv/versions/3.6.2/bin/python " \
                                 "/home/admin/.pyenv/versions/3.6.2/bin/mitmweb " \
                                 "--web-port {web_port} --port {proxy_port} " \
                                 "--web-iface 0.0.0.0 --insecure " \
                                 "-s /home/admin/projects/komondorScan/tools/proxy_script.py " \
                                 "--client-certs /home/admin/.mitmproxy " \
                                 "--cert *.apitops.com=/home/admin/.mitmproxy/apitops.com.pem " \
                                 "--cert *.tops001.com=/home/admin/.mitmproxy/tops001.com.pem "


Config = Config_Dev

if os.environ.get('ENV_CODE') == "GA":
    Config = Config_Ga
