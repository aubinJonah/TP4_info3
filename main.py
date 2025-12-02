import sys
import traceback

from PyQt6.QtWidgets import QApplication

from controller.main_controller import MainController
from model.model import Model
from view.MainWindow import MainWindow

if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook

    app = QApplication(sys.argv)
    fenetre = MainWindow()
    model = Model()
    controller = MainController(fenetre,model)
    fenetre.set_controller(controller)
    fenetre.show()


    sys.exit(app.exec())

