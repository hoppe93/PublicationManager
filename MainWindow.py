#!/usr/bin/env python3

import argparse
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ui import MainWindow_design
from pathlib import Path
import sys

from db import Article, config, Database, Setting

from DialogArticle import DialogArticle
from DialogSettings import DialogSettings
from DialogTopCoauthors import DialogTopCoauthors
from DialogExportText import DialogExportText


class MainWindow(QtWidgets.QMainWindow):
    

    def __init__(self):
        """
        Constructor.
        """
        QtWidgets.QMainWindow.__init__(self)
        self.ui = MainWindow_design.Ui_MainWindow()
        self.ui.setupUi(self)

        root = Path(__file__).parent.absolute()

        self.ui.btnAddArticle.setIcon(QtGui.QIcon(f'{root}/icons/add.png'))
        self.ui.btnExport.setIcon(QtGui.QIcon(f'{root}/icons/Printer.png'))
        self.ui.exportMenu = QtWidgets.QMenu()
        self.ui.actionExportText = self.ui.exportMenu.addAction('to text')
        self.ui.actionExportText.setIcon(QtGui.QIcon(f'{root}/icons/document-text.png'))
        self.ui.actionExportBibtex = self.ui.exportMenu.addAction('to BibTeX')
        self.ui.actionExportBibtex.setIcon(QtGui.QIcon(f'{root}/icons/disconnect.png'))
        self.ui.btnExport.setMenu(self.ui.exportMenu)

        self.treeViewModel = QtGui.QStandardItemModel()
        self.ui.tvPublications.setModel(self.treeViewModel)

        # Open/create database
        args = self.parseArgs()
        if args.new:
            fname = self.newDatabase()
            if fname is None:
                raise Exception('No publications database specified. Exiting.')
        elif args.publications is not None:
            self.loadPublications(args.publications)
        else:
            filename, _ = QFileDialog.getOpenFileName(
                parent=self, caption="Open publications database",
                filter="SQLite database (*.db);;All files (*.*)"
            )

            if not filename:
                raise Exception('No publications database specified. Exiting.')
            else:
                self.loadPublications(filename)

        self.bindEvents()


    def bindEvents(self):
        """
        Bind control events.
        """
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionSettings.triggered.connect(DialogSettings.set)
        self.ui.actionExportText.triggered.connect(DialogExportText.export)
        self.ui.actionTopCoauthors.triggered.connect(DialogTopCoauthors.exe)

        self.ui.btnAddArticle.clicked.connect(self.addEditArticle)
        self.ui.tvPublications.doubleClicked.connect(self.articleDoubleClicked)


    def parseArgs(self):
        parser = argparse.ArgumentParser('Publication manager')

        parser.add_argument('publications', help="File containing publication database.", nargs='?', default=None)
        parser.add_argument('-n', '--new', help="Create a new publication database.", action='store_true')

        return parser.parse_args()


    def closeEvent(self, event):
        self.exit()


    def exit(self):
        self.close()


    def loadPublications(self, filename):
        """
        Load the publications database.
        """
        self.filename = filename
        self.db = Database(filename)
        config.init(self.db)
        
        self.reloadPublications()


    def reloadPublications(self):
        """
        Reload the publications view.
        """
        stats = Article.loadPublicationsToTreeview(self.treeViewModel)
        self.ui.lblTotalPublications.setText(f"{stats['published']+stats['npublished']}")
        self.ui.lblFirstAuthor.setText(f"{stats['nfirst']}")
        self.ui.lblNRTotalPublications.setText(f"{stats['npeerreviewed']}")
        self.ui.lblNRFirstAuthor.setText(f"{stats['nfirst_nr']}")
        self.ui.lblInProgress.setText(f"{stats['npublished']}")


    def newDatabase(self):
        """
        Create a new publications database.
        """
        filename, _ = QFileDialog.getSaveFileName(
            parent=self, caption="Create a new publications database",
            filter="SQLite database (*.db);;All files (*.*)"
        )

        if not filename:
            return None

        self.loadPublications(filename)

        # Get user settings
        DialogSettings.set()

        return filename


    def addEditArticle(self, id=None):
        """
        Add/edit an article.
        """
        article = None
        if id is not None:
            article = Article.get(id=id)

        if DialogArticle.exe(article):
            self.reloadPublications()


    def articleDoubleClicked(self, modelIndex):
        """
        Signal triggered when an item in the tree view is double clicked.
        """
        item = self.treeViewModel.itemFromIndex(modelIndex)

        if item.data() is not None:
            self.addEditArticle(item.data())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


