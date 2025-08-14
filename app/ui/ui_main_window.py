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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

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
        self.actionActualizar = QAction(MainWindow)
        self.actionActualizar.setObjectName(u"actionActualizar")
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

        self.groupBoxAcciones = QGroupBox(self.centralwidget)
        self.groupBoxAcciones.setObjectName(u"groupBoxAcciones")
        self.horizontalLayoutAcciones = QHBoxLayout(self.groupBoxAcciones)
        self.horizontalLayoutAcciones.setObjectName(u"horizontalLayoutAcciones")
        self.btnClientes = QPushButton(self.groupBoxAcciones)
        self.btnClientes.setObjectName(u"btnClientes")

        self.horizontalLayoutAcciones.addWidget(self.btnClientes)

        self.btnDispositivos = QPushButton(self.groupBoxAcciones)
        self.btnDispositivos.setObjectName(u"btnDispositivos")

        self.horizontalLayoutAcciones.addWidget(self.btnDispositivos)

        self.btnInventario = QPushButton(self.groupBoxAcciones)
        self.btnInventario.setObjectName(u"btnInventario")

        self.horizontalLayoutAcciones.addWidget(self.btnInventario)

        self.btnNuevaReparacion = QPushButton(self.groupBoxAcciones)
        self.btnNuevaReparacion.setObjectName(u"btnNuevaReparacion")

        self.horizontalLayoutAcciones.addWidget(self.btnNuevaReparacion)

        self.btnActualizar = QPushButton(self.groupBoxAcciones)
        self.btnActualizar.setObjectName(u"btnActualizar")

        self.horizontalLayoutAcciones.addWidget(self.btnActualizar)


        self.verticalLayoutMain.addWidget(self.groupBoxAcciones)

        self.horizontalLayoutTablas = QHBoxLayout()
        self.horizontalLayoutTablas.setObjectName(u"horizontalLayoutTablas")
        self.groupBoxLowStock = QGroupBox(self.centralwidget)
        self.groupBoxLowStock.setObjectName(u"groupBoxLowStock")
        self.verticalLayoutLowStock = QVBoxLayout(self.groupBoxLowStock)
        self.verticalLayoutLowStock.setObjectName(u"verticalLayoutLowStock")
        self.tableLowStock = QTableWidget(self.groupBoxLowStock)
        if (self.tableLowStock.columnCount() < 2):
            self.tableLowStock.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableLowStock.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableLowStock.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableLowStock.setObjectName(u"tableLowStock")

        self.verticalLayoutLowStock.addWidget(self.tableLowStock)


        self.horizontalLayoutTablas.addWidget(self.groupBoxLowStock)

        self.groupBoxRecentRepairs = QGroupBox(self.centralwidget)
        self.groupBoxRecentRepairs.setObjectName(u"groupBoxRecentRepairs")
        self.verticalLayoutRecent = QVBoxLayout(self.groupBoxRecentRepairs)
        self.verticalLayoutRecent.setObjectName(u"verticalLayoutRecent")
        self.tableRecentRepairs = QTableWidget(self.groupBoxRecentRepairs)
        if (self.tableRecentRepairs.columnCount() < 5):
            self.tableRecentRepairs.setColumnCount(5)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableRecentRepairs.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableRecentRepairs.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableRecentRepairs.setHorizontalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableRecentRepairs.setHorizontalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableRecentRepairs.setHorizontalHeaderItem(4, __qtablewidgetitem6)
        self.tableRecentRepairs.setObjectName(u"tableRecentRepairs")

        self.verticalLayoutRecent.addWidget(self.tableRecentRepairs)


        self.horizontalLayoutTablas.addWidget(self.groupBoxRecentRepairs)


        self.verticalLayoutMain.addLayout(self.horizontalLayoutTablas)

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
        self.menuVer.addAction(self.actionActualizar)

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
        self.actionActualizar.setText(QCoreApplication.translate("MainWindow", u"Actualizar", None))
#if QT_CONFIG(shortcut)
        self.actionActualizar.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.groupBoxResumen.setTitle(QCoreApplication.translate("MainWindow", u"Resumen", None))
        self.labelClientes.setText(QCoreApplication.translate("MainWindow", u"Total clientes:", None))
        self.label_total_clientes.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labelDispositivos.setText(QCoreApplication.translate("MainWindow", u"Total dispositivos:", None))
        self.label_total_dispositivos.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labelProductos.setText(QCoreApplication.translate("MainWindow", u"Total productos:", None))
        self.label_total_productos.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labelReparaciones.setText(QCoreApplication.translate("MainWindow", u"Reparaciones pendientes:", None))
        self.label_total_reparaciones.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBoxAcciones.setTitle(QCoreApplication.translate("MainWindow", u"Acciones r\u00e1pidas", None))
        self.btnClientes.setText(QCoreApplication.translate("MainWindow", u"Clientes", None))
        self.btnDispositivos.setText(QCoreApplication.translate("MainWindow", u"Dispositivos", None))
        self.btnInventario.setText(QCoreApplication.translate("MainWindow", u"Inventario", None))
        self.btnNuevaReparacion.setText(QCoreApplication.translate("MainWindow", u"Nueva reparaci\u00f3n", None))
        self.btnActualizar.setText(QCoreApplication.translate("MainWindow", u"Actualizar", None))
        self.groupBoxLowStock.setTitle(QCoreApplication.translate("MainWindow", u"Alertas de inventario (agotados o casi)", None))
        ___qtablewidgetitem = self.tableLowStock.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Producto", None));
        ___qtablewidgetitem1 = self.tableLowStock.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Cantidad", None));
        self.groupBoxRecentRepairs.setTitle(QCoreApplication.translate("MainWindow", u"\u00daltimas reparaciones", None))
        ___qtablewidgetitem2 = self.tableRecentRepairs.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Fecha", None));
        ___qtablewidgetitem3 = self.tableRecentRepairs.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Cliente", None));
        ___qtablewidgetitem4 = self.tableRecentRepairs.horizontalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Dispositivo", None));
        ___qtablewidgetitem5 = self.tableRecentRepairs.horizontalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Estado", None));
        ___qtablewidgetitem6 = self.tableRecentRepairs.horizontalHeaderItem(4)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Costo", None));
        self.menuArchivo.setTitle(QCoreApplication.translate("MainWindow", u"&Archivo", None))
        self.menuModulos.setTitle(QCoreApplication.translate("MainWindow", u"&M\u00f3dulos", None))
        self.menuVer.setTitle(QCoreApplication.translate("MainWindow", u"&Ver", None))
    # retranslateUi

