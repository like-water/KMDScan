#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import api
from flask_restful import Resource, reqparse
from ..common.ApiResponse import ApiResponse
from ..common.alopex_auth_sdk import AccessTokenModel


def post_args():
    rp = reqparse.RequestParser()
    rp.add_argument("accesstoken", type=unicode, required=True, nullable=False)
    return rp.parse_args()


class UserInfo(Resource):
    def post(self):
        args = post_args()
        rel = AccessTokenModel.token2cls(args.accesstoken)
        return ApiResponse(rel.user if rel else rel)

api.add_resource(UserInfo,'/userinfo')