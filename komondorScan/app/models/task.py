# -*- coding: utf-8 -*-
from app import db


class TaskStatus(object):
    Init = 0
    Collecting = 1
    Finish = 2
    InitFail = 3
    Cancel = 4
    Scanning = 5


class TaskPocRship(db.Model):
    __tablename__ = "kmd_task_poc_rship"
    task_id = db.Column(db.BigInteger, primary_key=True)
    poc_id = db.Column(db.BigInteger, primary_key=True)

    def save(self, auto_commit=True):
        db.session.add(self)
        if auto_commit:
            db.session.commit()
        else:
            db.session.flush()


class Task(db.Model):
    __tablename__ = "kmd_task"
    task_id = db.Column(db.BigInteger, primary_key=True)
    task_desc = db.Column(db.String(500), default="")
    task_data_source = db.Column(db.String(50), default="")
    task_data_source_info = db.Column(db.String, default="")
    task_filter_rule = db.Column(db.String, default="")
    task_status = db.Column(db.Integer, default=TaskStatus.Init)
    task_creator = db.Column(db.String(32),default="")
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def save(self, auto_commit=True):
        db.session.add(self)

        if auto_commit:
            db.session.commit()
        else:
            db.session.flush()

    @staticmethod
    def get_by_id(task_id):
        return db.session.query(Task).filter(Task.task_id == task_id).first()
