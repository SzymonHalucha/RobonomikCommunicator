class Observable:
    def __init__(self):
        self._observers: "list" = []

    def notify(self, subject):
        for observer in self._observers:
            observer(subject)

    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
