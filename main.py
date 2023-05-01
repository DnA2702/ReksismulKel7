import sys
import cv2
import qrcode
import database
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PIL.ImageQt import ImageQt
path = os.path.abspath("Speaker-Identification-Using-Machine-Learning-master")
print(path)
sys.path.insert(0, path)
import SpeakerIdentification

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
            if (database.validatenim(nim)):
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
    speechValid = False
    nim = ""
    print(qrValid,",",speechValid,",",nim)

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
        msg.setText("Arahkan QR ke depan kamera, klik 'OK' untuk memindai QR")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()
        vid = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            ret, frame = vid.read()
            data, bbox, straight_qrcode = detector.detectAndDecode(frame)
            if len(data) > 0:
                
                if (database.validatenim(data)):
                    self.textBrowser.setStyleSheet("background-color: rgb(0, 255, 0)")
                    Presence.qrValid = True
                    Presence.nim = data
                else:
                    self.textBrowser.setStyleSheet("background-color: rgb(255, 0, 0);")
                    Presence.qrValid = False
                    Presence.nim = data
            cv2.imshow('frame', frame)
            if cv2.waitKey(1000):
                break
        vid.release()
        cv2.destroyAllWindows()
    
    def ValidSpeech(self):
        # Source Code Rekam Suara
        if Presence.qrValid:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Klik 'OK' untuk memulai rekaman suara. Rekaman akan dilakukan selama 3 detik")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            nama = database.getnama(Presence.nim)
            SpeakerIdentification.record_audio_test()
            hasil = SpeakerIdentification.test_model()
            if str(hasil).lower() == nama.lower():
                self.textBrowser_2.setStyleSheet("background-color: rgb(0, 255, 0)")
                Presence.speechValid = True
            else:
                self.textBrowser_2.setStyleSheet("background-color: rgb(255, 0, 0);")
                Presence.speechValid = False
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Pastikan QR valid sebelum melakukan validasi Speaker")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()       
    def Presensi(self):
        print(Presence.qrValid,",",Presence.speechValid,",",Presence.nim)
        if Presence.qrValid and Presence.speechValid:
            # Ubah status di database
            database.presensi(Presence.nim)
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Presensi berhasil dilakukan")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            # Presence.Menu(self)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Notification")
            msg.setText("Pastikan QR dan speaker valid")
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