from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal, Qt
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
        self.worker = Worker(physique)
        self.temps = 0
        self.__dock = dock

        self.ouvrir_carac()


        self.__view.layout.addWidget(self.__physique)
        self.__graph_view.add_canvas(self.__canvas)

        self.__view.action_ajouter.triggered.connect(self.ajouter_graphique)
        self.__graph_view.VitesseButton.clicked.connect(self.lancer_thread)
        #Bouton de gestion de la simulation
        self.__view.StartpushButton.clicked.connect(self.gestion_commencer)
        self.__view.PausepushButton.clicked.connect(self.gestion_pause)
        self.__view.RedemarrerpushButton.clicked.connect(self.gestion_redemarrer)

        #mettre a jour compteur de vitesse
        self.__physique.vitesse_signal.connect(self.changement_vitesse)

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
        self.__view.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.__dock)
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

        self.__physique.info_graph.connect(self.update_graph)

    def changement_vitesse(self, vitesse):
        self.__view.update_compteur_vitesse(vitesse)

        self.ajouter_donnees(vitesse)
        self.__canvas.line.set_xdata(self.__canvas.temps)
        self.__canvas.line.set_ydata(self.__canvas.donnees)
        self.__canvas.ax.set_xlim(min(self.__canvas.temps), max(self.__canvas.temps))
        #self.__canvas.ax.set_ylim(min(self.__canvas.donnees), max(self.__canvas.donnees))
        self.__canvas.draw()
        self.__canvas.flush_events()
        sleep(0.0002)

    def ajouter_donnees(self, donnee_a_ajouter):
        self.temps += 0.017
        self.__canvas.temps.append(self.temps)
        self.__canvas.donnees.append(donnee_a_ajouter)
        if len(self.__canvas.temps) > 100:
            self.__canvas.temps[:] = self.__canvas.temps[1:]
            self.__canvas.donnees[:] = self.__canvas.donnees[1:]

    def ajouter_graphique(self):
        self.__graph_view.show()

    def lancer_thread(self):
        self.worker.temps_passer.connect(self.update_graph)
        self.worker.start()



class Worker(QThread):
    temps_passer = pyqtSignal(int)
    temps = 0
    en_cours: bool
    __physique: PhysiqueQtWidget

    def __init__(self, physique):
        super().__init__()
        self.__physique = physique

    def run(self):
        # TODO
        self.en_cours = True
        while self.en_cours:
            sleep(1)
            # self.temps += 1
            # self.temps_passer.emit(self.temps)
            self.__physique.envoyer_signal_graph()
