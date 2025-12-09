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

    def __init__(self, view, model, canvas, physique,graph_view):
        self.__view = view
        self.__model = model
        self.__canvas = canvas
        self.__physique = physique
        self.__graph_view = graph_view


        self.__view.layout.addWidget(self.__physique)
        self.__graph_view.add_canvas(self.__canvas)

        self.__view.action_ajouter.triggered.connect(self.ajouter_graphique)

    def ajouter_graphique(self):
        self.__graph_view.show()
