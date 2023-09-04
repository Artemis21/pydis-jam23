from PyQt5 import QtGui, QtWidgets, uic


class UiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi("src/ui_files/main.ui", self)
        # self.ui.setWindowIcon() # we need a icon
        # self.ui.setWindowTitle() # already set in 'main.ui' file but just incase
        self._functions()
        self.show()  # displays the QMainWindow in QApplication Instance

    def _functions(self):
        self.action_open_image.triggered.connect(lambda: AppFuncs.action_open_image(self.image_viewer))
        self.action_save_image.triggered.connect(AppFuncs.action_save_image)

    # def resizeEvent(self, event):
    # ^ this is a problem for hatch formatting because this method is inherited from QMainWindow
    #     # self.image_scaled = image.scaled(self.scroll.width(),self.scroll.height())
    #     # self.pixmap = QPixmap.fromImage(self.image_scaled)
    #     # self.imageLabel.setPixmap(self.pixmap)
    #     QtWidgets.QMainWindow.resizeEvent(self, event)
    #     print(event)


class AppFuncs:
    @staticmethod
    def action_open_image(image_viewer):
        # this function opens a image in the gui app
        print("opening image")
        filename = QtWidgets.QFileDialog.getOpenFileName()
        print(filename)
        # dlg = QtWidgets.QFileDialog()
        # dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        # dlg.setFilter("Text files (*.*)")
        # filenames = QtCore.QStringListModel()
        # print(filenames)
        # image_viewer to display opened image
        image_viewer.setPixmap(QtGui.QPixmap(filename[0]))
        # need to find a zooming solution for the image

    @staticmethod
    def action_save_image():
        # this function saves a image in the gui app
        print("saving image")


def run_app():
    app = QtWidgets.QApplication([])
    UiApp()
    app.exec_()
