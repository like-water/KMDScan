# -*- coding: utf-8 -*-
from app import db
from ..models.poc import Poc
from ..models.task_log import TaskLog


def get_log_page_by_task(task_id, skip, take, result_code=""):
    query = db.session.query(TaskLog, Poc.bug_name, Poc.bug_grade) \
        .join(Poc, Poc.poc_id == TaskLog.poc_id).filter(TaskLog.task_id == task_id)
    count_query = db.session.query(db.func.count(TaskLog.task_id)).filter(TaskLog.task_id == task_id)

    if result_code:
        query = query.filter(TaskLog.result_code == result_code)
        count_query = count_query.filter(TaskLog.result_code == result_code)

    rel = query.order_by(Poc.bug_grade.desc(), Poc.poc_id.desc()).offset(skip).limit(take).all()
    total = count_query.first()[0]
    return [{
        "id": item.TaskLog.log_id,
        "poc": {
            "id": item.TaskLog.poc_id,
            "bugName": item.bug_name,
            "grade": item.bug_grade
        },
        "requestDetail": item.TaskLog.request_detail,
        "resultDetail": item.TaskLog.result_detail,
        "code": item.TaskLog.result_code,
        "validity": item.TaskLog.validity
    } for item in rel], total
