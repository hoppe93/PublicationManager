
from datetime import datetime
from sqlalchemy import Column, Date, Integer, String, or_
from . base import Base
from . Setting import Setting

from PyQt5 import QtGui
from pathlib import Path

from sqlalchemy.sql.expression import insert, select, update
from . import config

from . import refhelp


class Presentation(Base):
    

    __tablename__ = 'presentations'


    TYPE_ORAL = 1
    TYPE_POSTER = 2
    TYPE_INVITED = 3


    # Presentation ID
    id = Column(Integer, primary_key=True)
    # Status
    type = Column(Integer)
    # DOI
    doi = Column(String)
    # URL to poster/presentation
    url = Column(String)
    # EUROfusion pinboard ID
    pinboard = Column(String)
    # Title
    title = Column(String)
    # Authors
    authors = Column(String)
    # Venue
    venue = Column(String)
    # Presentation ID
    presentationid = Column(String)
    # Date
    date = Column(Date)
    # Keywords
    keywords = Column(String)


    def getFirstAuthor(self, asarray=False):
        """
        Returns the name of the first author of this presentation.
        """
        authors = self.authors.split(', ')
        if not asarray:
            return authors[0]

        return authors[0].split(' ')


    def getName(self):
        """
        Return a representative name for this presentation.
        """
        a = self.getFirstAuthor(True)[-1]

        return f'{a} ({self.date.year}): {self.title}'


    @staticmethod
    def exists(doi):
        """
        Check if the presentation with the given DOI exists.
        """
        p = Presentation.getByDOI(doi)
        return (p is not None)


    @staticmethod
    def get(id):
        """
        Returns the presentation with the given ID.
        """
        db = config.database()
        return db.exe(select(Presentation).where(Presentation.id == id)).scalars().one_or_none()


    @staticmethod
    def getOral():
        """
        Returns all oral presentations.
        """
        db = config.database()
        return db.exe(select(Presentation).where(Presentation.type == Presentation.TYPE_ORAL).order_by(Presentation.date.desc())).scalars().all()


    @staticmethod
    def getPoster():
        """
        Returns all poster presentations.
        """
        db = config.database()
        return db.exe(select(Presentation).where(Presentation.type == Presentation.TYPE_POSTER).order_by(Presentation.date.desc())).scalars().all()


    @staticmethod
    def getInvited():
        """
        Returns all invited presentations.
        """
        db = config.database()
        return db.exe(select(Presentation).where(Presentation.type == Presentation.TYPE_INVITED).order_by(Presentation.date.desc())).scalars().all()


    @staticmethod
    def getByDOI(doi):
        """
        Returns the presentation with the given DOI.
        """
        db = config.database()
        return db.exe(select(Presentation).where(Presentation.doi == doi)).scalars().one_or_none()


    @staticmethod
    def getall():
        """
        Returns all presentations.
        """
        db = config.database()
        return db.exe(select(Presentation).order_by(Presentation.date.desc())).scalars().all()


    @staticmethod
    def save(id=None, **kwargs):
        """
        Save the given presentation to the database. If an ID is given,
        the presentation is updated rather than inserted.
        """
        db = config.database()

        if id is not None:
            stmt = update(Presentation).where(Presentation.id==id)
        else:
            stmt = insert(Presentation)

        stmt = stmt.values(**kwargs)
        result = db.exe(stmt, commit=True)

        return result


    @staticmethod
    def fromDOI(doi):
        """
        Fetch presentation details from its DOI number (or URL).
        """
        js = refhelp.fromDOI(doi)

        def ret(key, d=''):
            value = js.get(key, d)
            if isinstance(value, list):
                if len(value) == 1:
                    return value[0]
                return ', '.join(value)
            return value

        p = Presentation()

        p.doi = ret('DOI')
        p.title = ret('title')
        p.url = f'https://doi.org/{p.doi}' if p.doi else ''
        authors = []
        for author in js.get('author', []):
            if 'given' in author and 'family' in author:
                authors.append(author['given'] + ' ' + author['family'])
            elif 'name' in author:
                authors.append(author['name'])
        p.authors = ', '.join(authors)
        p.venue = ret('event-title') or ret('group-title') or ret('container-title')

        if 'issued' in js:
            dt = js['issued']['date-parts'][0]
        elif 'created' in js:
            dt = js['created']['date-parts'][0]
        else:
            dt = None

        if dt:
            dt = [f'{x:02d}' for x in dt]
            ds = '-'.join(dt)
            if ds.count('-') == 2:
                p.date = datetime.fromisoformat(ds)
            elif ds.count('-') == 1:
                p.date = datetime.fromisoformat(ds + '-01')
            elif ds.count('-') == 0:
                p.date = datetime(int(ds), 1, 1)
            else:
                raise Exception(f"Unrecognized date format: '{ds}'.")
        else:
            p.date = datetime.now()

        return p


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
    def loadPresentationsToTreeview(treeViewModel, checkable=False):
        """
        Load all presentations from the database into a treeview.
        """
        ICONS = Presentation.getIcons()

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


        def addPresentations(parent, presentations, icon):
            years = []
            yr = None
            npres = 0

            for presentation in presentations:
                if presentation.date.year not in years:
                    if yr is not None:
                        yr.setText(yr.text() + f' ({npres})')
                        npres = 0

                    yr = addItem(parent, f'{presentation.date.year}', 'year')
                    years.append(presentation.date.year)

                addItem(yr, presentation.getName(), icon, presentation.id)
                npres += 1

            if yr is not None:
                yr.setText(yr.text() + f' ({npres})')


        oral = Presentation.getOral()
        poster = Presentation.getPoster()
        invited = Presentation.getInvited()

        root = treeViewModel.invisibleRootItem()

        ora = addItem(root, f'Oral presentations ({len(oral)})', 'category')
        pos = addItem(root, f'Poster presentations ({len(poster)})', 'category')
        inv = addItem(root, f'Invited presentations ({len(invited)})', 'category')

        addPresentations(ora, oral, 'article-blue')
        addPresentations(pos, poster, 'article-green')
        addPresentations(inv, invited, 'article-red')

        return {
            'oral': len(oral),
            'poster': len(poster),
            'invited': len(invited)
        }
