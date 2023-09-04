from PyQt5 import QtGui, QtWidgets, uic


class UiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi("src/ui_files/main.ui", self)
        # self.ui.setWindowIcon() # we need a icon
        # self.ui.setWindowTitle() # already set in 'main.ui' file but just incase
        self.lsbframe.hide()
        self._functions()
        self.statusBar.showMessage("Application Started")
        self.show()  # displays the QMainWindow in QApplication Instance

    def _functions(self):
        self.action_open_image.triggered.connect(lambda: AppFuncs.action_open_image(self.statusBar, self.image_viewer))
        self.action_save_image.triggered.connect(AppFuncs.action_save_image)
        self.lsbtoolbtn.clicked.connect(lambda: AppFuncs.lsbtoolsection(self.statusBar, self.lsbframe))

    # def resizeEvent(self, event):
    # ^ this is a problem for hatch formatting because this method is inherited from QMainWindow
    #     # self.image_scaled = image.scaled(self.scroll.width(),self.scroll.height())
    #     # self.pixmap = QPixmap.fromImage(self.image_scaled)
    #     # self.imageLabel.setPixmap(self.pixmap)
    #     QtWidgets.QMainWindow.resizeEvent(self, event)
    #     print(event)


class AppFuncs:
    @staticmethod
    def action_open_image(status, image_viewer):
        # this function opens a image in the gui app
        status.showMessage("file dialog opened")
        filename = QtWidgets.QFileDialog.getOpenFileName()
        print(filename)
        status.showMessage(f"Image: {filename[0]}")
        # dlg = QtWidgets.QFileDialog()
        # dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        # dlg.setFilter("Text files (*.*)")
        # filenames = QtCore.QStringListModel()
        # print(filenames)
        # image_viewer to display opened image
        image_viewer.setPixmap(QtGui.QPixmap(filename[0]))
        status.showMessage(f"{filename[0]} displayed")
        # need to find a zooming solution for the image

    @staticmethod
    def action_save_image():
        # this function saves a image in the gui app
        print("saving image")

    @staticmethod
    def lsbtoolsection(status, _frame):
        if _frame.isHidden():
            _frame.show()
            status.showMessage("lsbtools opened")
        elif not _frame.isHidden():
            _frame.hide()
            status.showMessage("lsbtools closed")


def run_app():
    app = QtWidgets.QApplication([])
    UiApp()
    app.exec_()
