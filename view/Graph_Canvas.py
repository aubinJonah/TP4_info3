import networkx as nx
import numpy as np
from PyQt6.QtCore import Qt

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from networkx import NetworkXError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.main_controller import MainController


class GraphCanvas(FigureCanvasQTAgg):
    borne_inf = 0
    borne_sup = 10
    donnees = [0]
    temps = [0.017]

    def __init__(self):
        plt.ion()
        # Crée une figure matplotlib
        self.fig, self.ax = plt.subplots(figsize=(20, 10))
        self.line, = self.ax.plot(self.temps, self.donnees, "r")
        self.ax.set_ylim(0, 250)
        super().__init__(self.fig)
        if TYPE_CHECKING:
            self.__controller: MainController | None = None
        # Permet de faire fonctionner l'ecoute des touches dans un canvas
        self.setFocus()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_controller(self, controller):
        self.__controller = controller

    def draw_graph(self):
        self.ax.clear()
        # Trace la fonction
        x = np.linspace(self.borne_inf, self.borne_sup, 100)
        y = np.sin(x)
        # self.ax.plot(x, y)

        self.draw()

    def draw_vitesse(self, vitesse):
        self.line, = self.ax.plot(self.temps, vitesse, "r")

        self.ax.clear()
        # Trace la fonction
        #x = np.linspace(self.borne_inf, self.borne_sup, 1)
        #y = vitesse
        #self.ax.plot(x, y)

        while True:
            self.__controller.ajouter_donnees()
            self.line.set_xdata(self.temps)
            self.line.set_ydata(self.donnees)
            self.ax.set_xlim(min(self.temps),max(self.temps))
            self.ax.set_ylim(min(self.donnees), max(self.donnees))
            self.draw()
            self.flush_events()
            self.sleep(0.0002)

        self.draw()
