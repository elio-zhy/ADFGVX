from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import sys
import string
import random
from adfgvx import ADFGVX


# details in https://leomoon.com/journal/python/high-dpi-scaling-in-pyqt5/
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons


class Encrypter(QObject):
    finished = pyqtSignal(str)

    @pyqtSlot(str, str, str)
    def run(self, plaintext, square, keyword):
        try:
            ret = ADFGVX(square, keyword).encrypt(plaintext)
        except Exception as e:
            ret = str(e)
        self.finished.emit(ret)


class Decrypter(QObject):
    finished = pyqtSignal(str)

    @pyqtSlot(str, str, str)
    def run(self, ciphertext, square, keyword):
        try:
            ret = ADFGVX(square, keyword).decrypt(ciphertext)
        except Exception as e:
            ret = str(e)
        self.finished.emit(ret)


class Ui(QtWidgets.QMainWindow):
    encrypt_requested = pyqtSignal(str, str, str)
    decrypt_requested = pyqtSignal(str, str, str)

    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('./main.ui', self) # Load the .ui file
        self.setup_ui()
        self.show() # Show the GUI

    def setup_ui(self):
        self.encrypt_btn.clicked.connect(self.encrypt_btn_clicked)
        self.encrypt_btn.clicked.connect(self.crypt_started)
        self.decrypt_btn.clicked.connect(self.decrypt_btn_clicked)
        self.decrypt_btn.clicked.connect(self.crypt_started)
        self.random_btn.clicked.connect(self.random_btn_clicked)

    def encrypt_btn_clicked(self):
        self.worker = Encrypter()
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        plaintext = self.plaintext_edit.toPlainText()
        square = self.square_edit.text()
        keyword  = self.keyword_edit.text()

        # connect signals and slots
        self.worker_thread.started.connect(
            lambda: self.encrypt_requested.emit(plaintext, square, keyword)
        )
        self.encrypt_requested.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.crypt_finished)
        self.worker.finished.connect(self.ciphertext_edit.setPlainText)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def decrypt_btn_clicked(self):
        self.worker = Decrypter()
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        ciphertext = self.ciphertext_edit.toPlainText()
        square = self.square_edit.text()
        keyword  = self.keyword_edit.text()

        # connect signals and slots
        self.worker_thread.started.connect(
            lambda: self.encrypt_requested.emit(ciphertext, square, keyword)
        )
        self.encrypt_requested.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.crypt_finished)
        self.worker.finished.connect(self.plaintext_edit.setPlainText)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def crypt_started(self):
        self.encrypt_btn.setEnabled(False)
        self.decrypt_btn.setEnabled(False)

    def crypt_finished(self):
        self.encrypt_btn.setEnabled(True)
        self.decrypt_btn.setEnabled(True)

    def random_btn_clicked(self):
        s = string.ascii_uppercase + string.digits
        self.square_edit.setText("".join(random.sample(s, len(s))))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Ui() # Create an instance of our class
    app.exec_() # Start the application