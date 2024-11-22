
import requests

from datetime import date
from sqlalchemy import Column, Date, Integer, String, or_
from . base import Base
from . Setting import Setting

from PyQt5 import QtGui
from pathlib import Path

from sqlalchemy.sql.expression import insert, select, update
from . import config

from . import refhelp


class Article(Base):
    

    __tablename__ = 'articles'


    STATUS_PUBLISHED = 1
    STATUS_ACCEPTED = 2
    STATUS_SUBMITTED = 3
    STATUS_NON_REVIEWED = 4


    # Article ID
    id = Column(Integer, primary_key=True)
    # Status
    status = Column(Integer)
    # DOI
    doi = Column(String)
    # URL to article
    url = Column(String)
    # EUROfusion pinboard ID
    pinboard = Column(String)
    # Title
    title = Column(String)
    # Authors
    authors = Column(String)
    # Journal
    journal = Column(String)
    # Volume
    volume = Column(String)
    # Issue
    issue = Column(String)
    # Pages
    pages = Column(String)
    # Date of publication
    date = Column(Date)
    # Keywords
    keywords = Column(String)


    def isFirstAuthor(self, authorname):
        """
        Returns true if the user is first author of this article.
        """
        authors = self.authors.split(', ')
        a = authors[0].split(' ')

        for w in a:
            if w.strip().strip('.') not in authorname:
                return False

        return True


    def getFirstAuthor(self, asarray=False):
        """
        Returns the name of the first author of this article.
        """
        authors = self.authors.split(', ')
        if not asarray:
            return authors[0]

        return authors[0].split(' ')

            
    def getName(self):
        """
        Return a representative name for this article.
        """
        a = self.getFirstAuthor(True)[-1]

        return f'{a} ({self.date.year}): {self.title}'


    @staticmethod
    def get(id):
        """
        Returns the article with the given ID.
        """
        db = config.database()
        return db.exe(select(Article).where(Article.id==id).order_by(Article.date.desc())).scalars().one_or_none()


    @staticmethod
    def getPublished():
        """
        Get all articles with status 'Published'.
        """
        db = config.database()
        return db.exe(select(Article).where(Article.status==Article.STATUS_PUBLISHED).order_by(Article.date.desc())).scalars().all()


    @staticmethod
    def getAccepted():
        """
        Get all articles with status 'Accepted'.
        """
        db = config.database()
        return db.exe(select(Article).where(Article.status==Article.STATUS_ACCEPTED).order_by(Article.date.desc())).scalars().all()


    @staticmethod
    def getSubmitted():
        """
        Get all articles with status 'Submitted'.
        """
        db = config.database()
        return db.exe(select(Article).where(Article.status==Article.STATUS_SUBMITTED)).scalars().all()


    @staticmethod
    def getNotPublished():
        """
        Get all articles with status which is not 'Published'.
        """
        db = config.database()
        return db.exe(select(Article).where(or_(Article.status==Article.STATUS_SUBMITTED, Article.status==Article.STATUS_ACCEPTED)).order_by(Article.date.desc())).scalars().all()


    @staticmethod
    def getNonPeerReviewed():
        """
        Get all non-peer reviewed articles.
        """
        db = config.database()
        return db.exe(select(Article).where(Article.status==Article.STATUS_NON_REVIEWED).order_by(Article.date.desc())).scalars().all()


    @staticmethod
    def getall():
        """
        Returns a list of all publications.
        """
        db = config.database()
        return db.exe(select(Article)).scalars().all()


    @staticmethod
    def save(id=None, **kwargs):
        """
        Save the given article to the database. If an ID is given,
        the article is updated rather than inserted.
        """
        db = config.database()
        
        if id is not None:
            stmt = update(Article).where(Article.id==id)
        else:
            stmt = insert(Article)

        stmt = stmt.values(**kwargs)
        result = db.exe(stmt, commit=True)

        return result


    @staticmethod
    def fromDOI(doi):
        """
        Fetch article details from its DOI number (or URL).
        """
        js = refhelp.fromDOI(doi)

        def ret(key, d=''):
            if key in js:
                return js[key]
            else:
                return d

        a = Article()

        a.doi = ret('DOI')
        a.title = ret('title')
        a.url = f'https://doi.org/{a.doi}'
        a.journal = ret('container-title')
        a.issue = ret('issue')
        a.volume = ret('volume')
        if 'page' in js:
            a.pages = ret('page')
        elif 'article-number' in js:
            a.pages = ret('article-number')

        if 'published-print' in js:
            dt = js['published-print']['date-parts'][0]
        elif 'published-online' in js:
            dt = js['published-online']['date-parts'][0]
        elif 'created' in js:
            dt = js['created']['date-parts'][0]

        dt = [f'{x:02d}' for x in dt]
        a.date = '-'.join(dt)

        if 'published-print' in js:
            a.status = Article.STATUS_PUBLISHED
        else:
            a.status = Article.STATUS_ACCEPTED

        authors = []
        aut = ret('author')
        for author in aut:
            if 'given' in author:
                given = author['given'].split(' ')
                gvn = ''
                for g in given:
                    gvn += g[0] + '. '
                gvn = gvn.strip()

                authors.append(gvn + ' ' + author['family'])
            # "Teams" do not have given names
            elif 'name' in author:
                authors.append(author['name'])
            else:
                # Sometimes ORCIDs are given as separate authors
                pass

        a.authors = ', '.join(authors)

        return a


    @staticmethod
    def getIcons():
        root = Path(__file__).parent.parent.absolute()
        return {
            'year': QtGui.QIcon(f'{root}/icons/year.png'),
            'category': QtGui.QIcon(f'{root}/icons/category.png'),
            'article-blue': QtGui.QIcon(f'{root}/icons/article-blue.png'),
            'article-green': QtGui.QIcon(f'{root}/icons/article-green.png'),
            'article-red': QtGui.QIcon(f'{root}/icons/article-red.png')
        }


    @staticmethod
    def loadPublicationsToTreeview(treeViewModel, checkable=False):
        """
        Load all articles from the database into a treeview.
        """
        ICONS = Article.getIcons()
        def addItem(parent, name, icon, data=None):
            """
            Add an item to the tree view.
            """
            itm = QtGui.QStandardItem(name)
            itm.setIcon(ICONS[icon])

            if checkable:
                itm.setCheckable(checkable)

            if data:
                itm.setData(data)

            parent.appendRow(itm)

            return itm


        treeViewModel.clear()

        published = Article.getPublished()
        npublishd = Article.getNotPublished()
        npeerrvwd = Article.getNonPeerReviewed()

        root = treeViewModel.invisibleRootItem()

        npb = addItem(root, f'In preparation ({len(npublishd)})', 'category')
        pub = addItem(root, f'Published ({len(published)})', 'category')
        npr = addItem(root, f'Non-peer reviewed ({len(npeerrvwd)})', 'category')

        authorname = Setting.get('name').value

        years = []
        yr = None
        nfirst = 0
        nart = 0
        for p in npublishd:
            if p.date.year not in years:
                if yr is not None:
                    yr.setText(yr.text() + f' ({nart})')
                    nart = 0
                yr = addItem(npb, f'{p.date.year}', 'year')
                years.append(p.date.year)

            if p.isFirstAuthor(authorname):
                nfirst += 1

            addItem(yr, p.getName(), 'article-red', p.id)
            nart += 1

        if yr is not None:
            yr.setText(yr.text() + f' ({nart})')

        years = []
        nart = 0
        for p in published:
            if p.date.year not in years:
                if yr is not None:
                    yr.setText(yr.text() + f' ({nart})')
                    nart = 0
                yr = addItem(pub, f'{p.date.year}', 'year')
                years.append(p.date.year)

            if p.isFirstAuthor(authorname):
                nfirst += 1

            addItem(yr, p.getName(), 'article-green', p.id)
            nart += 1

        if yr is not None:
            yr.setText(yr.text() + f' ({nart})')

        years = []
        nart = 0
        nfirst_npr = 0
        for p in npeerrvwd:
            if p.date.year not in years:
                if yr is not None:
                    yr.setText(yr.text() + f' ({nart})')
                    nart = 0

                yr = addItem(npr, f'{p.date.year}', 'year')
                years.append(p.date.year)

            if p.isFirstAuthor(authorname):
                nfirst_npr += 1

            addItem(yr, p.getName(), 'article-green', p.id)
            nart += 1

        if yr is not None:
            yr.setText(yr.text() + f' ({nart})')

        return {
            'published': len(published),
            'npublished': len(npublishd),
            'npeerreviewed': len(npeerrvwd),
            'nfirst': nfirst,
            'nfirst_nr': nfirst_npr
        }


