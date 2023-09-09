import typing

from PIL import Image
from PyQt5 import QtGui, QtWidgets, uic

from . import codecs
from .codecs import Codec, CodecError


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


class AppFuncs:
    @staticmethod
    def action_open_image(root):
        # this function opens a image in the gui app
        root.statusBar.showMessage("file dialog opened")
        filename = QtWidgets.QFileDialog.getOpenFileName()  # This is temporary
        root.statusBar.showMessage(f"Image: {filename[0]}")
        if filename[0] != "":
            root.image_viewer.setPixmap(QtGui.QPixmap(filename[0]))
            root.statusBar.showMessage(f"Displaying: {filename[0]}")
            # need to find a zooming solution for the image
            root.image = filename[0]
            root._image_tmp = Image.open(root.image)

    @staticmethod
    def action_save_image(root):
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
            try:
                args = {"bits": 1, "msb": False}  # TODO: get args from ui
                data = decode_message(root.image, codecs.lsb, args)
                root.lsbtext.setPlainText(data.decode())
                root.statusBar.showMessage("Received data from image.")
            except UnicodeDecodeError as e:
                msg = "Decoding Error (does not contain Unicode data)"
                print(f"{msg}: {e}")
                root.statusBar.showMessage(msg)
            except CodecError as e:
                msg = f"Codec Error: {e}"
                print(msg)
                root.statusBar.showMessage(msg)
        else:
            root.statusBar.showMessage("No image loaded")

    @staticmethod
    def lsbinsertdata(root):
        if root.image:
            try:
                args = {"bits": 1, "msb": False}  # TODO: get args from ui
                data = encode_message(root.image, codecs.lsb, root.lsbtext.toPlainText(), args)
            except CodecError as e:
                msg = f"Codec Error: {e}"
                print(msg)
                root.statusBar.showMessage(msg)
            root._image_tmp = data
            root.statusBar.showMessage("Data has been inserted.")
        else:
            root.statusBar.showMessage("No image loaded")


def encode_message(
    plain: typing.BinaryIO, codec: Codec, message: str, extra_args: dict[str, typing.Any]
) -> Image.Image:
    image = Image.open(plain)
    codec.encode(image, message.encode("utf-8"), **extra_args)
    return image


def decode_message(image_data: typing.BinaryIO, codec: Codec, extra_args: dict[str, typing.Any]) -> bytes:
    image = Image.open(image_data)
    return codec.decode(image, **extra_args)


def run():
    app = QtWidgets.QApplication([])
    UiApp()
    return app.exec_()
