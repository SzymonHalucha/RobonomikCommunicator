from Utility.observer import Observer


class BaseScreenModel(Observer):
    def __init__(self):
        super().__init__()

    def notify(self, screen_name: "str"):
        for observer in self._observers:
            if observer.name == screen_name:
                observer()
