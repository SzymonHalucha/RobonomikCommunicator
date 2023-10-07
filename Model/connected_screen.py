from Model.base_model import BaseScreenModel
import multitasking

multitasking.set_max_threads(10)


class ConnectedScreenModel(BaseScreenModel):
    def __init__(self, database):
        super().__init__()
        self._data = None
        self._database = database

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.notify("ConnectedScreen")

    @multitasking.task
    def get_data(self):
        self.data = {"data": "data"}
