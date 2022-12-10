import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from random import *

class ShowVideo(QtCore.QObject):
    flag = 0

    camera = cv2.VideoCapture(0)

    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global image
        global started

        started = True

        self.run_video = True
        while self.run_video:
            ret, image = self.camera.read()
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            self.qt_image = QtGui.QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal1.emit(self.qt_image)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    @QtCore.pyqtSlot()
    def savePicture(self):
        global started
        global input_sick
        global result
        global input_sick_str
        global result_str

        if started:
            filename = './capture.png'
            self.qt_image.save(filename)

            string = "100+200"
            res = "300"

            input_sick.setText(input_sick_str + string)
            result.setText(result_str + res)
        
class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui. QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

started = False
input_sick_str = "Formula : "
result_str = "Result : "

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)

    image_viewer1 = ImageViewer()

    vid.VideoSignal1.connect(image_viewer1.setImage)

    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Capture')
    blank = QtWidgets.QLabel(' ')
    input_sick = QtWidgets.QLabel(input_sick_str)
    result = QtWidgets.QLabel(result_str)
    input_sick.setAlignment(Qt.AlignCenter)
    result.setAlignment(Qt.AlignCenter)
    
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.savePicture)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)
    vertical_layout.addWidget(blank)
    vertical_layout.addWidget(input_sick)
    vertical_layout.addWidget(result)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())