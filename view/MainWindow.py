from typing import TYPE_CHECKING

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QPushButton, QLabel
from PyQt6.uic import loadUi

if TYPE_CHECKING:
    from controller.main_controller import MainController  # uniquement pour


class MainWindow(QMainWindow):
    layout:QVBoxLayout
    action_ajouter:QAction
    StartpushButton: QPushButton
    PausepushButton: QPushButton
    RedemarrerpushButton: QPushButton
    CompteurVitesse:QLabel
    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        if TYPE_CHECKING:
            self.__controller: MainController | None = None
        loadUi("view/ui/physique.ui",self)

    def set_controller(self, controller):
        self.__controller = controller

    def update_compteur_vitesse(self,vitesse):
        self.CompteurVitesse.setText(f"Vitesse : {vitesse:.2f} px/s")
