#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import requests
from .api_sign_sdk import SignatureGeneration


def post(host, url, need_sign=False, secret_key="",only_json=True):
    def decorator(func):
        @functools.wraps(func)
        def request(*args, **kw):
            headers = {
                "Content-Type": "application/json"
            }
            params = {}
            rstUrl = host + "/" + url
            rel = func(*args, **kw)
            if type(rel) == tuple:
                params = rel[0]
                rstUrl = rstUrl % rel[1]
            else:
                params = rel
            if need_sign:
                sign = SignatureGeneration(params, secret_key)
                headers["X-Signature"] = sign
            response = requests.post(rstUrl, headers=headers, json=params, timeout=20)
            if only_json:
                if response.status_code == 500:
                    raise StandardError("请求服务器错误:%s" % rstUrl, params)
                return response.json()
            else:
                return response

        return request

    return decorator


def get(host, url, need_sign=False, secret_key="",only_json=True):
    def decorator(func):
        @functools.wraps(func)
        def request(*args, **kw):
            params = {}
            headers = {}
            rstUrl = host + "/" + url
            rel = func(*args, **kw)
            if type(rel) == tuple:
                params = rel[0]
                rstUrl = rstUrl % rel[1]
            else:
                params = rel
            if need_sign:
                sign = SignatureGeneration(params, secret_key)
                headers["X-Signature"] = sign
            response = requests.get(rstUrl, params=params, timeout=20, headers=headers)
            if only_json:
                if response.status_code == 500:
                    raise StandardError("请求服务器错误:%s" % rstUrl, params)
                return response.json()
            else:
                return response

        return request

    return decorator


def put(host, url, need_sign=False, secret_key="",only_json=True):
    def decorator(func):
        @functools.wraps(func)
        def request(*args, **kw):
            headers = {
                "Content-Type": "application/json"
            }
            params = {}
            rstUrl = host + "/" + url
            rel = func(*args, **kw)
            if type(rel) == tuple:
                params = rel[0]
                rstUrl = rstUrl % rel[1]
            else:
                params = rel
            if need_sign:
                sign = SignatureGeneration(params, secret_key)
                headers["X-Signature"] = sign
            response = requests.put(rstUrl, headers=headers, json=params, timeout=10)
            if only_json:
                if response.status_code == 500:
                    raise StandardError("请求服务器错误:%s" % rstUrl, params)
                return response.json()
            else:
                return response

        return request

    return decorator


def delete(host, url, need_sign=False, secret_key="",only_json=True):
    def decorator(func):
        @functools.wraps(func)
        def request(*args, **kw):
            headers = {
                "Content-Type": "application/json"
            }
            params = {}
            rstUrl = host + "/" + url
            rel = func(*args, **kw)
            if type(rel) == tuple:
                params = rel[0]
                rstUrl = rstUrl % rel[1]
            else:
                params = rel
            if need_sign:
                sign = SignatureGeneration(params, secret_key)
                headers["X-Signature"] = sign
            response = requests.delete(rstUrl, headers=headers, json=params, timeout=10)
            if only_json:
                if response.status_code == 500:
                    raise StandardError("请求服务器错误:%s" % rstUrl, params)
                return response.json()
            else:
                return response

        return request

    return decorator
