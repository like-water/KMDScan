# -*- coding: utf-8 -*-
from ..common import RequestsDomain
from config import Config


@RequestsDomain.post(Config.SUPERVISORMAN_HOST, "api/processes")
def create_service(name, command, env={}):
    return {
        "name": name,
        "command": command,
        "env": env
    }


@RequestsDomain.delete(Config.SUPERVISORMAN_HOST, "api/process/%s")
def release_service(name):
    return {}, name
