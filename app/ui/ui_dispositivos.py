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
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_DispositivosDialog(object):
    def setupUi(self, DispositivosDialog):
        if not DispositivosDialog.objectName():
            DispositivosDialog.setObjectName(u"DispositivosDialog")
        self.verticalLayout = QVBoxLayout(DispositivosDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutInputs = QHBoxLayout()
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

        self.tableDispositivos = QTableWidget(DispositivosDialog)
        if (self.tableDispositivos.columnCount() < 7):
            self.tableDispositivos.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableDispositivos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableDispositivos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableDispositivos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableDispositivos.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableDispositivos.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableDispositivos.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableDispositivos.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tableDispositivos.setObjectName(u"tableDispositivos")
        self.tableDispositivos.setColumnCount(7)
        self.tableDispositivos.setSelectionBehavior(QAbstractItemView.SelectRows)

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


        self.retranslateUi(DispositivosDialog)

        QMetaObject.connectSlotsByName(DispositivosDialog)
    # setupUi

    def retranslateUi(self, DispositivosDialog):
        DispositivosDialog.setWindowTitle(QCoreApplication.translate("DispositivosDialog", u"Dispositivos", None))
        self.btnAgregar.setText(QCoreApplication.translate("DispositivosDialog", u"Agregar", None))
        ___qtablewidgetitem = self.tableDispositivos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DispositivosDialog", u"Cliente", None));
        ___qtablewidgetitem1 = self.tableDispositivos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DispositivosDialog", u"Marca", None));
        ___qtablewidgetitem2 = self.tableDispositivos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DispositivosDialog", u"Modelo", None));
        ___qtablewidgetitem3 = self.tableDispositivos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("DispositivosDialog", u"IMEI", None));
        ___qtablewidgetitem4 = self.tableDispositivos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("DispositivosDialog", u"N\u00ba Serie", None));
        ___qtablewidgetitem5 = self.tableDispositivos.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("DispositivosDialog", u"Color", None));
        ___qtablewidgetitem6 = self.tableDispositivos.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("DispositivosDialog", u"Accesorios", None));
        self.btnEliminar.setText(QCoreApplication.translate("DispositivosDialog", u"Eliminar", None))
        self.btnCerrar.setText(QCoreApplication.translate("DispositivosDialog", u"Cerrar", None))
    # retranslateUi

