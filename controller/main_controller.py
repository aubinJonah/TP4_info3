from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QColorDialog

from model.model import Model
from view.Dock_view import DockWindow
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
    __dock: DockWindow


    def __init__(self, view, model, canvas, physique, graph_view,dock):
        self.__view = view
        self.__model = model
        self.__canvas = canvas
        self.__physique = physique
        self.__graph_view = graph_view
        self.__dock = dock
        self.worker = Worker()

        self.__view.layout.addWidget(self.__physique)
        self.__graph_view.add_canvas(self.__canvas)

        self.__view.action_ajouter.triggered.connect(self.ajouter_graphique)
        self.__graph_view.VitesseButton.clicked.connect(self.lancer_thread)
        #Bouton de gestion de la simulation
        self.__view.StartpushButton.clicked.connect(self.gestion_commencer)
        self.__view.PausepushButton.clicked.connect(self.gestion_pause)
        self.__view.RedemarrerpushButton.clicked.connect(self.gestion_redemarrer)

        #mettre a jour compteur de vitesse
        self.__physique.vitesse_signal.connect(self.__view.update_compteur_vitesse)

        #boutons pour changer les caractéristiques de la voiture
        self.__view.actionCarac.triggered.connect(self.ouvrir_carac)
        self.__view.actionCouleur.triggered.connect(self.changement_de_couleur)

        #caractéristiques voiture
        self.__dock.SurfacecomboBox.currentIndexChanged.connect(self.update_carac)
        self.__dock.PoidshorizontalSlider.valueChanged.connect(self.update_carac)
        self.__dock.PuissancehorizontalSlider.valueChanged.connect(self.update_carac)

    def update_carac(self):
        poid = self.__dock.PoidshorizontalSlider.value()
        surface = self.__dock.SurfacecomboBox.currentIndex()
        puissance = self.__dock.PuissancehorizontalSlider.value()
        self.__physique.update_carac(poid, surface, puissance)

    def changement_de_couleur(self):
        couleur = QColorDialog.getColor(self.__physique.couleur, self.__view, "Choisir la couleur de la voiture")
        self.__physique.couleur = couleur
        self.__physique.update()

    def ouvrir_carac(self):
        self.__dock.show()

    def gestion_commencer(self):
        self.__view.StartpushButton.setEnabled(False)
        self.__view.PausepushButton.setEnabled(True)
        self.__view.RedemarrerpushButton.setEnabled(True)
        self.__physique.mettre_en_pause()

    def gestion_pause(self):
        self.__view.StartpushButton.setEnabled(True)
        self.__view.PausepushButton.setEnabled(False)
        self.__view.RedemarrerpushButton.setEnabled(True)
        self.__physique.mettre_en_pause()

    def gestion_redemarrer(self):
        self.__view.StartpushButton.setEnabled(True)
        self.__view.PausepushButton.setEnabled(False)
        self.__view.RedemarrerpushButton.setEnabled(False)
        self.__physique.redemarrer_simulation()

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
