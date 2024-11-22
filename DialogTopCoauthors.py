
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from ui import DialogTopCoauthors_design

from db import Article, Setting


class DialogTopCoauthors(QtWidgets.QDialog):
    

    def __init__(self, parent=None):
        """
        Constructor.
        """
        super().__init__(parent=parent)

        self.ui = DialogTopCoauthors_design.Ui_DialogTopCoauthors()
        self.ui.setupUi(self)

        self.ui.tblAuthors.setHorizontalHeaderLabels(['Name', 'Publications'])
        header = self.ui.tblAuthors.horizontalHeader()
        header.resizeSection(1, 100)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.processAuthors()


    def processAuthors(self):
        """
        Process authors and produce statistics.
        """
        articles = Article.getall()
        authors = []
        authorp = []
        name = Setting.get('name').value

        for article in articles:
            auths = article.authors.split(',')

            for a in auths:
                s = a.strip()
                if s == name:
                    # Skip self
                    continue
                elif s not in authors:
                    authors.append(s)
                    authorp.append(1)
                else:
                    authorp[authors.index(s)] += 1

        authorp, authors = zip(*sorted(zip(authorp, authors)))

        self.ui.tblAuthors.setRowCount(len(authors))
        for i in range(len(authors)):
            self.ui.tblAuthors.setItem(i, 0, QTableWidgetItem(f'{authors[-1-i]}'))
            self.ui.tblAuthors.setItem(i, 1, QTableWidgetItem(f'{authorp[-1-i]}'))


    @staticmethod
    def exe():
        """
        Execute this dialog.
        """
        return DialogTopCoauthors().exec()


