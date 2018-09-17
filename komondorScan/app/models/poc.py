# -*- coding: utf-8 -*-
from app import db


class BugGrade(object):
    Low = 1
    Middle = 2
    High = 3


class Poc(db.Model):
    __tablename__ = "kmd_poc"
    poc_id = db.Column(db.BigInteger, primary_key=True)
    bug_name = db.Column(db.String(255), default="")
    poc_desc = db.Column(db.String, default="")
    poc = db.Column(db.String, default="")
    bug_grade = db.Column(db.Integer, default=BugGrade.Low)
    author = db.Column(db.String(32), default="")
    create_time = db.Column(db.TIMESTAMP, server_default=db.func.now())
    is_del = db.Column(db.Boolean, default=False)

    def save(self):
        if self.poc_id:
            db.session.query(Poc).filter(Poc.poc_id == self.poc_id).update({
                Poc.bug_name: self.bug_name,
                Poc.poc_desc: self.poc_desc,
                Poc.poc: self.poc,
                Poc.bug_grade: self.bug_grade
            })
        else:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(poc_id):
        return db.session.query(Poc).filter(Poc.poc_id == poc_id).first()

    @staticmethod
    def delete(poc_id):
        db.session.query(Poc).filter(Poc.poc_id == poc_id).update({Poc.is_del: True})
        db.session.commit()

