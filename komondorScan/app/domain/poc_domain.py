# -*- coding: utf-8 -*-
from app import db
from ..models.poc import Poc


def get_pocs_page(skip=0, take=10):
    query = db.session.query(Poc.poc_id, Poc.author, Poc.bug_name, Poc.bug_grade, Poc.poc_desc)
    count_query = db.session.query(db.func.count(Poc.poc_id))
    rel = query.filter(Poc.is_del == False).order_by(Poc.poc_id.desc()).offset(skip).limit(take).all()
    total_count = count_query.filter(Poc.is_del == False).first()[0]
    return [{
        "id": poc.poc_id,
        "author": poc.author,
        "bugName": poc.bug_name,
        "bugGrade": poc.bug_grade,
        "pocDesc": poc.poc_desc
    } for poc in rel], total_count


def get_pocs_simple_list():
    rel = db.session.query(Poc.poc_id, Poc.bug_name, Poc.bug_grade).all()
    return [{
        "id": poc.poc_id,
        "bugName": poc.bug_name,
        "bugGrade": poc.bug_grade,
    } for poc in rel]
