from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QPushButton
from typing import TYPE_CHECKING

from PyQt6.uic import loadUi

if TYPE_CHECKING:
    from controller.main_controller import MainController


class GraphView(QMainWindow):
    layout: QVBoxLayout
    VitesseButton:QPushButton
    AccelerationButton:QPushButton
    ForceButton:QPushButton
    def __init__(self):
        super().__init__()
        if TYPE_CHECKING:
            self.__controller: MainController | None = None
        loadUi("view/ui/graph.ui",self)

    def set_controller(self, controller):
        self.__controller = controller

    def add_canvas(self, canvas):
        self.layout.insertWidget(0,canvas)
