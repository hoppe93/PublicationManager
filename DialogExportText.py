
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from ui import DialogExportText_design

from db import Article, ReferenceFormat

from DialogEditReferenceFormat import DialogEditReferenceFormat
import ReferenceFormatter


class DialogExportText(QtWidgets.QDialog):
    

    def __init__(self, parent=None):
        """
        Constructor.
        """
        super().__init__(parent=parent)

        self.ui = DialogExportText_design.Ui_DialogExportText()
        self.ui.setupUi(self)

        self.treeViewModel = QtGui.QStandardItemModel()
        self.ui.tvPublications.setModel(self.treeViewModel)

        self.reloadReferenceFormats()

        self.loadPublications()

        self.bindEvents()


    def bindEvents(self):
        """
        Bind controls to events.
        """
        self.ui.tvPublications.clicked.connect(self.treeViewItemClicked)
        self.ui.btnEdit.clicked.connect(self.editReferenceFormat)
        self.ui.sbMaxAuthors.valueChanged.connect(self.formatReferences)
        self.ui.cbAbbrJournal.stateChanged.connect(self.formatReferences)
        self.ui.cbPeriodInAuthors.stateChanged.connect(self.formatReferences)
        self.ui.cbReferenceFormat.currentTextChanged.connect(self.formatReferences)


    def editReferenceFormat(self):
        """
        Edit the selected reference format.
        """
        name = self.ui.cbReferenceFormat.currentText()
        newname = DialogEditReferenceFormat.edit(name, self)

        if newname:
            self.reloadReferenceFormats()
            self.ui.cbReferenceFormat.setCurrentText(newname)
            #self.ui


    def formatReferences(self):
        """
        Format the selected references.
        """
        rf = ReferenceFormat.get(name=self.ui.cbReferenceFormat.currentText())
        articles = self.getSelectedArticles()

        code = ReferenceFormat.DEFAULT
        if rf is not None:
            code = rf.code

        fmt = ''
        try:
            for article in articles:
                if fmt: fmt += '\n'
                fmt += ReferenceFormatter.format(
                    code, article,
                    maxauthors=self.ui.sbMaxAuthors.value(),
                    abbrjournal=self.ui.cbAbbrJournal.isChecked(),
                    includeperiods=self.ui.cbPeriodInAuthors.isChecked()
                )
        except Exception as ex:
            msg = f'Exception occurred while formatting references.\n\n{ex}'
            QMessageBox.critical(self, 'Formatting error', msg)
            fmt = msg

        self.ui.tbReferences.setPlainText(fmt)


    def getSelectedArticles(self):
        """
        Get all selected articles.
        """
        artid = []
        def recurse(parent):
            for i in range(parent.rowCount()):
                child = parent.child(i)
                gchildren = child.rowCount()
                if gchildren > 0:
                    recurse(child)
                elif child.checkState() == Qt.Checked:
                    artid.append(child.data())

        recurse(self.treeViewModel.invisibleRootItem())
        return [Article.get(id=i) for i in artid]


    def loadPublications(self):
        """
        Load the publications view.
        """
        Article.loadPublicationsToTreeview(self.treeViewModel, checkable=True)


    def treeViewItemClicked(self, modelIndex):
        """
        An item is clicked in the treeview.
        """
        self.itemChecked(modelIndex)
        self.formatReferences()


    def itemChecked(self, modelIndex):
        """
        An item is checked.
        """
        item = self.treeViewModel.itemFromIndex(modelIndex)

        if item.rowCount() == 0:
            return

        for i in range(item.rowCount()):
            child = item.child(i)
            child.setCheckState(item.checkState())
            self.itemChecked(child.index())


    def reloadReferenceFormats(self):
        self.ui.cbReferenceFormat.clear()
        rfs = ReferenceFormat.getAll()
        for rf in rfs:
            self.ui.cbReferenceFormat.addItem(rf.name, rf.id)

        self.ui.cbReferenceFormat.addItem('New', -1)
        self.ui.cbReferenceFormat.setCurrentIndex(0)


    @staticmethod
    def export():
        """
        Export the article list.
        """
        d = DialogExportText()
        return d.exec()


