import math

import pymunk
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QBrush, QPainter
from PyQt6.QtWidgets import QWidget
from pymunk import Vec2d


class PhysiqueQtWidget(QWidget):

    info_graph = pyqtSignal(int,int,int)
    def __init__(self):
        super().__init__()
        #permet de faire que les touche sont enregistrer meme si on n'a pas cliqué sur la simulation
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.W, self.H = 600, 400
        self.Up_Key = False
        self.Down_Key = False
        self.Left_Key = False
        self.Right_Key = False

        self.setFixedSize(self.W, self.H)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)
        self.init_simulation()

    def init_simulation(self):

        # Espace
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        # le mur
        mur_y = 375
        largeur = 25
        mur = pymunk.Segment(self.space.static_body,(0, mur_y),(self.W, mur_y),largeur)
        mur.elasticity = 0
        mur.friction = 1.0
        self.space.add(mur)
        # la voiture
        mass = 1
        self.size = (100,50)
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, self.size))
        self.body.position = (300, 200)
        self.angle = -math.degrees(self.body.angle)
        shape = pymunk.Poly.create_box(self.body,self.size)
        shape.elasticity = 0.8
        self.space.add(self.body, shape)


    def update_simulation(self):
        dt = 1 / 60

        self.space.step(dt)
        #limite la vitesse de la voiture
        vitesse_max = 200
        if self.body.velocity.length > vitesse_max:
            self.body.velocity = self.body.velocity.normalized() * vitesse_max
        #simule la friction de l'air sur la voiture et diminiue la vitesse de celle-ci pour chaque mise à jour
        self.body.velocity *= 0.95
        self.body.angular_velocity *= 0.90
        self.update_voiture()
        self.envoyer_signal_graph()
        self.update()

    def envoyer_signal_graph(self):
        vitesse = self.body.velocity.length
        self.info_graph.emit(self.body.position.x,self.body.postion.y,vitesse)
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # dessine le mur
        p.setBrush(Qt.GlobalColor.gray)
        y_mur = (self.H - 375) - (50 / 2)
        p.drawRect(0,int(y_mur),self.W,50)
        # dessine la voiture
        p.save()
        #on centre le canvas sur la voiture
        p.translate(self.body.position.x,self.H - self.body.position.y)
        #on transforme l'angle en degree pour la simulation et faire tourner l'image de la voiture
        self.angle = -math.degrees(self.body.angle)
        p.rotate(self.angle)


        largeur, hauteur = self.size
        p.setBrush(Qt.GlobalColor.red)
        p.drawRect(int(-largeur/2), int(-hauteur/2),self.size[0],self.size[1])

        p.setBrush(Qt.GlobalColor.yellow)
        p.drawRect(int(largeur / 2 - 10), int(-hauteur / 2), 10, 10)
        p.setBrush(Qt.GlobalColor.yellow)
        p.drawRect(int(largeur / 2 - 10), int(-(hauteur-80) / 2), 10, 10)

        p.setPen(Qt.GlobalColor.green)

        p.restore()

    def update_voiture(self):
        vitesse = self.body.velocity.length
        tourner = vitesse > 10

        if self.Up_Key:
            self.moveCar("forward")
        if self.Down_Key:
            self.moveCar("backward")

        if tourner:
            if self.Left_Key:
                self.rotate_car("left")
            if self.Right_Key:
                self.rotate_car("right")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.Up_Key = True
        if event.key() == Qt.Key.Key_Down:
            self.Down_Key = True
        if event.key() == Qt.Key.Key_Left:
            self.Left_Key = True
        if event.key() == Qt.Key.Key_Right:
            self.Right_Key = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.Up_Key = False
        if event.key() == Qt.Key.Key_Down:
            self.Down_Key = False
        if event.key() == Qt.Key.Key_Left:
            self.Left_Key = False
        if event.key() == Qt.Key.Key_Right:
            self.Right_Key = False

    def moveCar(self,sens):

        vitesse = 20

        if sens == "forward":
            self.body.apply_impulse_at_local_point((vitesse,0), (0, 0))
        else:
            self.body.apply_impulse_at_local_point((-(vitesse/2),0), (0, 0))

    def rotate_car(self,sens):
        vitesse_rotation = 2.0
        if sens == "left":
            self.body.angular_velocity = vitesse_rotation
        if sens == "right":
            self.body.angular_velocity = -vitesse_rotation