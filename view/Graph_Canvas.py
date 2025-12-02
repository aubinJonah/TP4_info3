import networkx as nx
from PyQt6.QtCore import Qt

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from networkx import NetworkXError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.main_controller import MainController


class GraphCanvas(FigureCanvasQTAgg):
    def __init__(self):
        # Crée une figure matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        super().__init__(self.fig)
        self.draw_graphe()
        if TYPE_CHECKING:
            self.__controller: MainController | None = None
        # Permet de faire fonctionner l'ecoute des touches dans un canvas
        self.setFocus()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_controller(self, controller):
        self.__controller = controller


