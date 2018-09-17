# -*- coding: utf-8 -*-
class BaseDataSource(object):
    def __init__(self, task_id):
        self.task_id = task_id

    def create(self):
        pass

    def release(self):
        pass
