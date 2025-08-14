# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dispositivos.ui'
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
    QHBoxLayout, QHeaderView, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)

class Ui_DispositivosDialog(object):
    def setupUi(self, DispositivosDialog):
        if not DispositivosDialog.objectName():
            DispositivosDialog.setObjectName(u"DispositivosDialog")
        self.verticalLayout = QVBoxLayout(DispositivosDialog)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.layoutInputs = QHBoxLayout()
        self.layoutInputs.setSpacing(12)
        self.layoutInputs.setObjectName(u"layoutInputs")
        self.comboCliente = QComboBox(DispositivosDialog)
        self.comboCliente.setObjectName(u"comboCliente")

        self.layoutInputs.addWidget(self.comboCliente)

        self.lineEditMarca = QLineEdit(DispositivosDialog)
        self.lineEditMarca.setObjectName(u"lineEditMarca")

        self.layoutInputs.addWidget(self.lineEditMarca)

        self.lineEditModelo = QLineEdit(DispositivosDialog)
        self.lineEditModelo.setObjectName(u"lineEditModelo")

        self.layoutInputs.addWidget(self.lineEditModelo)

        self.lineEditIMEI = QLineEdit(DispositivosDialog)
        self.lineEditIMEI.setObjectName(u"lineEditIMEI")

        self.layoutInputs.addWidget(self.lineEditIMEI)

        self.lineEditSerie = QLineEdit(DispositivosDialog)
        self.lineEditSerie.setObjectName(u"lineEditSerie")

        self.layoutInputs.addWidget(self.lineEditSerie)

        self.lineEditColor = QLineEdit(DispositivosDialog)
        self.lineEditColor.setObjectName(u"lineEditColor")

        self.layoutInputs.addWidget(self.lineEditColor)

        self.lineEditAccesorios = QLineEdit(DispositivosDialog)
        self.lineEditAccesorios.setObjectName(u"lineEditAccesorios")

        self.layoutInputs.addWidget(self.lineEditAccesorios)

        self.btnAgregar = QPushButton(DispositivosDialog)
        self.btnAgregar.setObjectName(u"btnAgregar")

        self.layoutInputs.addWidget(self.btnAgregar)


        self.verticalLayout.addLayout(self.layoutInputs)

        self.tableDispositivos = QTableView(DispositivosDialog)
        self.tableDispositivos.setObjectName(u"tableDispositivos")
        self.tableDispositivos.setAlternatingRowColors(True)
        self.tableDispositivos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableDispositivos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableDispositivos.setSortingEnabled(True)
        self.tableDispositivos.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableDispositivos)

        self.layoutButtons = QHBoxLayout()
        self.layoutButtons.setObjectName(u"layoutButtons")
        self.btnEliminar = QPushButton(DispositivosDialog)
        self.btnEliminar.setObjectName(u"btnEliminar")

        self.layoutButtons.addWidget(self.btnEliminar)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutButtons.addItem(self.horizontalSpacer)

        self.btnCerrar = QPushButton(DispositivosDialog)
        self.btnCerrar.setObjectName(u"btnCerrar")

        self.layoutButtons.addWidget(self.btnCerrar)


        self.verticalLayout.addLayout(self.layoutButtons)

        QWidget.setTabOrder(self.comboCliente, self.lineEditMarca)
        QWidget.setTabOrder(self.lineEditMarca, self.lineEditModelo)
        QWidget.setTabOrder(self.lineEditModelo, self.lineEditIMEI)
        QWidget.setTabOrder(self.lineEditIMEI, self.lineEditSerie)
        QWidget.setTabOrder(self.lineEditSerie, self.lineEditColor)
        QWidget.setTabOrder(self.lineEditColor, self.lineEditAccesorios)
        QWidget.setTabOrder(self.lineEditAccesorios, self.btnAgregar)
        QWidget.setTabOrder(self.btnAgregar, self.tableDispositivos)
        QWidget.setTabOrder(self.tableDispositivos, self.btnEliminar)
        QWidget.setTabOrder(self.btnEliminar, self.btnCerrar)

        self.retranslateUi(DispositivosDialog)

        QMetaObject.connectSlotsByName(DispositivosDialog)
    # setupUi

    def retranslateUi(self, DispositivosDialog):
        DispositivosDialog.setWindowTitle(QCoreApplication.translate("DispositivosDialog", u"Dispositivos", None))
#if QT_CONFIG(accessibility)
        self.comboCliente.setAccessibleName(QCoreApplication.translate("DispositivosDialog", u"cliente", None))
#endif // QT_CONFIG(accessibility)
        self.lineEditMarca.setPlaceholderText(QCoreApplication.translate("DispositivosDialog", u"Marca", None))
#if QT_CONFIG(accessibility)
        self.lineEditMarca.setAccessibleName(QCoreApplication.translate("DispositivosDialog", u"marca", None))
#endif // QT_CONFIG(accessibility)
        self.lineEditModelo.setPlaceholderText(QCoreApplication.translate("DispositivosDialog", u"Modelo", None))
#if QT_CONFIG(accessibility)
        self.lineEditModelo.setAccessibleName(QCoreApplication.translate("DispositivosDialog", u"modelo", None))
#endif // QT_CONFIG(accessibility)
        self.lineEditIMEI.setPlaceholderText(QCoreApplication.translate("DispositivosDialog", u"IMEI", None))
        self.lineEditSerie.setPlaceholderText(QCoreApplication.translate("DispositivosDialog", u"N\u00b0 Serie", None))
        self.lineEditColor.setPlaceholderText(QCoreApplication.translate("DispositivosDialog", u"Color", None))
        self.lineEditAccesorios.setPlaceholderText(QCoreApplication.translate("DispositivosDialog", u"Accesorios", None))
        self.btnAgregar.setText(QCoreApplication.translate("DispositivosDialog", u"Agregar", None))
        self.btnEliminar.setText(QCoreApplication.translate("DispositivosDialog", u"Eliminar", None))
        self.btnCerrar.setText(QCoreApplication.translate("DispositivosDialog", u"Cerrar", None))
    # retranslateUi

