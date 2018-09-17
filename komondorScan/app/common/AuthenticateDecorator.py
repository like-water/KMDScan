#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from flask import request, g, redirect, make_response
from .alopex_auth_sdk import authorize
from config import Config
from .ApiResponse import ApiResponse, ResposeStatus
from ..common.api_sign_sdk import SignatureGeneration


def need_user(roles=[]):
    def decorator(func):
        @functools.wraps(func)
        def auth(*args, **kwargs):
            access_token = request.headers.get("Authorization")
            user_obj = authorize(access_token)
            if user_obj:
                g.user = user_obj.user
                g.userID = user_obj.user.get("id")
                if (roles and
                        g.user.get("role") in roles) or roles.__len__() == 0:
                    response = func(*args, **kwargs)
                    return response
                else:
                    return ApiResponse(None, ResposeStatus.Powerless)
            else:
                return ApiResponse(None, ResposeStatus.AuthenticationFailed)
        return auth

    return decorator


def need_power(power):
    def decorator(func):
        @functools.wraps(func)
        def auth(*args, **kwargs):
            access_token = request.headers.get("Authorization")
            user_obj = authorize(access_token)
            if user_obj:
                g.user = user_obj.user
                g.userID = user_obj.user.get("id")
                if Config.POWERS.get(power) and (
                        g.user.get("role") in Config.POWERS.get(power)):
                    response = func(*args, **kwargs)
                    return response
                else:
                    return ApiResponse(None, ResposeStatus.Powerless)
            else:
                return ApiResponse(None, ResposeStatus.AuthenticationFailed)

        return auth

    return decorator


def need_sign():
    def decorator(func):
        @functools.wraps(func)
        def auth(*args, **kwargs):
            access_token = request.headers.get("Authorization")
            signature = request.headers.get("X-Signature")
            access = False
            if access_token:
                user_obj = authorize(access_token)
                if user_obj:
                    access = True
                else:
                    return ApiResponse(None,
                                       ResposeStatus.AuthenticationFailed)

            elif signature:
                req = {}
                if request.form:
                    req = dict(req, **request.form.to_dict())
                if request.args:
                    req = dict(req, **request.args.to_dict())
                if request.json:
                    req = dict(req, **request.json)
                if signature == SignatureGeneration(req):
                    access = True
                else:
                    return ApiResponse(None, ResposeStatus.SignFail)

            if access:
                response = func(*args, **kwargs)
                return response
            else:
                return ApiResponse(None, ResposeStatus.SignFail)

        return auth

    return decorator