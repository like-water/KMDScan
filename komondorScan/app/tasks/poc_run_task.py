# -*- coding: utf-8 -*-
from json import dumps, loads

from celery import group, chain
from redis import Redis

from app import celery, db
from config import Config
from . import SqlAlchemyTask
from .kmdpoc import KmdPoc
from ..models.poc import Poc
from ..models.task import Task, TaskPocRship, TaskStatus
from ..models.task_log import TaskLog, ResultCode
import re


def get_redis_conn():
    return Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, password=Config.REDIS_AUTH)


@celery.task(base=SqlAlchemyTask)
def assignment_task(task_id):
    task = Task.get_by_id(task_id)
    if task:
        poc_ids = db.session.query(TaskPocRship.poc_id).filter(TaskPocRship.task_id == task_id).all()
        print [poc_id[0] for poc_id in poc_ids]
        if poc_ids:
            pocs = db.session.query(Poc).filter(Poc.poc_id.in_([poc_id[0] for poc_id in poc_ids])).all()
            # 任务执行模式
            # if False:
            #     task_group = group([poc_run_all_request.s(task_id, {"poc_id": poc.poc_id, "poc": poc.poc}) for poc in
            #                         pocs])
            # else:
            #     redis = get_redis_conn()
            #     count = redis.llen(task_id)
            #     task_group = group(
            #         [request_run_all_poc.s(task_id, [{"poc_id": poc.poc_id, "poc": poc.poc} for poc in pocs],
            #                                loads(redis.lindex(task_id, index))) for index in
            #          range(count)])
            task_group = group(
                [poc_run_all_request.si(task_id,
                                        {"poc_id": poc.poc_id, "poc": poc.poc, "rule": loads(task.task_filter_rule)})
                 for poc in pocs])
            chain(task_group, task_finish.si(task_id))()


@celery.task(base=SqlAlchemyTask)
def task_finish(task_id):
    task = Task.get_by_id(task_id)
    task.task_status = TaskStatus.Finish
    task.save()
    redis = get_redis_conn()
    redis.delete(task_id)


@celery.task(base=SqlAlchemyTask)
def poc_run_all_request(task_id, poc):
    redis = get_redis_conn()
    count = redis.llen(task_id)
    KmdPoc.ClearPoc()
    for index in range(count):
        request = loads(redis.lindex(task_id, index))
        run_poc(task_id, poc.get("poc_id"), poc.get("poc"), request, poc.get("rule"))


@celery.task(base=SqlAlchemyTask)
def request_run_all_poc(task_id, pocs, request):
    for poc in pocs:
        KmdPoc.ClearPoc()
        run_poc(task_id, poc.get("poc_id"), poc.get("poc"), request, poc.get("rule"))


def run_poc(task_id, poc_id, poc, request, filter_rule):
    try:
        # Todo: 输入约定
        # Todo: 输入约定验证

        # Todo: 筛选规则过滤

        if task_rules_filter(filter_rule, request):

            url = "{0}://{1}{2}".format(request["scheme"],
                                        request["host"] if (request["scheme"] == "http" and request["port"] == 80) or (
                                            request["scheme"] == "https" and request[
                                                "port"] == 443) else "{0}:{1}".format(
                                            request["host"], request["port"]), request["path"])

            method = request["method"].upper()
            if method == "POST" or method == "PUT":
                data = request["form"]
            else:
                data = request["query"]

            # Todo： 输出约定
            rel_code, rel_info = KmdPoc(poc).execute(url=url, method=request["method"], header=request["headers"],
                                                     data=data,
                                                     request_detail=request)
            # Todo: 输出约定验证

            if rel_code == ResultCode.Unnormal or rel_code == ResultCode.Error:
                log = TaskLog()
                log.task_id = task_id
                log.poc_id = poc_id
                log.result_code = rel_code
                log.result_detail = rel_info
                log.request_detail = dumps(request)
                log.save()

        return True
    except Exception, ex:
        print ex.message
        return False


def task_rules_filter(rules, request):
    for rule in rules:
        if "where" in rule and "regex" in rule and "type" in rule:
            where = str(request.get(rule.get("where")))
            rel = re.search(rule.get("regex"), where)
            if rel is not None and rule.get("type") == "blacklist":
                return False
            elif rel is None and rule.get("type") == "whitelist":
                return False
            else:
                continue
    return True
