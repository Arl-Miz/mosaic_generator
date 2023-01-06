import os
import re
import sys

import cv2
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from MainWindow import Ui_MainWindow
from Qss import StyleSheet
from mosaic_generator import MosaicGenerator

pwd = os.getcwd()
progress_re = re.compile("Total complete: (\d+)%")


def simple_percent_parser(output):
    m = progress_re.search(output)
    if m:
        pc_complete = m.group(1)
        return int(pc_complete)


class AnotherWindow(QWidget):
    def __init__(self, mainWindow, *args, obj=None, **kwargs, ):
        super(AnotherWindow, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.resize(720, 490)
        self.mainWindow = mainWindow
        self.label_output = QLabel(self)
        self.label_output.setGeometry(QtCore.QRect(0, 0, 720, 410))
        self.h, self.w = cv2.imread(mainWindow.target_image).shape[:2]
        output = f'mosaic-{mainWindow.block_size}-{self.h}x{self.w}.png'
        self.tixmap = QtGui.QPixmap(f'{pwd}/{output}')
        os.system(f'rm -rf {pwd}/{output}')
        self.tixmap = self.tixmap.scaled(720, 480)
        self.label_output.setPixmap(self.tixmap)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.adjustSize()
        layout.addWidget(self.label)
        self.save_button = self.mainWindow.PushButton("save")
        self.save_button.clicked.connect(self.save)
        self.save_button.setProperty("class", "generateButton")
        layout.addWidget(self.save_button)
        self.reset_button = self.mainWindow.PushButton("reset")
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setProperty("class", "generateButton")
        layout.addWidget(self.reset_button)

    def save(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Enter name", pwd)
        if path:
            self.tixmap.save(f'{path[0]}')

    def reset(self):
        self.mainWindow.block_size = None
        self.mainWindow.target_image = None
        self.mainWindow.dataset_folder_path = None
        self.mainWindow.dataset = None
        self.mainWindow.shape = None
        self.mainWindow.blockSizeLineEdit.clear()
        self.mainWindow.targetImg.setText("Add target image")
        self.mainWindow.Datatset.setText("Add image folder")
        self.mainWindow.label_dataset_img.setStyleSheet("")
        self.mainWindow.label_target_img.setStyleSheet("")
        self.mainWindow.progressBar.reset()
        self.close()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, MosaicGenerator):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # self.show_popup()
        self.label_output = None
        self.tixmap = None
        self.block_size = None
        self.target_image = None
        self.dataset_folder_path = None
        self.dataset = None
        self.shape = None
        self.outPutWindow = None
        self.process = None

        self.Datatset.clicked.connect(lambda: self.load_dataset())
        self.targetImg.clicked.connect(lambda: self.load_target_image())
        self.blockSizeLineEdit.textChanged[str].connect(self.onChanged)
        self.generateBtn.clicked.connect(lambda: self.start_process())
        self.effect = QGraphicsOpacityEffect(self.generateBtn)
        self.generateBtn.setGraphicsEffect(self.effect)

    def _anim(self):
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setDuration(2100)
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.start()


    def start_process(self):
        if self.process is None:
            # self.message("Executing process")
            self.process = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.stateChanged.connect(self.handle_state)
            self.process.finished.connect(self.onFinished)
            self.process.start("python3", [f'mosaic_generator.py', f'{self.block_size}', f'{self.target_image}', f'{self.dataset_folder_path}'])

    def onFinished(self):
        self.outPutWindow = AnotherWindow(self)

        if self.outPutWindow.isVisible():
            self.outPutWindow.hide()

        else:
            self.outPutWindow.show()
        self.process = None

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        progress = simple_percent_parser(stderr)
        if progress:
            self.progressBar.setValue(progress)
        # self.message(stderr)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")

    def handle_state(self, state):
        states = {
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running',
        }
        state_name = states[state]

    def close(self):
        QtCore.QCoreApplication.instance().quit()

    def check(self):
        if self.block_size and self.target_image and self.dataset_folder_path:
            self.generateBtnMask.hide()
            output = f'mosaic-{self.block_size}-{self.shape[0]}x{self.shape[1]}.png'
            if output:
                os.system(f'rm -rf {pwd}/{output}')
            self.generateBtn.show()
            self._anim()

    def onChanged(self, text):
        if text:
            self.block_size = int(text)
            self.statusbar.clearMessage()
            self.check()
        else:
            self.generateBtn.hide()
            self.generateBtnMask.show()
            self.statusbar.showMessage("enter valid block size!!", 3300)

    def show_popup(self):
        msg = QMessageBox(text="Hello you are about to enter mosaic generator!", parent=self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setText('''
            - enter target image
            - add your data set folder
            - enter block size
                (it is more accurate it's when smaller)
            - enter your favorite width and height
            - click on ok button to preview your inputs
            - click on cancel to close
            - click on generate to see output
    ''')
        msg.setStyleSheet('width:500px')
        msg.exec()

    def load_dataset(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"), )
        if file:
            self.dataset_folder_path = file
            self.dataset = self.load_images_from_folder()
            w = 440
            h = 370
            dataShown = self.data_show()
            self._update_ldi_stylesheet(dataShown)
            os.system(f'rm -rf {pwd}/{dataShown}')
            self.Datatset.setText("reset folder path")
            self.check()
        else:

            self.label_dataset_img.setStyleSheet("")
            print(self.dataset_folder_path)

    def load_target_image(self):
        self.statusbar.clearMessage()
        self.target_image = QFileDialog.getOpenFileName(
            self,
            "Open File",
            pwd,
            "All Files (*);; Python Files (*.py);; PNG Files (*.png);; JPG Files (*.jpg) ;; JPEG Files (*jpeg)",
        )[0]
        if self.target_image:
            if self.target_image.find(".png") != -1 or self.target_image.find(".jpeg") != -1 or self.target_image.find(".jpg") != -1:
                self.shape = cv2.imread(self.target_image).shape[:2]
                self.targetImg.setText("rest target image")
                self._update_lti_stylesheet(self.target_image)
                self.check()
            else:
                self.statusbar.showMessage('enter valid image!!', 3300)
                self.label_target_img.setStyleSheet("")

    def _update_ldi_stylesheet(self, dataShown):
        self.label_dataset_img.setStyleSheet(f"""
            border-image: url('{dataShown}');
            border-radius:9;
            margin-top:10px;
            border :6px solid #fdbb2d;
            border-top-left-radius :20px;
            border-top-right-radius : 20px; 
            border-bottom-right-radius : 133px; 
            border-bottom-left-radius : 20px;
            margin-top:11px;
            margin-bottom:1px;
            margin-right:1px;
            margin-left:1px
                    """)

    def _update_lti_stylesheet(self, bi):
        self.label_target_img.setStyleSheet(f"""
            border-image: url('{bi}') ;
            border-radius:9;
            border :7px solid #fdbb2d;
            border-top-right-radius :20px;
            border-top-left-radius : 53px;
            border-bottom-right-radius : 20px;
            border-bottom-left-radius : 20px
                """)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(StyleSheet())
    window = MainWindow()
    window.show()
    app.exec()

    '''
    dio
        https://google.com/
        https://stackoverflow.com/
        https://www.pythonguis.com/pyqt6/
        https://www.tutorialspoint.com/pyqt/pyqt_qfiledialog_widget.htm
        https://programtalk.com/python-more-examples/PyQt6.QtCore.QAbstractAnimation.Direction.Forward/
        https://clay-atlas.com/us/blog/2021/05/18/pyqt5-en-save-text-image-qlabel-as-picture/
        https://realpython.com/python-pyqt-layout/
        https://www.pythonguis.com/tutorials/pyqt6-qprocess-external-programs/
        https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QFileDialog.html#PySide2.QtWidgets.PySide2.QtWidgets.QFileDialog.getOpenFileNames
    '''

