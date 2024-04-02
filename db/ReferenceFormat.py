
from sqlalchemy import Column, Integer, String
from . base import Base

from sqlalchemy.sql.expression import insert, select, update
from . import config


class ReferenceFormat(Base):
    

    __tablename__ = 'referenceformats'


    DEFAULT = "return f'{authors}, {journal} {volume} ({year})'"


    # Reference format ID
    id = Column(Integer, primary_key=True)
    # Reference format name
    name = Column(String)
    # Reference format code
    code = Column(String)


    @staticmethod
    def get(id=None, name=None):
        """
        Returns the reference format with the given name.
        """
        db = config.database()
        if name is not None:
            return db.exe(select(ReferenceFormat).where(ReferenceFormat.name==name)).scalars().one_or_none()
        elif id is not None:
            return db.exe(select(ReferenceFormat).where(ReferenceFormat.id==id)).scalars().one_or_none()
        else:
            raise Exception(f"Neither an ID nor a name was specified when trying to get a 'ReferenceFormat'.")


    @staticmethod
    def getAll():
        """
        Returns all reference formats from the database.
        """
        db = config.database()
        return db.exe(select(ReferenceFormat).order_by(ReferenceFormat.name.asc())).scalars().all()


    @staticmethod
    def getFormat(name):
        """
        Return the code corresponding to the named ReferenceFormat.
        """
        if name == 'New':
            return ReferenceFormat.DEFAULT
        else:
            return ReferenceFormat.get(name=name).code


    @staticmethod
    def save(id=None, **kwargs):
        """
        Save the given reference format to the database. If an ID is given,
        the reference format is updated rather than inserted.
        """
        db = config.database()

        if id is not None:
            stmt = update(ReferenceFormat).where(ReferenceFormat.id==id)
        else:
            stmt = insert(ReferenceFormat)

        stmt = stmt.values(**kwargs)
        return db.exe(stmt, commit=True)


    @staticmethod
    def saveByName(name, code):
        """
        Save the given reference format to the database.
        """
        db = config.database()

        stmt = update(ReferenceFormat).where(ReferenceFormat.name==name).values(code=code)
        return db.exe(stmt, commit=True)


