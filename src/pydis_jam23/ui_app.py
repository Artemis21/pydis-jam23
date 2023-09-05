from PIL import Image
from PyQt5 import QtGui, QtWidgets, uic

from .codecs import CODECS, decode_message, encode_message


class UiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi("src/pydis_jam23/ui_files/main.ui", self)
        self.ui.setWindowIcon(QtGui.QIcon("src/pydis_jam23/ui_files/appicon.png"))  # we need a icon
        # self.ui.setWindowTitle() # already set in 'main.ui' file but just incase
        self._temp()
        self._functions()
        self.statusBar.showMessage("Application Started")
        self.show()  # displays the QMainWindow in QApplication Instance

    def _temp(self):
        self._image_tmp = None
        self.image = None

    def _functions(self):
        # initial widget state configs
        self.lsbframe.hide()
        self.lsbinsertdata.hide()

        # shortcut key actions
        self.action_open_image.setShortcut("Ctrl+O")
        self.action_save_image.setShortcut("Ctrl+S")
        self.action_exit_app.setShortcut("Ctrl+Q")

        # lambda functions triggered by ui elements/buttons
        self.action_open_image.triggered.connect(lambda: AppFuncs.action_open_image(self))
        self.action_save_image.triggered.connect(lambda: AppFuncs.action_save_image(self))
        self.action_exit_app.triggered.connect(lambda: AppFuncs.action_exit_app(self))
        self.lsbtoolbtn.clicked.connect(lambda: AppFuncs.lsbtoolsection(self.statusBar, self.lsbframe))
        self.lsbaction.currentTextChanged.connect(lambda: AppFuncs.lsbaction(self))
        # self.lsbcodec.currentTextChanged.connect(lambda: AppFuncs.lsbsetcodec(self) )
        self.lsbinsertbtn.clicked.connect(lambda: AppFuncs.lsbinsertdata(self))
        self.lsbreceivebtn.clicked.connect(lambda: AppFuncs.lsbreceivedata(self))

    # def resizeEvent(self, event):
    # ^ this is a problem for hatch formatting because this method is inherited from QMainWindow
    #     # self.image_scaled = image.scaled(self.scroll.width(),self.scroll.height())
    #     # self.pixmap = QPixmap.fromImage(self.image_scaled)
    #     # self.imageLabel.setPixmap(self.pixmap)
    #     QtWidgets.QMainWindow.resizeEvent(self, event)
    #     print(event)


class AppFuncs:
    @staticmethod
    def action_open_image(root):
        # this function opens a image in the gui app
        root.statusBar.showMessage("file dialog opened")
        filename = QtWidgets.QFileDialog.getOpenFileName()  # This is temporary
        # print(filename)
        root.statusBar.showMessage(f"Image: {filename[0]}")
        # dlg = QtWidgets.QFileDialog()
        # dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        # dlg.setFilter("Text files (*.*)")
        # filenames = QtCore.QStringListModel()
        # print(filenames)
        # image_viewer to display opened image
        if filename[0] != "":
            root.image_viewer.setPixmap(QtGui.QPixmap(filename[0]))
            root.statusBar.showMessage(f"Displaying: {filename[0]}")
            # need to find a zooming solution for the image
            root.image = filename[0]
            root._image_tmp = Image.open(root.image)

    @staticmethod
    def action_save_image(root):
        # this function saves a image in the gui app
        print("saving image")
        # with open('newImage.jpg', 'wb') as imagefile:
        #     imagefile.write(root._image_tmp)
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(root, "Save File", "", "All Files(*);;Text Files(*.png)")
        root._image_tmp.save(file_name, format="PNG")
        root.statusBar.showMessage("Image saved")

    @staticmethod
    def action_exit_app(root):
        root.close()

    @staticmethod
    def lsbtoolsection(status, _frame):
        if _frame.isHidden():
            _frame.show()
            status.showMessage("lsbtools opened")
        elif not _frame.isHidden():
            _frame.hide()
            status.showMessage("lsbtools closed")

    @staticmethod
    def lsbaction(root):
        # print('lsb action')
        option = ["Insert Data", "Retrieve Data"]
        if root.lsbaction.currentText() == option[0]:
            print("Inserting data")
            root.lsbtext.setReadOnly(False)
            root.lsbtext.setPlaceholderText("Insert text you want to embed.")
            root.lsbinsertdata.show()
            root.lsbinsertbtn.show()
            root.lsbreceivebtn.hide()
        elif root.lsbaction.currentText() == option[1]:
            print("Recieving data")
            root.lsbtext.setPlainText("")
            root.lsbtext.setReadOnly(True)
            root.lsbtext.setPlaceholderText("Retrieved data will be displayed here.")
            root.lsbinsertdata.show()
            root.lsbinsertbtn.hide()
            root.lsbreceivebtn.show()
        else:
            root.lsbinsertdata.hide()

    @staticmethod
    def lsbreceivedata(root):
        if root.image:
            data = decode_message(root.image, CODECS[0], root.image)
            try:
                root.lsbtext.setPlainText(data.decode())
                root.statusBar.showMessage("Received data from image.")
            except UnicodeDecodeError as e:
                msg = "Decoding Error"
                print(f"{msg}: {e}")
                root.statusBar.showMessage(msg)
        else:
            root.statusBar.showMessage("No image loaded")

    @staticmethod
    def lsbinsertdata(root):
        if root.image:
            data = encode_message(root.image, CODECS[0], root.lsbtext.toPlainText())
            root._image_tmp = data
            root.statusBar.showMessage("Data has been inserted.")
        else:
            root.statusBar.showMessage("No image loaded")


def run_app():
    app = QtWidgets.QApplication([])
    UiApp()
    return app.exec_()
