
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from ui import DialogTopCoauthors_design

from db import Article, Setting
from DialogPapers import DialogPapers


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
        self.bindEvents()


    def bindEvents(self):
        """
        Bind events.
        """
        self.ui.tbFilter.textChanged.connect(self.filterAuthors)
        self.ui.tblAuthors.cellDoubleClicked.connect(self.showPapers)


    def filterAuthors(self, text):
        """
        Filter authors based on search.
        """
        txtl = text.lower()
        for i in range(self.ui.tblAuthors.rowCount()):
            hide = True
            q = self.ui.tblAuthors.item(i, 0)
            if txtl in q.text().lower():
                hide = False

            self.ui.tblAuthors.setRowHidden(i, hide)


    def showPapers(self, row, col):
        """
        Show the papers for the selected author.
        """
        name = self.ui.tblAuthors.item(row, 0).text()
        papers = self.ui.tblAuthors.item(row, 1).data(QtCore.Qt.UserRole)
        DialogPapers.exe(f'Joint papers with {name}', papers, self)


    def processAuthors(self):
        """
        Process authors and produce statistics.
        """
        articles = Article.getall()
        authors = []
        authorp = []
        authora = {}
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
                    authora[s] = [article]
                else:
                    authorp[authors.index(s)] += 1
                    authora[s].append(article)

        authorp, authors = zip(*sorted(zip(authorp, authors)))

        self.ui.tblAuthors.setRowCount(len(authors))
        for i in range(len(authors)):
            papers = QTableWidgetItem(f'{authorp[-1-i]}')
            papers.setData(QtCore.Qt.UserRole, authora[authors[-1-i]])

            self.ui.tblAuthors.setItem(i, 0, QTableWidgetItem(f'{authors[-1-i]}'))
            self.ui.tblAuthors.setItem(i, 1, papers)


    @staticmethod
    def exe():
        """
        Execute this dialog.
        """
        return DialogTopCoauthors().exec()


