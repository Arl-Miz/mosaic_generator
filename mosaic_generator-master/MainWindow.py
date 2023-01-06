from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *


class PushButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QtCore.QVariantAnimation(
            startValue=QtGui.QColor("#ff5400"),
            endValue=QtGui.QColor("#ff8500"),
            valueChanged=self._on_value_changed,
            duration=300,
        )
        self._update_stylesheet(QtGui.QColor("#ff8500"), QtGui.QColor("#1c2541"))

    def _on_value_changed(self, color):
        foreground = (
            QtGui.QColor("#1c2541")
            if self._animation.direction() == QtCore.QAbstractAnimation.Direction.Forward
            else QtGui.QColor("#ffe169")
        )
        self._update_stylesheet(color, foreground)

    def _update_stylesheet(self, background, foreground):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            border: none;
            color: %s;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border: 2px solid #ffe169;
        }
        """
            % (background.name(), foreground.name())
        )

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Direction.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Direction.Forward)
        self._animation.start()
        super().leaveEvent(event)


class Ui_MainWindow(object):
    def __init__(self, *args, obj=None, **kwargs):
        self.PushButton = PushButton
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 490)
        MainWindow.setIconSize(QtCore.QSize(45, 45))
        MainWindow.setDocumentMode(False)
        self.MainWindowGeometry = MainWindow
        self.MainWindowGeometry.setObjectName("MainWindowGeometry")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Datatset = QtWidgets.QPushButton(self.centralwidget)
        self.Datatset.setGeometry(QtCore.QRect(510, 40, 160, 30))
        self.Datatset.setObjectName("Datatset")
        self.targetImg = QtWidgets.QPushButton(self.centralwidget)
        self.targetImg.setGeometry(QtCore.QRect(510, 90, 160, 30))
        self.targetImg.setCheckable(False)
        self.targetImg.setAutoRepeat(False)
        self.targetImg.setObjectName("targetImg")
        self.previwDatasetBox = QtWidgets.QGroupBox(self.centralwidget)
        self.previwDatasetBox.setGeometry(QtCore.QRect(10, 20, 440, 390))
        self.previwDatasetBox.setObjectName("previwDatasetBox")
        self.datasetView = QtWidgets.QGraphicsView(self.previwDatasetBox)
        self.datasetView.setGeometry(QtCore.QRect(0, 20, 440, 370))
        self.datasetView.setObjectName("datasetView")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(510, 130, 160, 65))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.blockSizeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.blockSizeLabel.setObjectName("blockSizeLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.blockSizeLabel)
        self.blockSizeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.blockSizeLineEdit.setObjectName("blockSizeLineEdit")

        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.blockSizeLineEdit)
        self.previewImgBox = QtWidgets.QGroupBox(self.centralwidget)
        self.previewImgBox.setGeometry(QtCore.QRect(470, 250, 240, 160))
        self.previewImgBox.setObjectName("previewImgBox")
        self.targetImgView = QtWidgets.QGraphicsView(self.previewImgBox)
        self.targetImgView.setGeometry(QtCore.QRect(0, 30, 240, 130))
        self.targetImgView.setObjectName("targetImgView")
        self.generateBtn = self.PushButton(self.centralwidget)
        self.generateBtn.setGeometry(QtCore.QRect(220, 432, 270, 25))
        self.generateBtn.setObjectName("generateBtn")
        self.generateBtnMask = QtWidgets.QLabel(self.centralwidget)
        self.generateBtnMask.setGeometry(QtCore.QRect(220, 432, 270, 25))
        self.generateBtnMask.setObjectName("generateBtnMask")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(530, 430, 161, 28))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setRange(0, 100)
        self.horizontalLayout.addWidget(self.progressBar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionMosaic_Maker = QtGui.QAction(MainWindow)
        self.actionMosaic_Maker.setObjectName("actionMosaic_Maker")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mosaic Generetor"))
        self.Datatset.setText(_translate("MainWindow", "Add image folder"))
        self.datasetView.setProperty("class", "datasetView")
        self.targetImgView.setProperty("class", "targetImgView")
        self.targetImg.setText(_translate("MainWindow", "Add target image"))
        self.previwDatasetBox.setTitle(_translate("MainWindow", "Preview DataSet"))
        self.previwDatasetBox.setStyleSheet('color:#caf0f8;')
        self.blockSizeLabel.setText(_translate("MainWindow", "block size"))
        self.blockSizeLabel.setStyleSheet('color:#caf0f8;')
        self.blockSizeLineEdit.setStyleSheet("#blockSizeLineEdit{background-color:#ffbf69;border-radius:11px;padding:5 1px;text-align: center;}#blockSizeLineEdit:hover{background-color:#ff9e00;border-radius:11px}")
        self.previewImgBox.setTitle(_translate("MainWindow", "Preview Target Image"))
        self.previewImgBox.setStyleSheet('color:#caf0f8;')
        self.generateBtn.setText(_translate("MainWindow", "Generate"))
        self.actionMosaic_Maker.setText(_translate("MainWindow", "Mosaic Maker"))
        self.blockSizeLabel.setToolTip('sets accuracy')
        self.blockSizeLineEdit.setPlaceholderText("Enter an integer!!")
        self.blockSizeLineEdit.setValidator(QtGui.QIntValidator())
        self.targetImg.setProperty("class", "fileButton")
        self.Datatset.setProperty("class", "fileButton")
        self.generateBtnMask.setProperty("class", "generateBtnMask")
        self.generateBtn.setProperty("class", "generateButton")
        self.progressBar.setProperty("class", "GreenProgressBar")
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(50)
        self.previwDatasetBox.setGraphicsEffect(self.shadow)
        self.label_dataset_img = QLabel(self.previwDatasetBox)
        self.label_dataset_img.setGeometry(self.datasetView.frameGeometry())
        self.label_target_img = QLabel(self.previewImgBox)
        self.label_target_img.setGeometry(self.targetImgView.frameGeometry())
        self.generateBtn.hide()
