import sys
import cv2
import qrcode
import database

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt

class Menu(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("main.ui", self)
        self.pushButton_5.clicked.connect(self.GenQR)
        self.pushButton_6.clicked.connect(self.Presence)

    def GenQR(self):
        genQR = GenQR()
        widget.addWidget(genQR)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Presence(self):
        presence = Presence()
        widget.addWidget(presence)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class GenQR(QMainWindow):
    def __init__(self):
        super(GenQR, self).__init__()
        loadUi("genqr.ui", self)
        self.pushButton_10.clicked.connect(self.Menu)
        self.pushButton_11.clicked.connect(self.PopUpGenerate)
    
    def Menu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def PopUpGenerate(self):
        nim = self.textEdit.toPlainText()
        if (nim == ""):
            self.label.clear()
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Masukan NIM Terlebih Dahulu")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()
        else:
            if (nim == "18220051" or nim == "18220063" or nim == "18220064"):
                img = qrcode.make(nim)
                qr = ImageQt(img)
                pix = QPixmap.fromImage(qr)
                self.label.setPixmap(pix)
                msg = QMessageBox()
                msg.setWindowTitle("Notification")
                msg.setText("QR berhasil di generate, silahkan simpan QR")
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()
            else:
                self.label.clear()
                msg = QMessageBox()
                msg.setWindowTitle("Notification")
                msg.setText("NIM tidak terdaftar pada database, silahkan coba lagi")
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()

class Presence(QMainWindow):

    qrValid = False
    speechValid = True
    nim = ""

    def __init__(self):
        super(Presence, self).__init__()
        loadUi("presence.ui", self)
        self.pushButton_10.clicked.connect(self.Menu)
        self.pushButton_7.clicked.connect(self.ScanQR)
        self.pushButton_8.clicked.connect(self.ValidSpeech)
        self.pushButton_9.clicked.connect(self.Presensi)
    
    def Menu(self):
        Presence.qrValid = False
        Presence.speechValid = False
        Presence.nim = ""
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def ScanQR(self):
        msg = QMessageBox()
        msg.setWindowTitle("Notification")
        msg.setText("Arahkan QR ke depan kamera")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
        vid = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            ret, frame = vid.read()
            data, bbox, straight_qrcode = detector.detectAndDecode(frame)
            if len(data) > 0:
                if (data == '18220051' or data == '18220063' or data == '18220064'):
                    self.textBrowser.setStyleSheet("background-color: rgb(0, 255, 0)")
                    Presence.qrValid = True
                    Presence.nim = data
                else:
                    self.textBrowser.setStyleSheet("background-color: rgb(255, 0, 0);")
            cv2.imshow('frame', frame)
            if cv2.waitKey(1000):
                break
        vid.release()
        cv2.destroyAllWindows()
    
    def ValidSpeech(self):
        # Source Code Rekam Suara
        print("")

    def Presensi(self):
        if Presence.qrValid and Presence.speechValid:
            # Ubah status di database
            database.presensi(Presence.nim)
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Presensi berhasil dilakukan")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            Presence.Menu(self)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Pastikan QR dan speech valid")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

# main
app = QApplication(sys.argv)
welcome = Menu()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exit Program")