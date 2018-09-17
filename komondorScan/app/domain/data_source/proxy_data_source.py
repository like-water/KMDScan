# -*- coding: utf-8 -*-
from ..supervisorman_domain import create_service, release_service
from .base_data_source import BaseDataSource
import random
from ...common.get_port_help import find_port, get_local_ip
from config import Config


class ProxyDataSource(BaseDataSource):
    def create(self):
        name = "proxy" + self.task_id.__str__()
        proxy_port, web_port = find_port(random.randint(10000, 20000), 2)
        command = Config.DATA_SOURCE_PROXY_TEMPLATE.format(proxy_port=proxy_port, web_port=web_port)
        create_service(name, command, {
            "TASKID": self.task_id
        })
        return {
            "ip": get_local_ip(),
            "proxy": proxy_port,
            "web": web_port
        }

    def release(self):
        name = "proxy" + self.task_id.__str__()
        release_service(name)
