
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui import Article_design
from datetime import date

from db import Article, Setting


class DialogArticle(QtWidgets.QDialog):
    

    def __init__(self, article=None, parent=None):
        """
        Constructor.
        """
        super().__init__(parent=parent)

        self.ui = Article_design.Ui_DialogArticle()
        self.ui.setupUi(self)

        self.ui.cbStatus.addItem('Published')
        self.ui.cbStatus.addItem('Accepted')
        self.ui.cbStatus.addItem('Submitted')
        self.ui.cbStatus.setCurrentIndex(0)

        if article is not None:
            self.load(article)
        else:
            self.article = None

        self.bindEvents()


    def bindEvents(self):
        """
        Bind control events.
        """
        self.ui.btnFromDOI.clicked.connect(self.fromDOI)
        self.ui.buttonBox.accepted.connect(self.validate)


    def commit(self, origarticle):
        """
        Commit the article to the database.
        """
        data = dict(
            doi=self.ui.tbDOI.text(),
            status=self.ui.cbStatus.currentIndex()+1,
            url=self.ui.tbURL.text(),
            pinboard=self.ui.tbPinboard.text(),
            title=self.ui.tbTitle.text(),
            authors=self.ui.tbAuthors.toPlainText(),
            journal=self.ui.tbJournal.text(),
            date=self.getDate(),
            volume=self.ui.tbVolume.text(),
            issue=self.ui.tbIssue.text(),
            pages=self.ui.tbPages.text(),
            keywords=self.ui.tbKeywords.text()
        )

        if origarticle:
            Article.save(id=origarticle.id, **data)
        else:
            Article.save(**d)

        return True


    def fromDOI(self):
        """
        Load an article from its DOI.
        """
        if self.ui.tbDOI.text():
            self.load(Article.fromDOI(self.ui.tbDOI.text()))


    def getDate(self):
        """
        Converts the specified date string to a Python datetime.date.
        """
        dstr = self.ui.tbDate.text()
        parts = dstr.split('-')
        while len(parts) < 3:
            parts.append('1')

        return date(year=int(parts[0]), month=int(parts[1]), day=int(parts[2]))


    def load(self, article):
        """
        Load an article from the database.
        """
        self.article = article

        self.ui.tbDOI.setText(article.doi)
        self.ui.tbURL.setText(article.url)
        self.ui.tbPinboard.setText(article.pinboard)
        self.ui.tbTitle.setText(article.title)
        self.ui.tbAuthors.setPlainText(article.authors)
        self.ui.tbJournal.setText(article.journal)
        if type(article.date) == date:
            self.ui.tbDate.setText(article.date.strftime('%Y-%m-%d'))
        else:
            self.ui.tbDate.setText(article.date)
        self.ui.tbVolume.setText(article.volume)
        self.ui.tbIssue.setText(article.issue)
        self.ui.tbPages.setText(article.pages)
        self.ui.tbKeywords.setText(article.keywords)


    def validate(self):
        """
        Validate the input.
        """
        try:
            self.getDate()
        except Exception as ex:
            QMessageBox.critical(self, 'Invalid date specified', f'Invalid format of article date:\n\n{ex}')
            return

        self.accept()


    @staticmethod
    def exe(article=None):
        """
        Execute this dialog.
        """
        d = DialogArticle(article=article)

        if d.exec():
            return d.commit(article)
        else:
            return False


