
from PyQt5 import QtWidgets
from ui import Settings_design

from db import Setting


class DialogSettings(QtWidgets.QDialog):


    def __init__(self, parent=None):
        """
        Constructor.
        """
        super().__init__(parent=parent)

        self.ui = Settings_design.Ui_DialogSettings()
        self.ui.setupUi(self)

        self.SETTINGS = {
            'name': self.ui.tbName,
            'scholar': self.ui.tbScholar
        }

        self.load()


    def commit(self):
        """
        Commit the settings made.
        """
        for name, ctrl in self.SETTINGS.items():
            Setting.saveByName(name, ctrl.text())

        return True


    def load(self):
        """
        Load the user settings.
        """
        for name, ctrl in self.SETTINGS.items():
            s = Setting.get(name)
            if s:
                ctrl.setText(s.value)
            else:
                Setting.create(name, '')
            

    @staticmethod
    def set():
        """
        Set settings.
        """
        d = DialogSettings()

        if d.exec():
            return d.commit()
        else:
            return False


