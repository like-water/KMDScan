# -*- coding: utf-8 -*-
from flasgger import swag_from
from flask_restful import Resource, reqparse

from . import api
from ..common.ApiResponse import PageResponse
from ..common.AuthenticateDecorator import need_sign
from ..common.RequestInputs import int_min
from ..common.api_doc_helper import get_request_parser_doc_dist
from ..domain.task_log_domain import get_log_page_by_task


def page_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("pageSkip", type=int_min(0), default=0)
    rp.add_argument("pageTake", type=int_min(1), default=10)
    rp.add_argument("code", type=int, default=0)
    return rp.parse_args() if return_parse_args else rp


class TaskLogResource(Resource):
    @swag_from(get_request_parser_doc_dist("Task Log列表", ["Log"], page_args(False)))
    @need_sign()
    def get(self, task_id):
        args = page_args()
        page, total = get_log_page_by_task(task_id, args.pageSkip, args.pageTake, args.code)
        return PageResponse(page, total)


api.add_resource(TaskLogResource, "/tasklog/<task_id>")
