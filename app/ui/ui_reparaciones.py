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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

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

        self.labelDiagnostico = QLabel(ReparacionesDialog)
        self.labelDiagnostico.setObjectName(u"labelDiagnostico")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelDiagnostico)

        self.plainTextDiagnostico = QPlainTextEdit(ReparacionesDialog)
        self.plainTextDiagnostico.setObjectName(u"plainTextDiagnostico")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.plainTextDiagnostico)

        self.labelAcciones = QLabel(ReparacionesDialog)
        self.labelAcciones.setObjectName(u"labelAcciones")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelAcciones)

        self.plainTextAcciones = QPlainTextEdit(ReparacionesDialog)
        self.plainTextAcciones.setObjectName(u"plainTextAcciones")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.plainTextAcciones)

        self.labelPiezas = QLabel(ReparacionesDialog)
        self.labelPiezas.setObjectName(u"labelPiezas")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.labelPiezas)

        self.plainTextPiezas = QPlainTextEdit(ReparacionesDialog)
        self.plainTextPiezas.setObjectName(u"plainTextPiezas")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.plainTextPiezas)

        self.labelEstado = QLabel(ReparacionesDialog)
        self.labelEstado.setObjectName(u"labelEstado")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.labelEstado)

        self.comboEstado = QComboBox(ReparacionesDialog)
        self.comboEstado.addItem("")
        self.comboEstado.addItem("")
        self.comboEstado.addItem("")
        self.comboEstado.setObjectName(u"comboEstado")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.comboEstado)

        self.labelPrioridad = QLabel(ReparacionesDialog)
        self.labelPrioridad.setObjectName(u"labelPrioridad")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.labelPrioridad)

        self.comboPrioridad = QComboBox(ReparacionesDialog)
        self.comboPrioridad.addItem("")
        self.comboPrioridad.addItem("")
        self.comboPrioridad.addItem("")
        self.comboPrioridad.setObjectName(u"comboPrioridad")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.comboPrioridad)

        self.labelManoObra = QLabel(ReparacionesDialog)
        self.labelManoObra.setObjectName(u"labelManoObra")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.labelManoObra)

        self.doubleSpinBoxManoObra = QDoubleSpinBox(ReparacionesDialog)
        self.doubleSpinBoxManoObra.setObjectName(u"doubleSpinBoxManoObra")
        self.doubleSpinBoxManoObra.setMinimum(0.000000000000000)
        self.doubleSpinBoxManoObra.setMaximum(999999999.000000000000000)
        self.doubleSpinBoxManoObra.setDecimals(2)

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.doubleSpinBoxManoObra)

        self.labelCostoPiezas = QLabel(ReparacionesDialog)
        self.labelCostoPiezas.setObjectName(u"labelCostoPiezas")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.labelCostoPiezas)

        self.doubleSpinBoxCostoPiezas = QDoubleSpinBox(ReparacionesDialog)
        self.doubleSpinBoxCostoPiezas.setObjectName(u"doubleSpinBoxCostoPiezas")
        self.doubleSpinBoxCostoPiezas.setMinimum(0.000000000000000)
        self.doubleSpinBoxCostoPiezas.setMaximum(999999999.000000000000000)
        self.doubleSpinBoxCostoPiezas.setDecimals(2)

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.doubleSpinBoxCostoPiezas)

        self.labelDeposito = QLabel(ReparacionesDialog)
        self.labelDeposito.setObjectName(u"labelDeposito")

        self.formLayout.setWidget(10, QFormLayout.ItemRole.LabelRole, self.labelDeposito)

        self.doubleSpinBoxDeposito = QDoubleSpinBox(ReparacionesDialog)
        self.doubleSpinBoxDeposito.setObjectName(u"doubleSpinBoxDeposito")
        self.doubleSpinBoxDeposito.setMinimum(0.000000000000000)
        self.doubleSpinBoxDeposito.setMaximum(999999999.000000000000000)
        self.doubleSpinBoxDeposito.setDecimals(2)

        self.formLayout.setWidget(10, QFormLayout.ItemRole.FieldRole, self.doubleSpinBoxDeposito)

        self.labelTotal = QLabel(ReparacionesDialog)
        self.labelTotal.setObjectName(u"labelTotal")

        self.formLayout.setWidget(11, QFormLayout.ItemRole.LabelRole, self.labelTotal)

        self.doubleSpinBoxTotal = QDoubleSpinBox(ReparacionesDialog)
        self.doubleSpinBoxTotal.setObjectName(u"doubleSpinBoxTotal")
        self.doubleSpinBoxTotal.setMinimum(0.000000000000000)
        self.doubleSpinBoxTotal.setMaximum(999999999.000000000000000)
        self.doubleSpinBoxTotal.setDecimals(2)
        self.doubleSpinBoxTotal.setReadOnly(True)

        self.formLayout.setWidget(11, QFormLayout.ItemRole.FieldRole, self.doubleSpinBoxTotal)

        self.labelSaldo = QLabel(ReparacionesDialog)
        self.labelSaldo.setObjectName(u"labelSaldo")

        self.formLayout.setWidget(12, QFormLayout.ItemRole.LabelRole, self.labelSaldo)

        self.doubleSpinBoxSaldo = QDoubleSpinBox(ReparacionesDialog)
        self.doubleSpinBoxSaldo.setObjectName(u"doubleSpinBoxSaldo")
        self.doubleSpinBoxSaldo.setMinimum(0.000000000000000)
        self.doubleSpinBoxSaldo.setMaximum(999999999.000000000000000)
        self.doubleSpinBoxSaldo.setDecimals(2)
        self.doubleSpinBoxSaldo.setReadOnly(True)

        self.formLayout.setWidget(12, QFormLayout.ItemRole.FieldRole, self.doubleSpinBoxSaldo)

        self.labelTecnico = QLabel(ReparacionesDialog)
        self.labelTecnico.setObjectName(u"labelTecnico")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.LabelRole, self.labelTecnico)

        self.lineEditTecnico = QLineEdit(ReparacionesDialog)
        self.lineEditTecnico.setObjectName(u"lineEditTecnico")

        self.formLayout.setWidget(13, QFormLayout.ItemRole.FieldRole, self.lineEditTecnico)

        self.labelGarantia = QLabel(ReparacionesDialog)
        self.labelGarantia.setObjectName(u"labelGarantia")

        self.formLayout.setWidget(14, QFormLayout.ItemRole.LabelRole, self.labelGarantia)

        self.spinBoxGarantia = QSpinBox(ReparacionesDialog)
        self.spinBoxGarantia.setObjectName(u"spinBoxGarantia")
        self.spinBoxGarantia.setMinimum(0)
        self.spinBoxGarantia.setMaximum(9999)

        self.formLayout.setWidget(14, QFormLayout.ItemRole.FieldRole, self.spinBoxGarantia)

        self.labelPassBloqueo = QLabel(ReparacionesDialog)
        self.labelPassBloqueo.setObjectName(u"labelPassBloqueo")

        self.formLayout.setWidget(15, QFormLayout.ItemRole.LabelRole, self.labelPassBloqueo)

        self.lineEditPassBloqueo = QLineEdit(ReparacionesDialog)
        self.lineEditPassBloqueo.setObjectName(u"lineEditPassBloqueo")
        self.lineEditPassBloqueo.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(15, QFormLayout.ItemRole.FieldRole, self.lineEditPassBloqueo)

        self.labelRespaldo = QLabel(ReparacionesDialog)
        self.labelRespaldo.setObjectName(u"labelRespaldo")

        self.formLayout.setWidget(16, QFormLayout.ItemRole.LabelRole, self.labelRespaldo)

        self.checkBoxRespaldo = QCheckBox(ReparacionesDialog)
        self.checkBoxRespaldo.setObjectName(u"checkBoxRespaldo")

        self.formLayout.setWidget(16, QFormLayout.ItemRole.FieldRole, self.checkBoxRespaldo)

        self.labelAccesorios = QLabel(ReparacionesDialog)
        self.labelAccesorios.setObjectName(u"labelAccesorios")

        self.formLayout.setWidget(17, QFormLayout.ItemRole.LabelRole, self.labelAccesorios)

        self.lineEditAccesorios = QLineEdit(ReparacionesDialog)
        self.lineEditAccesorios.setObjectName(u"lineEditAccesorios")

        self.formLayout.setWidget(17, QFormLayout.ItemRole.FieldRole, self.lineEditAccesorios)


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
        self.labelDiagnostico.setText(QCoreApplication.translate("ReparacionesDialog", u"Diagn\u00f3stico", None))
        self.labelAcciones.setText(QCoreApplication.translate("ReparacionesDialog", u"Acciones", None))
        self.labelPiezas.setText(QCoreApplication.translate("ReparacionesDialog", u"Piezas usadas", None))
        self.labelEstado.setText(QCoreApplication.translate("ReparacionesDialog", u"Estado", None))
        self.comboEstado.setItemText(0, QCoreApplication.translate("ReparacionesDialog", u"Pendiente", None))
        self.comboEstado.setItemText(1, QCoreApplication.translate("ReparacionesDialog", u"Finalizada", None))
        self.comboEstado.setItemText(2, QCoreApplication.translate("ReparacionesDialog", u"En curso", None))

        self.labelPrioridad.setText(QCoreApplication.translate("ReparacionesDialog", u"Prioridad", None))
        self.comboPrioridad.setItemText(0, QCoreApplication.translate("ReparacionesDialog", u"Baja", None))
        self.comboPrioridad.setItemText(1, QCoreApplication.translate("ReparacionesDialog", u"Normal", None))
        self.comboPrioridad.setItemText(2, QCoreApplication.translate("ReparacionesDialog", u"Alta", None))

        self.labelManoObra.setText(QCoreApplication.translate("ReparacionesDialog", u"Costo mano de obra", None))
        self.labelCostoPiezas.setText(QCoreApplication.translate("ReparacionesDialog", u"Costo piezas", None))
        self.labelDeposito.setText(QCoreApplication.translate("ReparacionesDialog", u"Dep\u00f3sito", None))
        self.labelTotal.setText(QCoreApplication.translate("ReparacionesDialog", u"Total", None))
        self.labelSaldo.setText(QCoreApplication.translate("ReparacionesDialog", u"Saldo", None))
        self.labelTecnico.setText(QCoreApplication.translate("ReparacionesDialog", u"T\u00e9cnico", None))
        self.labelGarantia.setText(QCoreApplication.translate("ReparacionesDialog", u"Garant\u00eda d\u00edas", None))
        self.labelPassBloqueo.setText(QCoreApplication.translate("ReparacionesDialog", u"Pass bloqueo", None))
        self.labelRespaldo.setText(QCoreApplication.translate("ReparacionesDialog", u"Respaldo datos", None))
        self.labelAccesorios.setText(QCoreApplication.translate("ReparacionesDialog", u"Accesorios entregados", None))
        self.btnGuardar.setText(QCoreApplication.translate("ReparacionesDialog", u"Guardar", None))
        self.btnCancelar.setText(QCoreApplication.translate("ReparacionesDialog", u"Cancelar", None))
    # retranslateUi

