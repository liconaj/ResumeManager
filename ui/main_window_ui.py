# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModal)
        MainWindow.resize(1000, 600)
        MainWindow.setFocusPolicy(Qt.ClickFocus)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.idSearchLineEdit = QLineEdit(self.centralwidget)
        self.idSearchLineEdit.setObjectName(u"idSearchLineEdit")
        self.idSearchLineEdit.setGeometry(QRect(20, 20, 111, 31))
        self.advancedSearchLineEdit = QLineEdit(self.centralwidget)
        self.advancedSearchLineEdit.setObjectName(u"advancedSearchLineEdit")
        self.advancedSearchLineEdit.setGeometry(QRect(140, 20, 341, 31))
        self.syncPushButton = QPushButton(self.centralwidget)
        self.syncPushButton.setObjectName(u"syncPushButton")
        self.syncPushButton.setGeometry(QRect(880, 20, 101, 31))
        self.profilesTableView = QTableView(self.centralwidget)
        self.profilesTableView.setObjectName(u"profilesTableView")
        self.profilesTableView.setGeometry(QRect(20, 60, 961, 481))
        self.profilesTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.profilesTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.profilesTableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.profilesTableView.setAutoScroll(False)
        self.profilesTableView.setAlternatingRowColors(False)
        self.profilesTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.profilesTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.profilesTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.profilesTableView.setShowGrid(True)
        self.profilesTableView.setCornerButtonEnabled(True)
        self.profilesTableView.verticalHeader().setVisible(False)
        self.importProfilePushButton = QPushButton(self.centralwidget)
        self.importProfilePushButton.setObjectName(u"importProfilePushButton")
        self.importProfilePushButton.setGeometry(QRect(770, 20, 91, 31))
        self.deleteProfilePushButton = QPushButton(self.centralwidget)
        self.deleteProfilePushButton.setObjectName(u"deleteProfilePushButton")
        self.deleteProfilePushButton.setEnabled(False)
        self.deleteProfilePushButton.setGeometry(QRect(680, 550, 131, 31))
        self.deleteProfilePushButton.setFlat(False)
        self.seeProfilePushButton = QPushButton(self.centralwidget)
        self.seeProfilePushButton.setObjectName(u"seeProfilePushButton")
        self.seeProfilePushButton.setGeometry(QRect(834, 550, 151, 31))
        self.searchItemComboBox = QComboBox(self.centralwidget)
        self.searchItemComboBox.setObjectName(u"searchItemComboBox")
        self.searchItemComboBox.setGeometry(QRect(490, 20, 161, 31))
        self.searchItemComboBox.setEditable(False)
        self.resultsLabel = QLabel(self.centralwidget)
        self.resultsLabel.setObjectName(u"resultsLabel")
        self.resultsLabel.setGeometry(QRect(20, 550, 381, 16))
        font = QFont()
        font.setPointSize(10)
        self.resultsLabel.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.idSearchLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.advancedSearchLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Buscar", None))
        self.syncPushButton.setText(QCoreApplication.translate("MainWindow", u"Sincronizar", None))
        self.importProfilePushButton.setText(QCoreApplication.translate("MainWindow", u"Importar", None))
        self.deleteProfilePushButton.setText(QCoreApplication.translate("MainWindow", u"Eliminar", None))
        self.seeProfilePushButton.setText(QCoreApplication.translate("MainWindow", u"Ver perfil", None))
        self.searchItemComboBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Filtrar por columna", None))
        self.resultsLabel.setText(QCoreApplication.translate("MainWindow", u"Resultados", None))
    # retranslateUi

