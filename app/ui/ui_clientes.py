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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFormLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QVBoxLayout, QWidget)

class Ui_ClientesDialog(object):
    def setupUi(self, ClientesDialog):
        if not ClientesDialog.objectName():
            ClientesDialog.setObjectName(u"ClientesDialog")
        self.verticalLayout = QVBoxLayout(ClientesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelNombre = QLabel(ClientesDialog)
        self.labelNombre.setObjectName(u"labelNombre")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelNombre)

        self.lineEditNombre = QLineEdit(ClientesDialog)
        self.lineEditNombre.setObjectName(u"lineEditNombre")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditNombre)

        self.labelTelefono = QLabel(ClientesDialog)
        self.labelTelefono.setObjectName(u"labelTelefono")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelTelefono)

        self.lineEditTelefono = QLineEdit(ClientesDialog)
        self.lineEditTelefono.setObjectName(u"lineEditTelefono")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEditTelefono)

        self.labelEmail = QLabel(ClientesDialog)
        self.labelEmail.setObjectName(u"labelEmail")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelEmail)

        self.lineEditEmail = QLineEdit(ClientesDialog)
        self.lineEditEmail.setObjectName(u"lineEditEmail")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEditEmail)

        self.labelDireccion = QLabel(ClientesDialog)
        self.labelDireccion.setObjectName(u"labelDireccion")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelDireccion)

        self.lineEditDireccion = QLineEdit(ClientesDialog)
        self.lineEditDireccion.setObjectName(u"lineEditDireccion")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineEditDireccion)

        self.labelNif = QLabel(ClientesDialog)
        self.labelNif.setObjectName(u"labelNif")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelNif)

        self.lineEditNif = QLineEdit(ClientesDialog)
        self.lineEditNif.setObjectName(u"lineEditNif")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.lineEditNif)

        self.labelNotas = QLabel(ClientesDialog)
        self.labelNotas.setObjectName(u"labelNotas")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelNotas)

        self.plainTextEditNotas = QPlainTextEdit(ClientesDialog)
        self.plainTextEditNotas.setObjectName(u"plainTextEditNotas")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.plainTextEditNotas)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayoutBtns = QHBoxLayout()
        self.horizontalLayoutBtns.setObjectName(u"horizontalLayoutBtns")
        self.btnAgregar = QPushButton(ClientesDialog)
        self.btnAgregar.setObjectName(u"btnAgregar")

        self.horizontalLayoutBtns.addWidget(self.btnAgregar)

        self.btnGuardar = QPushButton(ClientesDialog)
        self.btnGuardar.setObjectName(u"btnGuardar")

        self.horizontalLayoutBtns.addWidget(self.btnGuardar)


        self.verticalLayout.addLayout(self.horizontalLayoutBtns)

        self.tableClientes = QTableView(ClientesDialog)
        self.tableClientes.setObjectName(u"tableClientes")
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
        self.labelNombre.setText(QCoreApplication.translate("ClientesDialog", u"Nombre", None))
        self.labelTelefono.setText(QCoreApplication.translate("ClientesDialog", u"Tel\u00e9fono", None))
        self.labelEmail.setText(QCoreApplication.translate("ClientesDialog", u"Email", None))
        self.labelDireccion.setText(QCoreApplication.translate("ClientesDialog", u"Direcci\u00f3n", None))
        self.labelNif.setText(QCoreApplication.translate("ClientesDialog", u"NIF", None))
        self.labelNotas.setText(QCoreApplication.translate("ClientesDialog", u"Notas", None))
        self.btnAgregar.setText(QCoreApplication.translate("ClientesDialog", u"Agregar", None))
        self.btnGuardar.setText(QCoreApplication.translate("ClientesDialog", u"Guardar cambios", None))
        self.btnEliminar.setText(QCoreApplication.translate("ClientesDialog", u"Eliminar", None))
        self.btnCerrar.setText(QCoreApplication.translate("ClientesDialog", u"Cerrar", None))
    # retranslateUi

