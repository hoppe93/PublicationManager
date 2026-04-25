from datetime import date, datetime
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from db import Presentation
from ui import Presentation_design


class DialogPresentation(QtWidgets.QDialog):


    def __init__(self, presentation=None, parent=None):
        """
        Constructor.
        """
        super().__init__(parent=parent)

        self.ui = Presentation_design.Ui_DialogPresentation()
        self.ui.setupUi(self)

        self.ui.cbType.addItem('Oral')
        self.ui.cbType.addItem('Poster')
        self.ui.cbType.addItem('Invited')
        self.ui.cbType.setCurrentIndex(0)

        if presentation is not None:
            self.load(presentation)
        else:
            self.presentation = None

        self.bindEvents()


    def bindEvents(self):
        """
        Bind control events.
        """
        self.ui.pushButton.clicked.connect(self.fromDOI)
        self.ui.buttonBox.accepted.connect(self.validate)


    def commit(self, origpresentation):
        """
        Commit the presentation to the database.
        """
        data = dict(
            doi=self.ui.tbDOI.text(),
            type=self.ui.cbType.currentIndex()+1,
            url=self.ui.tbURL.text(),
            pinboard=self.ui.tbPinboard.text(),
            title=self.ui.tbTitle.text(),
            authors=self.ui.tbAuthors.toPlainText(),
            venue=self.ui.tbVenue.text(),
            presentationid=self.ui.tbPresentationID.text(),
            date=self.getDate(),
            keywords=self.ui.tbKeywords.text()
        )

        if origpresentation:
            Presentation.save(id=origpresentation.id, **data)
        else:
            Presentation.save(**data)

        return True


    def fromDOI(self):
        """
        Load a presentation from its DOI.
        """
        if self.ui.tbDOI.text():
            try:
                presentation = Presentation.fromDOI(self.ui.tbDOI.text())
            except Exception as ex:
                QMessageBox.critical(self, 'Error importing presentation', f'{ex}\n\n{"".join(traceback.format_exception(ex))}')
                return

            self.load(presentation)

            # Check if this presentation already exists in the database
            if presentation.doi and Presentation.exists(doi=presentation.doi):
                QMessageBox.warning(self, 'Duplicate presentation', 'This presentation already exists in the database.')


    def getDate(self):
        """
        Converts the specified date string to a Python datetime.date.
        """
        dstr = self.ui.tbDate.text()
        parts = dstr.split('-')
        while len(parts) < 3:
            parts.append('1')

        return date(year=int(parts[0]), month=int(parts[1]), day=int(parts[2]))


    def load(self, presentation):
        """
        Load a presentation from the database.
        """
        self.presentation = presentation

        self.ui.tbDOI.setText(presentation.doi or '')
        self.ui.tbURL.setText(presentation.url or '')
        self.ui.tbPinboard.setText(presentation.pinboard or '')
        self.ui.tbTitle.setText(presentation.title or '')
        self.ui.tbAuthors.setPlainText(presentation.authors or '')
        self.ui.tbVenue.setText(presentation.venue or '')
        self.ui.tbPresentationID.setText(presentation.presentationid or '')
        if type(presentation.date) == date or type(presentation.date) == datetime:
            self.ui.tbDate.setText(presentation.date.strftime('%Y-%m-%d'))
        elif presentation.date:
            self.ui.tbDate.setText(presentation.date)
        else:
            self.ui.tbDate.setText('')
        self.ui.tbKeywords.setText(presentation.keywords or '')
        self.ui.cbType.setCurrentIndex(presentation.type-1 if presentation.type else 0)


    def validate(self):
        """
        Validate the input.
        """
        try:
            self.getDate()
        except Exception as ex:
            QMessageBox.critical(self, 'Invalid date specified', f'Invalid format of presentation date:\n\n{ex}')
            return

        self.accept()


    @staticmethod
    def exe(presentation=None):
        """
        Execute this dialog.
        """
        d = DialogPresentation(presentation=presentation)

        if d.exec():
            return d.commit(presentation)
        else:
            return False
