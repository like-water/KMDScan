#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restful import Api

api = Api(prefix='/api', catch_all_404s=True)

import user, task, poc, task_log
