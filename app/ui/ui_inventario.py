# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'inventario.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QDoubleSpinBox, QGridLayout, QHBoxLayout, QHeaderView,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTableView, QVBoxLayout, QWidget)

class Ui_InventarioDialog(object):
    def setupUi(self, InventarioDialog):
        if not InventarioDialog.objectName():
            InventarioDialog.setObjectName(u"InventarioDialog")
        self.verticalLayout = QVBoxLayout(InventarioDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutInputs = QGridLayout()
        self.layoutInputs.setObjectName(u"layoutInputs")
        self.lineEditSKU = QLineEdit(InventarioDialog)
        self.lineEditSKU.setObjectName(u"lineEditSKU")

        self.layoutInputs.addWidget(self.lineEditSKU, 0, 0, 1, 1)

        self.lineEditNombre = QLineEdit(InventarioDialog)
        self.lineEditNombre.setObjectName(u"lineEditNombre")

        self.layoutInputs.addWidget(self.lineEditNombre, 0, 1, 1, 1)

        self.comboCategoria = QComboBox(InventarioDialog)
        self.comboCategoria.setObjectName(u"comboCategoria")
        self.comboCategoria.setEditable(True)

        self.layoutInputs.addWidget(self.comboCategoria, 0, 2, 1, 1)

        self.spinCantidad = QSpinBox(InventarioDialog)
        self.spinCantidad.setObjectName(u"spinCantidad")
        self.spinCantidad.setMinimum(0)

        self.layoutInputs.addWidget(self.spinCantidad, 0, 3, 1, 1)

        self.spinStockMin = QSpinBox(InventarioDialog)
        self.spinStockMin.setObjectName(u"spinStockMin")
        self.spinStockMin.setMinimum(0)

        self.layoutInputs.addWidget(self.spinStockMin, 0, 4, 1, 1)

        self.doubleCosto = QDoubleSpinBox(InventarioDialog)
        self.doubleCosto.setObjectName(u"doubleCosto")
        self.doubleCosto.setDecimals(2)
        self.doubleCosto.setMinimum(0.000000000000000)

        self.layoutInputs.addWidget(self.doubleCosto, 1, 0, 1, 1)

        self.doublePrecio = QDoubleSpinBox(InventarioDialog)
        self.doublePrecio.setObjectName(u"doublePrecio")
        self.doublePrecio.setDecimals(2)
        self.doublePrecio.setMinimum(0.000000000000000)

        self.layoutInputs.addWidget(self.doublePrecio, 1, 1, 1, 1)

        self.lineUbicacion = QLineEdit(InventarioDialog)
        self.lineUbicacion.setObjectName(u"lineUbicacion")

        self.layoutInputs.addWidget(self.lineUbicacion, 1, 2, 1, 1)

        self.lineProveedor = QLineEdit(InventarioDialog)
        self.lineProveedor.setObjectName(u"lineProveedor")

        self.layoutInputs.addWidget(self.lineProveedor, 1, 3, 1, 1)

        self.btnAgregar = QPushButton(InventarioDialog)
        self.btnAgregar.setObjectName(u"btnAgregar")

        self.layoutInputs.addWidget(self.btnAgregar, 1, 4, 1, 1)


        self.verticalLayout.addLayout(self.layoutInputs)

        self.tableProductos = QTableView(InventarioDialog)
        self.tableProductos.setObjectName(u"tableProductos")
        self.tableProductos.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.tableProductos)

        self.layoutButtons = QHBoxLayout()
        self.layoutButtons.setObjectName(u"layoutButtons")
        self.btnEliminar = QPushButton(InventarioDialog)
        self.btnEliminar.setObjectName(u"btnEliminar")

        self.layoutButtons.addWidget(self.btnEliminar)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutButtons.addItem(self.horizontalSpacer)

        self.btnCerrar = QPushButton(InventarioDialog)
        self.btnCerrar.setObjectName(u"btnCerrar")

        self.layoutButtons.addWidget(self.btnCerrar)


        self.verticalLayout.addLayout(self.layoutButtons)


        self.retranslateUi(InventarioDialog)

        QMetaObject.connectSlotsByName(InventarioDialog)
    # setupUi

    def retranslateUi(self, InventarioDialog):
        InventarioDialog.setWindowTitle(QCoreApplication.translate("InventarioDialog", u"Inventario", None))
        self.btnAgregar.setText(QCoreApplication.translate("InventarioDialog", u"Agregar", None))
        self.btnEliminar.setText(QCoreApplication.translate("InventarioDialog", u"Eliminar", None))
        self.btnCerrar.setText(QCoreApplication.translate("InventarioDialog", u"Cerrar", None))
    # retranslateUi

