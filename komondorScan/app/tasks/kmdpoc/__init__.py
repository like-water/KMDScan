# -*- coding: utf-8 -*-
from .common import StringImporter
import os
import sys

KMDPOC_DIR = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir))
sys.path.append(KMDPOC_DIR)


class KmdPoc(object):
    def __init__(self, poc_context):
        self.poc_context = poc_context
        self.poc_model = StringImporter("Poc", self.poc_context).load_module()
        self.poc_class = self.poc_model.Poc

    def execute(self,
                url="",
                method="GET",
                header=None,
                data=None,
                request_detail=None):
        return self.poc_class(url, method, header, data,
                              request_detail).execute()

    @staticmethod
    def ClearPoc():
        if sys.modules.has_key("Poc"):
            del sys.modules["Poc"]