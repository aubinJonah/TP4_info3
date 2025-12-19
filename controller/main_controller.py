from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from model.model import Model
from view.Graph_Canvas import GraphCanvas
from view.Graph_View import GraphView
from view.MainWindow import MainWindow
from view.PhysiqueWindow import PhysiqueQtWidget


class MainController:
    __view: MainWindow
    __model: Model
    __canvas: GraphCanvas
    __physique: PhysiqueQtWidget
    __graph_view: GraphView

    def __init__(self, view, model, canvas, physique, graph_view):
        self.__view = view
        self.__model = model
        self.__canvas = canvas
        self.__physique = physique
        self.__graph_view = graph_view
        self.worker = Worker()

        self.__view.layout.addWidget(self.__physique)
        self.__graph_view.add_canvas(self.__canvas)

        self.__view.action_ajouter.triggered.connect(self.ajouter_graphique)
        self.__graph_view.VitesseButton.clicked.connect(self.lancer_thread)

    def ajouter_graphique(self):
        self.__graph_view.show()

    def lancer_thread(self):
        self.worker.temps_passer.connect(self.update_graph)
        self.worker.start()

    def update_graph(self,temps):
        self.__canvas.borne_sup += 1
        self.__canvas.draw_vitesse()
        print(f"temps écoulé : {temps}")

class Worker(QThread):
    temps_passer = pyqtSignal(int)
    temps = 0
    en_cours :bool
    def run(self):
        # TODO
        self.en_cours = True
        while self.en_cours:
            sleep(1)
            self.temps += 1
            self.temps_passer.emit(self.temps)
