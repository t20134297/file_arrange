import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import file_classifier_service as fcs
import os

choosePendingFolder = "选择待处理文件夹"
chooseOutputFolder = "选择输出文件夹"
chooseKeywordsFile = "选择关键词文件"
beginToClassify = "开始分类"
viewResult = "查看分类结果"
success = "分类完成"


keywordsFileNotFound = "关键词文件不存在"
pendingFolderNotFound = "待处理文件夹不存在"
createOutputFolderFailed = "创建输出文件夹失败"
keywordsNotFound = "关键词不存在"
elseKeyword = "其它"

class AppContext(ApplicationContext):

    def __init__(self):
        super().__init__()
        self.widget = None
        self.pendingFolderLineEdit = None
        self.pendingFolderButton = None
        self.outputFolderLineEdit = None
        self.outputFolderButton = None
        self.keywordsFileLineEdit = None
        self.keywordsFileButton = None
        self.confirmButton = None
        self.tipLabel = None
        self.viewResultButton = None

    def run(self):
        self.widget = QWidget()
        mainV = QVBoxLayout(self.widget)

        # 待处理文件夹空控件组
        pendingFolderHBox = QHBoxLayout()
        # 待处理文件夹输入框
        self.pendingFolderLineEdit = QLineEdit()
        # 待处理文件夹选择按钮
        self.pendingFolderButton = QPushButton()
        self.pendingFolderButton.setText(choosePendingFolder)
        self.pendingFolderButton.clicked.connect(self.onPendingFolderButtonClicked)
        pendingFolderHBox.addWidget(self.pendingFolderLineEdit)
        pendingFolderHBox.addWidget(self.pendingFolderButton)

        # 关键词文件夹空间组
        keywordsFileHBox = QHBoxLayout()
        self.keywordsFileLineEdit = QLineEdit()
        self.keywordsFileButton = QPushButton()
        self.keywordsFileButton.setText(chooseKeywordsFile)
        self.keywordsFileButton.clicked.connect(self.onKeywordsFileButtonClicked)
        keywordsFileHBox.addWidget(self.keywordsFileLineEdit)
        keywordsFileHBox.addWidget(self.keywordsFileButton)

        # 输出文件夹控件组
        outputFolderHBox = QHBoxLayout()
        self.outputFolderLineEdit = QLineEdit()
        self.outputFolderButton = QPushButton()
        self.outputFolderButton.setText(chooseOutputFolder)
        self.outputFolderButton.clicked.connect(self.onOutputFolderButtonClicked)
        outputFolderHBox.addWidget(self.outputFolderLineEdit)
        outputFolderHBox.addWidget(self.outputFolderButton)

        # 确定按钮
        self.confirmButton = QPushButton()
        self.confirmButton.setText(beginToClassify)
        self.confirmButton.clicked.connect(self.onConfirmButtonClicked)

        # 提示信息
        self.tipLabel = QLabel()
        self.tipLabel.setText("")
        self.tipLabel.setAlignment(Qt.AlignCenter)

        # 查看分类结果按钮
        viewResultBox = QHBoxLayout()
        self.viewResultButton = QPushButton()
        self.viewResultButton.setText(viewResult)
        self.viewResultButton.clicked.connect(self.onViewResultButtonClicked)
        viewResultBox.addStretch(1)
        viewResultBox.addWidget(self.viewResultButton)
        self.viewResultButton.setVisible(False)

        mainV.addStretch(1)
        mainV.addLayout(pendingFolderHBox)
        mainV.addLayout(keywordsFileHBox)
        mainV.addLayout(outputFolderHBox)
        mainV.addStretch(1)
        mainV.addWidget(self.confirmButton)
        mainV.addWidget(self.tipLabel)
        mainV.addLayout(viewResultBox)

        self.widget.setWindowTitle("File Classifier")
        self.widget.setGeometry(100, 100, 300, 300)
        self.widget.setWindowIcon(QIcon(self.get_resource("Icon.ico")))
        self.widget.show()
        return self.app.exec_()

    def onPendingFolderButtonClicked(self):
        pendingFolderPath = QFileDialog.getExistingDirectory(self.widget, choosePendingFolder, "/")
        if not pendingFolderPath == "":
            self.pendingFolderLineEdit.setText(pendingFolderPath)

    def onKeywordsFileButtonClicked(self):
        keywordsFilePathTuple = QFileDialog.getOpenFileName(self.widget, chooseKeywordsFile, "/", "Text Files (*.txt)")
        keywordsFilePath = keywordsFilePathTuple[0]
        if not keywordsFilePath == "":
            self.keywordsFileLineEdit.setText(keywordsFilePath)

    def onOutputFolderButtonClicked(self):
        outputFolderPath = QFileDialog.getExistingDirectory(self.widget, chooseOutputFolder, "/")
        if not outputFolderPath == "":
            self.outputFolderLineEdit.setText(outputFolderPath)

    def onConfirmButtonClicked(self):
        self.tipLabel.setStyleSheet("color:black")
        self.tipLabel.setText(beginToClassify)
        pendingFolderPath = self.pendingFolderLineEdit.text()
        outputFolderPath = self.outputFolderLineEdit.text()
        keywordsFilePath = self.keywordsFileLineEdit.text()
        # 检查文件
        if not self._checkPendingFolderPath(pendingFolderPath):
            return
        if not self._checkKeywordsFilePath(keywordsFilePath):
            return
        if not self._checkOutputFolderPath(outputFolderPath):
            return
        fcs.classify(keywordsFilePath, pendingFolderPath, outputFolderPath)
        self.tipLabel.setStyleSheet("color:green")
        self.tipLabel.setText(success)
        self.viewResultButton.setVisible(True)

    def onViewResultButtonClicked(self):
        outputFolderPath = self.outputFolderLineEdit.text()
        QFileDialog.getOpenFileName(self.widget, viewResult, outputFolderPath)

    def _checkPendingFolderPath(self, pendingFolderPath):
        if not os.path.exists(pendingFolderPath):
            self.tipLabel.setStyleSheet("color:red")
            self.tipLabel.setText(pendingFolderNotFound)
            return False
        return True

    def _checkKeywordsFilePath(self, keywordsFilePath):
        if not os.path.exists(keywordsFilePath):
            self.tipLabel.setStyleSheet("color:red")
            self.tipLabel.setText(keywordsFileNotFound)
            return False
        return True

    def _checkOutputFolderPath(self, outputFolderPath):
        if not os.path.exists(outputFolderPath):
            try:
                os.makedirs(outputFolderPath)
                return True
            except OSError:
                self.tipLabel.setStyleSheet("color:red")
                self.tipLabel.setText(createOutputFolderFailed)
                return False
        return True


if __name__ == '__main__':
    appContext = AppContext()
    exit_code = appContext.run()
    sys.exit(exit_code)
