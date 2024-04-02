
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui import EditReferenceFormat_design

from db import ReferenceFormat


class DialogEditReferenceFormat(QtWidgets.QDialog):
    

    def __init__(self, name, parent=None):
        """
        Constructor.
        """
        super().__init__(parent=parent)

        self.ui = EditReferenceFormat_design.Ui_EditReferenceFormat()
        self.ui.setupUi(self)

        if name != 'New':
            self.referenceFormat = ReferenceFormat.get(name=name)
            self.ui.tbName.setText(name)
            self.ui.tbCode.setPlainText(self.referenceFormat.code)
        else:
            self.referenceFormat = None
            self.ui.tbCode.setPlainText(ReferenceFormat.DEFAULT)

        self.bindEvents()


    def bindEvents(self):
        """
        Bind controls to events.
        """
        self.ui.buttonBox.accepted.connect(self.validateAndAccept)


    def commit(self):
        """
        Commit the modifications to the database.
        """
        vals = {
            'name': self.ui.tbName.text(),
            'code': self.ui.tbCode.toPlainText()
        }

        if self.referenceFormat is not None:
            vals['id'] = self.referenceFormat.id

        ReferenceFormat.save(**vals)

        return vals['name']


    def validateAndAccept(self):
        """
        Validate input and accept if correct.
        """
        if self.ui.tbName.text().strip() not in ['', 'New']:
            self.accept()
        else:
            QMessageBox.critical(self, 'Invalid name', 'The specified name is not allowed.')


    @staticmethod
    def edit(name, parent=None):
        """
        Edit the reference format of the specified name. 'New' is a
        special name.
        """
        d = DialogEditReferenceFormat(name, parent=parent)

        if d.exec():
            return d.commit()
        else:
            return False


