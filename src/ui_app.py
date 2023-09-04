from PyQt5 import QtWidgets, uic


class UiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi("src/ui_files/main.ui", self)
        # self.ui.setWindowIcon() # we need a icon
        # self.ui.setWindowTitle() # already set in 'main.ui' file but just incase
        self._functions()
        self.show()

    def _functions(self):
        self.action_open_image.triggered.connect(AppFuncs.action_open_image)
        self.action_save_image.triggered.connect(AppFuncs.action_save_image)

    # def resizeEvent(self, event):
    # ^ this is a problem for hatch formatting because this method is inherited from QMainWindow
    #     # self.image_scaled = image.scaled(self.scroll.width(),self.scroll.height())
    #     # self.pixmap = QPixmap.fromImage(self.image_scaled)
    #     # self.imageLabel.setPixmap(self.pixmap)
    #     QtWidgets.QMainWindow.resizeEvent(self, event)
    #     print(event)


class AppFuncs:
    def action_open_image():
        # this function opens a image in the gui app
        print("opening image")
        # self.image_viewer to display opened image

    def action_save_image():
        # this function saves a image in the gui app
        print("saving image")


def run_app():
    app = QtWidgets.QApplication([])
    UiApp()
    app.exec_()
