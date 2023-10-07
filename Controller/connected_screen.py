from View.ConnectedScreen.connected_screen import ConnectedScreenView

if __debug__:
    import importlib
    import View.ConnectedScreen.connected_screen
    importlib.reload(View.ConnectedScreen.connected_screen)


class ConnectedScreenController:
    def __init__(self, model):
        self.model = model
        self.view = ConnectedScreenView(controller=self, model=self.model)

    def get_view(self) -> "ConnectedScreenView":
        return self.view
