from __future__ import annotations
from utils.observable import Observable
from threading import Thread
from datetime import datetime
from serial import Serial


class Messenger(Observable):
    def __init__(self):
        super().__init__()
        self.port: str = ""
        self.baudrate: int = 9600
        self.serial: Serial = None
        self.is_open: bool = False
        self._history: list[tuple[str, str, bool]] = []
        self._listen_serial_thread: Thread = None

    def open(self, port: str, baudrate: int):
        if self.is_open:
            self.close()
        self.port = port
        self.baudrate = baudrate
        self.serial = Serial(port=port, baudrate=baudrate, timeout=1.0)
        self.is_open = True
        self.start_listen_serial()

    def close(self):
        if not self.is_open:
            return
        self.is_open = False
        self.stop_listen_serial()
        self.serial.close()
        self.clear_history()

    def clear_history(self):
        self._history = []

    def send(self, msg: str):
        self.history = (f"{msg}\n", True)
        self.serial.write(msg.encode())

    def recieve(self) -> str:
        return self.serial.readline().decode()

    def start_listen_serial(self):
        self._listen_serial_thread = Thread(target=self._listen_serial)
        self._listen_serial_thread.start()

    def stop_listen_serial(self):
        self.is_open = False
        self._listen_serial_thread.join(1)

    def _listen_serial(self):
        while self.is_open:
            if self.serial.in_waiting > 0:
                try:
                    self.history = (self.recieve(), False)
                except UnicodeDecodeError:
                    self.history = "Unicode Decode Error. Probably wrong baudrate.\n"
                    return

    @property
    def history(self) -> list[tuple[str, str, bool]]:
        return self._history

    @property
    def history_last(self) -> tuple[str, str, bool] | None:
        return self._history[-1] if len(self._history) > 0 else None

    @history.setter
    def history(self, msg: tuple[str, bool]):
        current_time: str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self._history.append((current_time, msg[0], msg[1]))
        self._history = self._history[-300:]
        self.notify(self._history[-1])
