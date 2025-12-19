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

    est_Vitesse = False
    est_Acceleration = False

    def __init__(self, view, model, canvas, physique, graph_view, dock):
        self.__view = view
        self.__model = model
        self.__canvas = canvas
        self.__physique = physique
        self.__graph_view = graph_view
        self.temps = 0
        self.__dock = dock

        self.__view.layout.addWidget(self.__physique)
        self.__graph_view.add_canvas(self.__canvas)

        self.__view.action_ajouter.triggered.connect(self.ajouter_graphique)

        # Bouton de gestion de la simulation
        self.__view.StartpushButton.clicked.connect(self.gestion_commencer)
        self.__view.PausepushButton.clicked.connect(self.gestion_pause)
        self.__view.RedemarrerpushButton.clicked.connect(self.gestion_redemarrer)

        # Bouton des choix de graphes
        self.__graph_view.VitesseButton.clicked.connect(self.graphVitesse)
        self.__graph_view.AccelerationButton.clicked.connect(self.graphAcceleration)

        # mettre a jour compteur de vitesse
        self.__physique.vitesse_signal.connect(self.changement_vitesse)

        # boutons pour changer les caractéristiques de la voiture
        self.__view.actionCarac.triggered.connect(self.ouvrir_carac)
        self.__view.actionCouleur.triggered.connect(self.changement_de_couleur)

        # caractéristiques voiture
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

        self.reset_graph()

    def changement_vitesse(self, vitesse):
        self.__view.update_compteur_vitesse(vitesse)
        self.gestion_donnees(vitesse)

    def gestion_donnees(self, donnees):
        donnees_a_ajouter = 0
        if self.est_Vitesse:
            donnees_a_ajouter = donnees
        elif self.est_Acceleration:
            if self.__canvas.temps == []:
                pass
            else:
                donnees_a_ajouter = donnees / self.__canvas.temps[len(self.__canvas.temps) - 1]
        self.ajouter_donnees(donnees_a_ajouter)
        self.__canvas.line.set_xdata(self.__canvas.temps)
        self.__canvas.line.set_ydata(self.__canvas.donnees)
        self.__canvas.ax.set_xlim(min(self.__canvas.temps), max(self.__canvas.temps))
        self.__canvas.draw()
        self.__canvas.flush_events()
        sleep(0.017)

    def ajouter_donnees(self, donnee_a_ajouter):
        self.temps += 0.017
        self.__canvas.temps.append(self.temps)
        self.__canvas.donnees.append(donnee_a_ajouter)
        if len(self.__canvas.temps) > 100:
            self.__canvas.temps[:] = self.__canvas.temps[1:]
            self.__canvas.donnees[:] = self.__canvas.donnees[1:]

    def ajouter_graphique(self):
        self.__graph_view.show()

    def reset_graph(self):
        self.temps = 0
        self.__canvas.temps.clear()
        self.__canvas.donnees.clear()
        self.__canvas.line, = self.__canvas.ax.plot(self.__canvas.temps, self.__canvas.donnees, "r")
        self.__canvas.ax.clear()
        self.__canvas.draw_graph()

    def graphVitesse(self):
        self.reset_graph()
        self.est_Vitesse = True
        self.est_Acceleration = False
        self.__graph_view.VitesseButton.setEnabled(False)
        self.__graph_view.AccelerationButton.setEnabled(True)

    def graphAcceleration(self):
        self.reset_graph()
        self.est_Vitesse = False
        self.est_Acceleration = True
        self.__graph_view.VitesseButton.setEnabled(True)
        self.__graph_view.AccelerationButton.setEnabled(False)
