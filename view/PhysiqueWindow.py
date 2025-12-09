import math

import pymunk
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QBrush, QPainter
from PyQt6.QtWidgets import QWidget
from pymunk import Vec2d


class PhysiqueQtWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.W, self.H = 600, 400
        self.setFixedSize(self.W, self.H)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)
        self.init_simulation()

    def init_simulation(self):

        # Espace
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        # --- SOL -------------------------------------------------
        # Segment statique de (0, 50) à (600, 50)
        ground_y = 50
        ground = pymunk.Segment(self.space.static_body,
                            (0, ground_y),
                            (self.W, ground_y),
                            2)
        ground.elasticity = 0.8
        ground.friction = 1.0
        self.space.add(ground)
        # --- voiture -----------------------------------------------
        mass = 1
        self.size = (100,50)
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, self.size))
        self.body.position = (0, 100)
        self.angle = -math.degrees(self.body.angle)
        shape = pymunk.Poly.create_box(self.body)
        shape.elasticity = 0.8
        self.space.add(self.body, shape)


    def update_simulation(self):
        dt = 1 / 60

        self.space.step(dt)
        print(f"{self.body.position.x},{self.body.position.y}")
        self.update()


    def paintEvent(self, event):
        p = QPainter(self)

        # --- Dessine le sol ---
        p.setBrush(Qt.GlobalColor.gray)
        p.drawRect(0,self.H - 50,self.W,50)
        # --- Dessine la voiture ---
        x = int(self.body.position.x)
        y = int(self.H -self.body.position.y)
        self.angle = -math.degrees(self.body.angle)
        p.setBrush(Qt.GlobalColor.red)
        p.translate(self.body.position.x,self.body.position.y)
        p.rotate(self.angle)
        p.drawRect(x,self.H - y,self.size[0],self.size[1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.moveCar("forward")
        if event.key() == Qt.Key.Key_Down:
            self.moveCar("backward")
        if event.key() == Qt.Key.Key_Left:
            self.rotate_car("left")
        if event.key() == Qt.Key.Key_Right:
            self.rotate_car("right")


    def moveCar(self,sens):
        y = 50 * math.sin(self.body.angle)
        x = 50 * math.cos(self.body.angle)

        if sens == "forward":
            self.body.velocity = Vec2d(x,y)
        #else:
            #elf.body.velocity = Vec2d(x,y)

    def rotate_car(self,sens):
        if sens == "left":
            self.body.torque = 200
        if sens == "right":
            self.body.torque = -200