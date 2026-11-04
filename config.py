import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "hfj132kslad")
    PRODUCTS_DB = os.path.join(BASE_DIR, "data", "products.json")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024