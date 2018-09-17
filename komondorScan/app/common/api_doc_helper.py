#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import collections


def get_request_parser_doc_dist(desc="", tag=[], rp=None):
    """
    根据 RequestParser 生成 Swagger Dict
    :param desc:  接口描述
    :param tag:   标签
    :param rp:    RequestParser
    :return:
    """
    rel = {
        "description": desc,
        "summary": desc,
        "tags": tag,
        "parameters": [{
            "name": arg.name,
            "in": ",".join(arg.location),
            "type": arg.type.__class__.__name__ if
            isinstance(arg.type, collections.Callable) else arg.type.__name__,
            "required": arg.required,
            "default": arg.default,
            "description": arg.help if arg.help else arg.name
        } for arg in rp.args] if rp else []
    }
    return rel
