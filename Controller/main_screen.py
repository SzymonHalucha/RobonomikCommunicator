from View.MainScreen.main_screen import MainScreenView

if __debug__:
    import importlib
    import View.MainScreen.main_screen
    importlib.reload(View.MainScreen.main_screen)


class MainScreenController:
    def __init__(self, model):
        self.model = model
        self.view = MainScreenView(controller=self, model=self.model)

    def get_view(self) -> "MainScreenView":
        return self.view
