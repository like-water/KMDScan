# -*- coding: utf-8 -*-
from app import db
from .data_source import DataSourceFactory
from ..models.task import Task, TaskStatus, TaskPocRship
from json import dumps, loads
from ..tasks.poc_run_task import assignment_task
from ..models.poc import Poc
from ..common import time_helper
from redis import Redis
from config import Config


def get_redis_conn():
    return Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, password=Config.REDIS_AUTH)


def create_task(desc, data_source, filter_rule, pocs):
    task = Task()
    task.task_data_source = data_source
    task.task_desc = desc
    task.task_filter_rule = dumps(filter_rule)
    task.task_status = TaskStatus.Init
    task.save()

    task_bind_poc(task.task_id, pocs)

    try:
        data_source_info = DataSourceFactory(task.task_data_source, task.task_id).create()
        task.task_data_source_info = dumps(data_source_info)
        task.task_status = TaskStatus.Collecting
    except Exception, ex:
        task.task_status = TaskStatus.InitFail
        print ex.message
        redis = get_redis_conn()
        redis.delete(task.task_id)
    finally:
        task.save()
    return task


def cancel_task(task_id):
    task = Task.get_by_id(task_id)
    if task and task.task_status == TaskStatus.Collecting:
        DataSourceFactory(task.task_data_source, task.task_id).release()
        task.task_status = TaskStatus.Cancel
        task.save()
        redis = get_redis_conn()
        redis.delete(task_id)


def start_scan_task(task_id):
    task = Task.get_by_id(task_id)
    if task and task.task_status == TaskStatus.Collecting:
        DataSourceFactory(task.task_data_source, task.task_id).release()
        task.task_status = TaskStatus.Scanning
        task.save()
        assignment_task.delay(task.task_id)


def task_bind_poc(task_id, poc_ids):
    for poc_id in poc_ids:
        rship = TaskPocRship()
        rship.task_id = task_id
        rship.poc_id = poc_id
        rship.save(auto_commit=False)
    db.session.commit()


def get_tasks_page(skip=0, take=10):
    query = db.session.query(Task)
    count_query = db.session.query(db.func.count(Task.task_id))
    rel = query.order_by(Task.task_id.desc()).offset(skip).limit(take).all()
    total_count = count_query.first()[0]
    return rel, total_count


def get_task_detail(task_id):
    task = Task.get_by_id(task_id)
    if task:
        pocs = db.session.query(Poc.poc_id, Poc.bug_name).join(TaskPocRship, TaskPocRship.poc_id == Poc.poc_id).filter(
            TaskPocRship.task_id == task_id).all()

        return {
            "taskID": task.task_id,
            "status": task.task_status,
            "dataSource": task.task_data_source,
            "dataSourceInfo": loads(task.task_data_source_info) if task.task_data_source_info else "",
            "desc": task.task_desc,
            "createTime": time_helper.datetime_to_strtime(task.create_time, "%Y-%m-%d %H:%M:%S"),
            "filterRule": loads(task.task_filter_rule) if task.task_filter_rule else "",
            "pocs": [{
                "id": poc.poc_id,
                "bugName": poc.bug_name
            } for poc in pocs]
        }
    return None
