# -*- coding: utf-8 -*-
from app import db


class LogValidity(object):
    Unknown = 0
    Validity = 1
    Invalidity = 2


class ResultCode(object):
    Normal = 0
    Unnormal = 1
    Error = 2


class TaskLog(db.Model):
    __tablename__ = "kmd_task_log"
    log_id = db.Column(db.BigInteger, primary_key=True)
    task_id = db.Column(db.BigInteger)
    poc_id = db.Column(db.BigInteger)
    request_detail = db.Column(db.String, default="")
    result_code = db.Column(db.Integer, default=ResultCode.Unnormal)
    result_detail = db.Column(db.String, default="")
    validity = db.Column(db.Integer, default=LogValidity.Unknown)
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()
