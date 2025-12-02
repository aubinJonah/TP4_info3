import pymunk
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QBrush, QPainter
from PyQt6.QtWidgets import QWidget


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
        mass = 5
        self.size = (5,5)
        self.body = pymunk.Body(mass, pymunk.moment_for_box(mass, self.size))
        self.body.position = (200, 100)
        shape = pymunk.Poly.create_box(self.body)
        shape.elasticity = 0.8
        self.space.add(self.body, shape)


    def update_simulation(self):
        dt = 1 / 60

        self.space.step(dt)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)

        # --- Dessine le sol ---
        p.setBrush(Qt.GlobalColor.gray)
        p.drawRect(0,self.H - 50,self.W,50)
        # --- Dessine la voiture ---
        x = int(self.body.position.x)
        y = int(self.H - self.body.position.y)
        p.setBrush(Qt.GlobalColor.red)
        p.drawRect(x,self.size[0],self.size[1],y)