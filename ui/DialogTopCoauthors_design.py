# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/DialogTopCoauthors.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogTopCoauthors(object):
    def setupUi(self, DialogTopCoauthors):
        DialogTopCoauthors.setObjectName("DialogTopCoauthors")
        DialogTopCoauthors.resize(400, 518)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogTopCoauthors)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblDesc = QtWidgets.QLabel(DialogTopCoauthors)
        self.lblDesc.setMinimumSize(QtCore.QSize(0, 0))
        self.lblDesc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblDesc.setObjectName("lblDesc")
        self.verticalLayout.addWidget(self.lblDesc)
        self.tblAuthors = QtWidgets.QTableWidget(DialogTopCoauthors)
        self.tblAuthors.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblAuthors.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblAuthors.setColumnCount(2)
        self.tblAuthors.setObjectName("tblAuthors")
        self.tblAuthors.setRowCount(0)
        self.verticalLayout.addWidget(self.tblAuthors)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogTopCoauthors)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogTopCoauthors)
        self.buttonBox.rejected.connect(DialogTopCoauthors.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogTopCoauthors)

    def retranslateUi(self, DialogTopCoauthors):
        _translate = QtCore.QCoreApplication.translate
        DialogTopCoauthors.setWindowTitle(_translate("DialogTopCoauthors", "Dialog"))
        self.lblDesc.setText(_translate("DialogTopCoauthors", "Top co-authors:"))
