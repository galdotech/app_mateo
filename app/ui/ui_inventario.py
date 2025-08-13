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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_InventarioDialog(object):
    def setupUi(self, InventarioDialog):
        if not InventarioDialog.objectName():
            InventarioDialog.setObjectName(u"InventarioDialog")
        self.verticalLayout = QVBoxLayout(InventarioDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutInputs = QHBoxLayout()
        self.layoutInputs.setObjectName(u"layoutInputs")
        self.lineEditNombre = QLineEdit(InventarioDialog)
        self.lineEditNombre.setObjectName(u"lineEditNombre")

        self.layoutInputs.addWidget(self.lineEditNombre)

        self.spinCantidad = QSpinBox(InventarioDialog)
        self.spinCantidad.setObjectName(u"spinCantidad")
        self.spinCantidad.setMinimum(0)

        self.layoutInputs.addWidget(self.spinCantidad)

        self.btnAgregar = QPushButton(InventarioDialog)
        self.btnAgregar.setObjectName(u"btnAgregar")

        self.layoutInputs.addWidget(self.btnAgregar)


        self.verticalLayout.addLayout(self.layoutInputs)

        self.tableProductos = QTableWidget(InventarioDialog)
        if (self.tableProductos.columnCount() < 2):
            self.tableProductos.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableProductos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableProductos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableProductos.setObjectName(u"tableProductos")
        self.tableProductos.setColumnCount(2)
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
        ___qtablewidgetitem = self.tableProductos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("InventarioDialog", u"Nombre", None));
        ___qtablewidgetitem1 = self.tableProductos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("InventarioDialog", u"Cantidad", None));
        self.btnEliminar.setText(QCoreApplication.translate("InventarioDialog", u"Eliminar", None))
        self.btnCerrar.setText(QCoreApplication.translate("InventarioDialog", u"Cerrar", None))
    # retranslateUi

