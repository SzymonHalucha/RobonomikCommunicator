from Model.main_screen import MainScreenModel
from Controller.main_screen import MainScreenController
from Model.connected_screen import ConnectedScreenModel
from Controller.connected_screen import ConnectedScreenController

screens = {
    "MainScreen": {
        "model": MainScreenModel,
        "controller": MainScreenController,
    },
    "ConnectedScreen": {
        "model": ConnectedScreenModel,
        "controller": ConnectedScreenController,
    },
}
