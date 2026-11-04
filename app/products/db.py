import os
from flask import current_app
from tinydb import TinyDB


def _db():
    path = current_app.config["PRODUCTS_DB"]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return TinyDB(path, indent=2, ensure_ascii=False, encoding="utf-8")


def _with_id(doc):
    return dict(doc, id=doc.doc_id) if doc else None


def all_products():
    with _db() as db:
        return [_with_id(d) for d in db.table("products").all()]


def get_product(pid):
    with _db() as db:
        return _with_id(db.table("products").get(doc_id=pid))


def add_product(data):
    with _db() as db:
        return db.table("products").insert(data)


def update_product(pid, data):
    with _db() as db:
        db.table("products").update(data, doc_ids=[pid])


def delete_product(pid):
    with _db() as db:
        db.table("products").remove(doc_ids=[pid])