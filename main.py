import sys
import traceback

from PyQt6.QtWidgets import QApplication, QDockWidget

from controller.main_controller import MainController
from view.Dock_view import DockWindow
from view.Graph_Canvas import GraphCanvas
from view.Graph_View import GraphView
from view.MainWindow import MainWindow
from view.PhysiqueWindow import PhysiqueQtWidget

if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook

    app = QApplication(sys.argv)
    fenetre = MainWindow()
    physique = PhysiqueQtWidget()
    canvas = GraphCanvas()
    graphView = GraphView()
    dock = DockWindow()
    controller = MainController(fenetre,canvas,physique,graphView,dock)
    #fenetre.set_controller(controller)
    fenetre.show()


    sys.exit(app.exec())

