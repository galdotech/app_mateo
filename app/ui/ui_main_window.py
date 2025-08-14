# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QLabel,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(820, 560)
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName(u"actionSalir")
        self.actionClientes = QAction(MainWindow)
        self.actionClientes.setObjectName(u"actionClientes")
        self.actionDispositivos = QAction(MainWindow)
        self.actionDispositivos.setObjectName(u"actionDispositivos")
        self.actionInventario = QAction(MainWindow)
        self.actionInventario.setObjectName(u"actionInventario")
        self.actionReparaciones = QAction(MainWindow)
        self.actionReparaciones.setObjectName(u"actionReparaciones")
        self.actionTemaClaro = QAction(MainWindow)
        self.actionTemaClaro.setObjectName(u"actionTemaClaro")
        self.actionTemaOscuro = QAction(MainWindow)
        self.actionTemaOscuro.setObjectName(u"actionTemaOscuro")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutMain = QVBoxLayout(self.centralwidget)
        self.verticalLayoutMain.setSpacing(12)
        self.verticalLayoutMain.setObjectName(u"verticalLayoutMain")
        self.verticalLayoutMain.setContentsMargins(12, 12, 12, 12)
        self.groupBoxResumen = QGroupBox(self.centralwidget)
        self.groupBoxResumen.setObjectName(u"groupBoxResumen")
        self.formLayoutResumen = QFormLayout(self.groupBoxResumen)
        self.formLayoutResumen.setSpacing(12)
        self.formLayoutResumen.setObjectName(u"formLayoutResumen")
        self.formLayoutResumen.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.formLayoutResumen.setContentsMargins(12, 12, 12, 12)
        self.labelClientes = QLabel(self.groupBoxResumen)
        self.labelClientes.setObjectName(u"labelClientes")

        self.formLayoutResumen.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelClientes)

        self.label_total_clientes = QLabel(self.groupBoxResumen)
        self.label_total_clientes.setObjectName(u"label_total_clientes")

        self.formLayoutResumen.setWidget(0, QFormLayout.ItemRole.FieldRole, self.label_total_clientes)

        self.labelDispositivos = QLabel(self.groupBoxResumen)
        self.labelDispositivos.setObjectName(u"labelDispositivos")

        self.formLayoutResumen.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelDispositivos)

        self.label_total_dispositivos = QLabel(self.groupBoxResumen)
        self.label_total_dispositivos.setObjectName(u"label_total_dispositivos")

        self.formLayoutResumen.setWidget(1, QFormLayout.ItemRole.FieldRole, self.label_total_dispositivos)

        self.labelProductos = QLabel(self.groupBoxResumen)
        self.labelProductos.setObjectName(u"labelProductos")

        self.formLayoutResumen.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelProductos)

        self.label_total_productos = QLabel(self.groupBoxResumen)
        self.label_total_productos.setObjectName(u"label_total_productos")

        self.formLayoutResumen.setWidget(2, QFormLayout.ItemRole.FieldRole, self.label_total_productos)

        self.labelReparaciones = QLabel(self.groupBoxResumen)
        self.labelReparaciones.setObjectName(u"labelReparaciones")

        self.formLayoutResumen.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelReparaciones)

        self.label_total_reparaciones = QLabel(self.groupBoxResumen)
        self.label_total_reparaciones.setObjectName(u"label_total_reparaciones")

        self.formLayoutResumen.setWidget(3, QFormLayout.ItemRole.FieldRole, self.label_total_reparaciones)


        self.verticalLayoutMain.addWidget(self.groupBoxResumen)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menuArchivo = QMenu(self.menubar)
        self.menuArchivo.setObjectName(u"menuArchivo")
        self.menuModulos = QMenu(self.menubar)
        self.menuModulos.setObjectName(u"menuModulos")
        self.menuVer = QMenu(self.menubar)
        self.menuVer.setObjectName(u"menuVer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuModulos.menuAction())
        self.menubar.addAction(self.menuVer.menuAction())
        self.menuArchivo.addAction(self.actionSalir)
        self.menuModulos.addAction(self.actionClientes)
        self.menuModulos.addAction(self.actionDispositivos)
        self.menuModulos.addAction(self.actionInventario)
        self.menuModulos.addAction(self.actionReparaciones)
        self.menuVer.addAction(self.actionTemaClaro)
        self.menuVer.addAction(self.actionTemaOscuro)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Inventario Base", None))
        self.actionSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.actionClientes.setText(QCoreApplication.translate("MainWindow", u"Clientes", None))
        self.actionDispositivos.setText(QCoreApplication.translate("MainWindow", u"Dispositivos", None))
        self.actionInventario.setText(QCoreApplication.translate("MainWindow", u"Inventario", None))
        self.actionReparaciones.setText(QCoreApplication.translate("MainWindow", u"Reparaciones", None))
        self.actionTemaClaro.setText(QCoreApplication.translate("MainWindow", u"Tema claro", None))
        self.actionTemaOscuro.setText(QCoreApplication.translate("MainWindow", u"Tema oscuro", None))
        self.groupBoxResumen.setTitle(QCoreApplication.translate("MainWindow", u"Resumen", None))
        self.labelClientes.setText(QCoreApplication.translate("MainWindow", u"Total clientes:", None))
        self.label_total_clientes.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labelDispositivos.setText(QCoreApplication.translate("MainWindow", u"Total dispositivos:", None))
        self.label_total_dispositivos.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labelProductos.setText(QCoreApplication.translate("MainWindow", u"Total productos:", None))
        self.label_total_productos.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labelReparaciones.setText(QCoreApplication.translate("MainWindow", u"Reparaciones pendientes:", None))
        self.label_total_reparaciones.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.menuArchivo.setTitle(QCoreApplication.translate("MainWindow", u"&Archivo", None))
        self.menuModulos.setTitle(QCoreApplication.translate("MainWindow", u"&M\u00f3dulos", None))
        self.menuVer.setTitle(QCoreApplication.translate("MainWindow", u"&Ver", None))
    # retranslateUi

