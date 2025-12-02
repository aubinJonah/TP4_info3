from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QMainWindow, QGridLayout

if TYPE_CHECKING:
    from controller.main_controller import MainController  # uniquement pour


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        if TYPE_CHECKING:
            self.__controller: MainController | None = None

    def set_controller(self, controller):
        self.__controller = controller
