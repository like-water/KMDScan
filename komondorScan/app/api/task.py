# -*- coding: utf-8 -*-
from flasgger import swag_from
from flask_restful import Resource, reqparse

from . import api
from ..common import time_helper
from ..common.ApiResponse import ApiResponse, ResposeStatus, PageResponse
from ..common.RequestInputs import json_dict, int_min
from ..common.api_doc_helper import get_request_parser_doc_dist
from ..domain.task_domain import create_task, cancel_task, start_scan_task, get_tasks_page, get_task_detail
from ..common.AuthenticateDecorator import need_sign


def page_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("pageSkip", type=int_min(0), default=0)
    rp.add_argument("pageTake", type=int_min(1), default=10)
    return rp.parse_args() if return_parse_args else rp


def post_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("dataSource", type=unicode, required=True, nullable=False)
    rp.add_argument("desc", type=unicode, required=True, nullable=False)
    rp.add_argument("filterRule", type=json_dict(["type", "regex", "where"]),
                    action="append")
    rp.add_argument("pocs", type=int, required=True, nullable=False, action="append")
    return rp.parse_args() if return_parse_args else rp


class TasksResource(Resource):
    @swag_from(get_request_parser_doc_dist("Task列表", ["TASK"], page_args(False)))
    @need_sign()
    def get(self):
        args = page_args()
        tasks, total = get_tasks_page(args.pageSkip, args.pageTake)
        return PageResponse([{
            "id": task.task_id,
            "desc": task.task_desc,
            "status": task.task_status,
            "creator": task.task_creator,
            "createTime": time_helper.datetime_to_strtime(task.create_time, "%Y-%m-%d %H:%M:%S")
        } for task in tasks], total)

    @swag_from(get_request_parser_doc_dist("创建任务", ["TASK"], post_args(False)))
    @need_sign()
    def post(self):
        args = post_args()
        task = create_task(args.desc, args.dataSource, args.filterRule if args.filterRule else [], args.pocs)
        return ApiResponse({"taskID": task.task_id})


class TaskResource(Resource):
    @swag_from(get_request_parser_doc_dist("Task详情", ["TASK"]))
    @need_sign()
    def get(self, task_id):
        task = get_task_detail(task_id)
        return ApiResponse(task) if task else ApiResponse(status=ResposeStatus.NotFound)

    @swag_from(get_request_parser_doc_dist("Task开始扫描", ["TASK"]))
    @need_sign()
    def post(self, task_id):
        start_scan_task(task_id)
        return ApiResponse()

    @swag_from(get_request_parser_doc_dist("Task取消任务", ["TASK"]))
    @need_sign()
    def delete(self, task_id):
        cancel_task(task_id)
        return ApiResponse()


api.add_resource(TasksResource, "/tasks")
api.add_resource(TaskResource, "/task/<task_id>")
