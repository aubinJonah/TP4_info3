from PyQt6.QtWidgets import QDockWidget, QComboBox, QSlider
from PyQt6.uic import loadUi


class DockWindow(QDockWidget):
    SurfacecomboBox:QComboBox
    PoidshorizontalSlider:QSlider
    PuissancehorizontalSlider:QSlider

    def __init__(self):
        super().__init__()
        loadUi("view/ui/caracteristiques.ui", self)