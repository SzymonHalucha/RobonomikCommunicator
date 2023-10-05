class Observer:
    def __init__(self):
        self._observers: "list" = []

    def notify(self, subject):
        for observer in self._observers:
            observer(subject)

    def subscribe(self, subject):
        if subject not in self._observers:
            self._observers.append(subject)

    def unsubscribe(self, subject):
        if subject in self._observers:
            self._observers.remove(subject)
