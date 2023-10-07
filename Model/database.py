import socket


def get_connect(func, host="8.8.8.8", port=53, timeout=3):
    def wrapper(*args, **kwargs):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrapper


class Database:
    def __init__(self):
        self.name = "Firebase"
        self.url = ""
        self.user_data = ""
        self.firebase = None

    @get_connect
    def get_data_from_collection(self, collection_name: str) -> "dict | None":
        try:
            data = self.firebase.get(self.url, collection_name)
            return data
        except Exception:
            return None
