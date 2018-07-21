#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import requests


def SignatureGeneration(res_dict={}, secret_key=""):
    """
    生成签名
    :param secret_key: 签名 Key
    :param time_out: 签名过期时间
    :param res_dict: 签名参数体
    :return:
    """
    print res_dict
    key_list = res_dict.keys()
    key_list.sort()
    sign_str = u''
    for key in key_list:
        if not isinstance(res_dict.get(key), (dict, list)):
            sign_str += unicode(res_dict.get(key))
    # secret_key + value 组合字符串 md5 取中间16位
    sign_str = secret_key + sign_str
    sign = hashlib.md5(sign_str).hexdigest()[8:-8]
    return sign


def post_with_sign(url, data=None, json=None, secret_key="", **kwargs):
    """
    requests post 自动附带签名
    :param url: 
    :param data: 
    :param json: 
    :param secret_key: 
    :param kwargs: 
    :return: 
    """
    if data:
        sign = SignatureGeneration(data, secret_key)
    elif json:
        sign = SignatureGeneration(json, secret_key)
    else:
        sign = SignatureGeneration(secret_key=secret_key)

    if kwargs.get("headers"):
        kwargs["headers"] = dict(
            kwargs.get("headers"), **{'X-Signature': sign})
    else:
        kwargs["headers"] = {'X-Signature': sign}
    return requests.post(url, data, json, **kwargs)


def get_with_sign(url, params=None, secret_key="", **kwargs):
    """
    requests get 自动附带签名
    :param url: 
    :param params: 
    :param secret_key: 
    :param kwargs: 
    :return: 
    """
    if params:
        sign = SignatureGeneration(params, secret_key)
    else:
        sign = SignatureGeneration(secret_key=secret_key)

    if kwargs.get("headers"):
        kwargs["headers"] = dict(
            kwargs.get("headers"), **{'X-Signature': sign})
    else:
        kwargs["headers"] = {'X-Signature': sign}
    return requests.get(url, params, **kwargs)


def put_with_sign(url, data=None, secret_key="", **kwargs):
    """
    requests put 自动附带签名
    :param url: 
    :param data: 
    :param secret_key: 
    :param kwargs: 
    :return: 
    """
    if data:
        sign = SignatureGeneration(data, secret_key)
    else:
        sign = SignatureGeneration(secret_key=secret_key)

    if kwargs.get("headers"):
        kwargs["headers"] = dict(
            kwargs.get("headers"), **{'X-Signature': sign})
    else:
        kwargs["headers"] = {'X-Signature': sign}
    return requests.put(url, data, **kwargs)


def delete_with_sign(url, secret_key="", **kwargs):
    """
    requests delete 自动附带签名
    :param url: 
    :param secret_key: 
    :param kwargs: 
    :return: 
    """
    sign = SignatureGeneration(secret_key=secret_key)
    if kwargs.get("headers"):
        kwargs["headers"] = dict(
            kwargs.get("headers"), **{'X-Signature': sign})
    else:
        kwargs["headers"] = {'X-Signature': sign}
    return requests.delete(url, **kwargs)


def head_with_sign(url, secret_key="", **kwargs):
    """
    requests head 自动附带签名
    :param url: 
    :param secret_key: 
    :param kwargs: 
    :return: 
    """
    sign = SignatureGeneration(secret_key=secret_key)
    if kwargs.get("headers"):
        kwargs["headers"] = dict(
            kwargs.get("headers"), **{'X-Signature': sign})
    else:
        kwargs["headers"] = {'X-Signature': sign}
    return requests.head(url, **kwargs)


def options_with_sign(url, secret_key="", **kwargs):
    """
    requests options 自动附带签名
    :param url: 
    :param secret_key: 
    :param kwargs: 
    :return: 
    """
    sign = SignatureGeneration(secret_key=secret_key)
    if kwargs.get("headers"):
        kwargs["headers"] = dict(
            kwargs.get("headers"), **{'X-Signature': sign})
    else:
        kwargs["headers"] = {'X-Signature': sign}
    return requests.options(url, **kwargs)


def patch_with_sign(url, data=None, secret_key="", **kwargs):
    """
    requests patch 自动附带签名
    :param url: 
    :param data: 
    :param secret_key: 
    :param kwargs: 
    :return: 
    """
    if data:
        sign = SignatureGeneration(data, secret_key)
    else:
        sign = SignatureGeneration(secret_key=secret_key)

    if kwargs.get("headers"):
        kwargs["headers"] = dict(
            kwargs.get("headers"), **{'X-Signature': sign})
    else:
        kwargs["headers"] = {'X-Signature': sign}
    return requests.patch(url, data, **kwargs)
