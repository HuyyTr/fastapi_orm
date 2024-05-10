from fastapi import FastAPI

from .config import settings

from typing import Dict, Any
import importlib


def init_middleware(app: FastAPI):
    for middleware in settings.middlware.MIDDLEWARE:
        try:
            add_middleware(app, middleware)
        except Exception as e:
            print(f"Error adding middleware. {e}")


def add_middleware(app: FastAPI, middleware: Dict[str, Any]) -> None:
    middleware_module = '.'.join(middleware["type"].split(".")[0:-1])
    middleware_class = middleware["type"].split(".")[-1]
    middleware_instance = create_instance(
        middleware_module, middleware_class)
    app.add_middleware(middleware_instance, **middleware["params"])


def create_instance(module_name, class_name):
    module = importlib.import_module(module_name)
    instance_class = getattr(module, class_name)
    return instance_class
