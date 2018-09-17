# -*- coding: utf-8 -*-
from flasgger import swag_from
from flask_restful import Resource, reqparse, inputs

from . import api
from ..common import time_helper
from ..common.ApiResponse import ApiResponse, PageResponse
from ..common.AuthenticateDecorator import need_sign,need_power
from ..common.RequestInputs import int_min
from ..common.api_doc_helper import get_request_parser_doc_dist
from ..domain.poc_domain import get_pocs_page, get_pocs_simple_list
from ..models.poc import Poc


def page_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("pageSkip", type=int_min(0), default=0)
    rp.add_argument("pageTake", type=int_min(1), default=10)
    return rp.parse_args() if return_parse_args else rp


def post_args(return_parse_args=True):
    rp = reqparse.RequestParser()
    rp.add_argument("bugName", type=unicode, required=True, nullable=False)
    rp.add_argument("desc", type=unicode, required=True, nullable=False)
    rp.add_argument("poc", type=unicode, required=True, nullable=False)
    rp.add_argument("grade", type=inputs.int_range(-1, 4), required=True, nullable=False)
    return rp.parse_args() if return_parse_args else rp


class PocsResource(Resource):
    @swag_from(get_request_parser_doc_dist("POC列表", ["POC"], page_args(False)))
    @need_sign()
    def get(self):
        args = page_args()
        page, total = get_pocs_page(args.pageSkip, args.pageTake)
        return PageResponse(page, total)

    @swag_from(get_request_parser_doc_dist("新增POC", ["POC"], post_args(False)))
    @need_power("WritePOC")
    def post(self):
        args = post_args()
        poc = Poc()
        poc.bug_name = args.bugName
        poc.poc = args.poc
        poc.poc_desc = args.desc
        poc.bug_grade = args.grade
        poc.save()
        return ApiResponse()


class PocResource(Resource):
    @swag_from(get_request_parser_doc_dist("POC详情", ["POC"]))
    @need_sign()
    def get(self, poc_id):
        poc = Poc.get_by_id(poc_id)
        return ApiResponse({
            "id": poc.poc_id,
            "bugName": poc.bug_name,
            "desc": poc.poc_desc,
            "poc": poc.poc,
            "grade": poc.bug_grade,
            "author": poc.author,
            "createTime": time_helper.datetime_to_strtime(poc.create_time, "%Y-%m-%d %H:%M:%S")
        })

    @swag_from(get_request_parser_doc_dist("编辑POC", ["POC"], post_args(False)))
    @need_power("WritePOC")
    def put(self, poc_id):
        args = post_args()
        poc = Poc()
        poc.poc_id = poc_id
        poc.bug_name = args.bugName
        poc.poc = args.poc
        poc.poc_desc = args.desc
        poc.bug_grade = args.grade
        poc.save()
        return ApiResponse()

    @swag_from(get_request_parser_doc_dist("删除POC", ["POC"]))
    @need_sign()
    def delete(self, poc_id):
        Poc.delete(poc_id)
        return ApiResponse()


class PocsSelectResource(Resource):
    @swag_from(get_request_parser_doc_dist("POC列表 For Select", ["POC", "SELECT"]))
    @need_sign()
    def get(self):
        rel = get_pocs_simple_list()
        return ApiResponse(rel)


api.add_resource(PocsResource, "/pocs")
api.add_resource(PocResource, "/poc/<poc_id>")
api.add_resource(PocsSelectResource, "/select/pocs")
