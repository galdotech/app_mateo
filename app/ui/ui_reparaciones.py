# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reparaciones.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ReparacionesDialog(object):
    def setupUi(self, ReparacionesDialog):
        if not ReparacionesDialog.objectName():
            ReparacionesDialog.setObjectName(u"ReparacionesDialog")
        self.verticalLayout = QVBoxLayout(ReparacionesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelCliente = QLabel(ReparacionesDialog)
        self.labelCliente.setObjectName(u"labelCliente")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCliente)

        self.lineEditCliente = QLineEdit(ReparacionesDialog)
        self.lineEditCliente.setObjectName(u"lineEditCliente")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditCliente)

        self.labelMarca = QLabel(ReparacionesDialog)
        self.labelMarca.setObjectName(u"labelMarca")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelMarca)

        self.lineEditMarca = QLineEdit(ReparacionesDialog)
        self.lineEditMarca.setObjectName(u"lineEditMarca")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEditMarca)

        self.labelModelo = QLabel(ReparacionesDialog)
        self.labelModelo.setObjectName(u"labelModelo")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelModelo)

        self.lineEditModelo = QLineEdit(ReparacionesDialog)
        self.lineEditModelo.setObjectName(u"lineEditModelo")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEditModelo)

        self.labelDescripcion = QLabel(ReparacionesDialog)
        self.labelDescripcion.setObjectName(u"labelDescripcion")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelDescripcion)

        self.plainTextDescripcion = QPlainTextEdit(ReparacionesDialog)
        self.plainTextDescripcion.setObjectName(u"plainTextDescripcion")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.plainTextDescripcion)

        self.labelEstado = QLabel(ReparacionesDialog)
        self.labelEstado.setObjectName(u"labelEstado")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelEstado)

        self.comboEstado = QComboBox(ReparacionesDialog)
        self.comboEstado.addItem("")
        self.comboEstado.addItem("")
        self.comboEstado.setObjectName(u"comboEstado")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.comboEstado)

        self.labelCosto = QLabel(ReparacionesDialog)
        self.labelCosto.setObjectName(u"labelCosto")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelCosto)

        self.inputCosto = QLineEdit(ReparacionesDialog)
        self.inputCosto.setObjectName(u"inputCosto")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.inputCosto)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonsLayout.addItem(self.horizontalSpacer)

        self.btnGuardar = QPushButton(ReparacionesDialog)
        self.btnGuardar.setObjectName(u"btnGuardar")

        self.buttonsLayout.addWidget(self.btnGuardar)

        self.btnCancelar = QPushButton(ReparacionesDialog)
        self.btnCancelar.setObjectName(u"btnCancelar")

        self.buttonsLayout.addWidget(self.btnCancelar)


        self.verticalLayout.addLayout(self.buttonsLayout)


        self.retranslateUi(ReparacionesDialog)

        QMetaObject.connectSlotsByName(ReparacionesDialog)
    # setupUi

    def retranslateUi(self, ReparacionesDialog):
        ReparacionesDialog.setWindowTitle(QCoreApplication.translate("ReparacionesDialog", u"Nueva Reparaci\u00f3n", None))
        self.labelCliente.setText(QCoreApplication.translate("ReparacionesDialog", u"Cliente", None))
        self.labelMarca.setText(QCoreApplication.translate("ReparacionesDialog", u"Marca", None))
        self.labelModelo.setText(QCoreApplication.translate("ReparacionesDialog", u"Modelo", None))
        self.labelDescripcion.setText(QCoreApplication.translate("ReparacionesDialog", u"Descripci\u00f3n", None))
        self.labelEstado.setText(QCoreApplication.translate("ReparacionesDialog", u"Estado", None))
        self.comboEstado.setItemText(0, QCoreApplication.translate("ReparacionesDialog", u"Pendiente", None))
        self.comboEstado.setItemText(1, QCoreApplication.translate("ReparacionesDialog", u"Finalizada", None))

        self.labelCosto.setText(QCoreApplication.translate("ReparacionesDialog", u"Costo", None))
        self.inputCosto.setPlaceholderText(QCoreApplication.translate("ReparacionesDialog", u"0.00", None))
        self.btnGuardar.setText(QCoreApplication.translate("ReparacionesDialog", u"Guardar", None))
        self.btnCancelar.setText(QCoreApplication.translate("ReparacionesDialog", u"Cancelar", None))
    # retranslateUi

