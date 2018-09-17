# -*- coding: utf-8 -*-
from proxy_data_source import ProxyDataSource


class DataSourceFactory(object):
    def __init__(self, source_type, task_id):
        self.source_type = source_type

        if source_type == "proxy":
            self.data_source = ProxyDataSource(task_id)
        else:
            raise Exception("未知数据源")

    def create(self):
        return self.data_source.create()

    def release(self):
        self.data_source.release()
