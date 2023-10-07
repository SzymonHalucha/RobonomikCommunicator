from inspect import isfunction
from functools import wraps
from typing import Callable
import logging
import time
import sys
import os


def init():
    file_handler = logging.FileHandler(filename=os.path.abspath("./app.log"), mode="w", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s"))
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger = logging.getLogger("Communicator")
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


_logger = None
# _logger = init()


def trace_class(cls):
    def initialize(self, *args, **kwargs):
        cls_init(self, *args, **kwargs)

    def get_class_methods(cls):
        return ((method_name, getattr(cls, method_name)) for method_name in dir(cls) if isfunction(getattr(cls, method_name)))

    def trace_method(cls, name: "str", func: "Callable"):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log = f"Class \"{cls.__name__}\" calling method \"{name}\"."
            _logger.debug(log)
            return func(*args, **kwargs)
        return wrapper

    if _logger is None:
        return cls
    cls_init = cls.__init__
    cls.__init__ = initialize
    for (name, func) in get_class_methods(cls):
        if isfunction(func) and func.__module__ == cls.__module__:
            setattr(cls, name, trace_method(cls, name, func))
    return cls


def calculate_time(func):
    if _logger is None:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        result = func(*args, **kwargs)
        cls_name = args[0].__class__.__name__
        func_name = func.__name__
        ms = "{0:.2f}".format((time.time_ns() - start) / 1000_000)
        _logger.info(f"Class \"{cls_name}\" calling method \"{func_name}\" took {ms} miliseconds to execute.")
        return result
    return wrapper
