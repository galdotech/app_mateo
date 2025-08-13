# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clientes.ui'
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
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_ClientesDialog(object):
    def setupUi(self, ClientesDialog):
        if not ClientesDialog.objectName():
            ClientesDialog.setObjectName(u"ClientesDialog")
        self.verticalLayout = QVBoxLayout(ClientesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditNombre = QLineEdit(ClientesDialog)
        self.lineEditNombre.setObjectName(u"lineEditNombre")

        self.horizontalLayout.addWidget(self.lineEditNombre)

        self.btnAgregar = QPushButton(ClientesDialog)
        self.btnAgregar.setObjectName(u"btnAgregar")

        self.horizontalLayout.addWidget(self.btnAgregar)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableClientes = QTableWidget(ClientesDialog)
        if (self.tableClientes.columnCount() < 2):
            self.tableClientes.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableClientes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableClientes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableClientes.setObjectName(u"tableClientes")
        self.tableClientes.setColumnCount(2)
        self.tableClientes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableClientes.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addWidget(self.tableClientes)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnEliminar = QPushButton(ClientesDialog)
        self.btnEliminar.setObjectName(u"btnEliminar")

        self.horizontalLayout_2.addWidget(self.btnEliminar)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btnCerrar = QPushButton(ClientesDialog)
        self.btnCerrar.setObjectName(u"btnCerrar")

        self.horizontalLayout_2.addWidget(self.btnCerrar)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ClientesDialog)

        QMetaObject.connectSlotsByName(ClientesDialog)
    # setupUi

    def retranslateUi(self, ClientesDialog):
        ClientesDialog.setWindowTitle(QCoreApplication.translate("ClientesDialog", u"Clientes", None))
        self.btnAgregar.setText(QCoreApplication.translate("ClientesDialog", u"Agregar", None))
        ___qtablewidgetitem = self.tableClientes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ClientesDialog", u"ID", None));
        ___qtablewidgetitem1 = self.tableClientes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ClientesDialog", u"Nombre", None));
        self.btnEliminar.setText(QCoreApplication.translate("ClientesDialog", u"Eliminar", None))
        self.btnCerrar.setText(QCoreApplication.translate("ClientesDialog", u"Cerrar", None))
    # retranslateUi

