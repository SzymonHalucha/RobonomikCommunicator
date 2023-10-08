from __future__ import annotations
from typing import Callable
import Utility.logger as logger
import socket


def get_connect(func: Callable, host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> Callable | None:
    def wrapper(*args, **kwargs):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrapper


@logger.trace_class
class Database:
    def __init__(self):
        self.name: str = "Firebase"
        self.url: str = ""
        self.user_data: str = ""
        self.firebase = None

    @get_connect
    def get_data_from_collection(self, collection_name: str) -> dict | None:
        try:
            data = self.firebase.get(self.url, collection_name)
            return data
        except Exception:
            return None
