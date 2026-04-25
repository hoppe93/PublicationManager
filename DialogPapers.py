
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from ui import DialogPapers_design

from db import Article
from DialogArticle import DialogArticle


class DialogPapers(QtWidgets.QDialog):
    

    def __init__(self, title, papers, parent=None):
        """
        Constructor.
        """
        super().__init__(parent=parent)

        self.ui = DialogPapers_design.Ui_DialogPapers()
        self.ui.setupUi(self)
        self.setWindowTitle(title)

        cols = ['Year', 'Title', 'No. of authors']

        self.ui.tblPapers.setColumnCount(len(cols))
        self.ui.tblPapers.setHorizontalHeaderLabels(cols)
        header = self.ui.tblPapers.horizontalHeader()
        header.resizeSection(0, 80)
        header.resizeSection(2, 120)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.addPapers(papers)
        self.bindEvents()


    def bindEvents(self):
        """
        Bind events.
        """
        self.ui.tblPapers.cellDoubleClicked.connect(self.showPaper)


    def addPapers(self, papers):
        """
        Add the list of papers to the table.
        """
        pprs = sorted(papers, key=lambda p : p.date, reverse=True)
        self.ui.tblPapers.setRowCount(len(pprs))
        for i in range(len(pprs)):
            p = pprs[i]
            
            nauthors = len(p.authors.split(','))

            year = QTableWidgetItem(f'{p.date.year:d}')
            year.setData(QtCore.Qt.UserRole, p)
            self.ui.tblPapers.setItem(i, 0, year)
            self.ui.tblPapers.setItem(i, 1, QTableWidgetItem(f'{p.title}'))
            self.ui.tblPapers.setItem(i, 2, QTableWidgetItem(f'{nauthors}'))


    def showPaper(self, row, col):
        """
        Show details about the selected paper.
        """
        paper = self.ui.tblPapers.item(row, 0).data(QtCore.Qt.UserRole)
        DialogArticle.exe(paper)


    @staticmethod
    def exe(title, papers, parent=None):
        """
        Execute this dialog.
        """
        return DialogPapers(title, papers, parent).exec()


