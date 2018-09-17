#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, g,redirect,make_response
from itsdangerous import TimedJSONWebSignatureSerializer as JwtSerializer
import functools

from config import Config

APP_ID = Config.APP_ID
APP_SECRET = Config.APP_SECRET
AUTH_SERVER_HOST = Config.AUTH_SERVER_HOST
AUTH_SERVER_LOGIN_URL = Config.AUTH_SERVER_LOGIN_URL
AUTH_SERVER_LOGOUT_URL = Config.AUTH_SERVER_LOGOUT_URL


class AccessTokenModel(object):
    def __init__(self, client_id, user):
        self.client_id = client_id
        self.user = user

    @classmethod
    def token2cls(cls, token,client_secret=APP_SECRET):
        if token:
            s = JwtSerializer(client_secret)
            try:
                data = s.loads(token)
                if "client_id" in data and "user" in data:
                    return cls(data["client_id"], data["user"])
                else:
                    return None
            except:
                return None
        else:
            return None


def get_access_token():
    access_token = request.headers.get("Authorization")
    access_token = request.args.get("accesstoken") if access_token is None else access_token
    access_token = request.cookies.get("accesstoken") if access_token is None else access_token
    access_token = request.form.get("accesstoken") if access_token is None else access_token
    return access_token


def authorize(access_token):
    token_obj = AccessTokenModel.token2cls(access_token)

    if token_obj:
        return token_obj
    else:
        return None


def need_login(save_token_at_cookie=True):
    """
    身份验证装饰器
    :param save_token_at_cookie:
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def auth(*args, **kw):
            access_token = get_access_token()
            user_obj = authorize(access_token)
            if user_obj:
                # 已登录
                g.user = user_obj.user
                g.userID = user_obj.user.get('id')
                response = make_response(func(*args, **kw))
                if save_token_at_cookie:
                    if (not request.cookies.get("accesstoken")) or (access_token!=request.cookies.get("accesstoken")) :
                        response.set_cookie("accesstoken", access_token)
                return response
            else:
                # 未登录或登录失效
                return redirect("{0}?appid={1}&callback={2}".format(AUTH_SERVER_LOGIN_URL,APP_ID,request.url))

        return auth

    return decorator


def logout():
    """
    用户退出引入方法
    :return:
    """
    response = make_response(redirect("{0}?appid={1}&callback={2}".format(AUTH_SERVER_LOGOUT_URL, APP_ID, request.host)))
    response.delete_cookie('accesstoken')
    return response
