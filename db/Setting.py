
from sqlalchemy import Column, Integer, String
from . base import Base

from sqlalchemy.sql.expression import insert, select, update
from . import config


class Setting(Base):
    

    __tablename__ = 'settings'


    # Setting ID
    id = Column(Integer, primary_key=True)
    # Setting name
    name = Column(String)
    # Setting value
    value = Column(String)


    @staticmethod
    def create(name, value):
        """
        Create a new setting with the given name.
        """
        db = config.database()

        s = Setting.get(name)
        if s != None:
            return False

        return db.exe(insert(Setting).values(name=name, value=value))


    @staticmethod
    def get(name):
        """
        Returns the setting with the given name.
        """
        db = config.database()
        return db.exe(select(Setting).where(Setting.name==name)).scalars().one_or_none()


    @staticmethod
    def save(id=None, **kwargs):
        """
        Save the given setting to the database. If an ID is given,
        the setting is updated rather than inserted.
        """
        db = config.database()

        if id is not None:
            stmt = update(Setting).where(Setting.id==id)
        else:
            stmt = insert(Setting)

        stmt = stmt.values(**kwargs)
        return db.exe(stmt, commit=True)


    @staticmethod
    def saveByName(name, value):
        """
        Save the given setting to the database.
        """
        db = config.database()

        stmt = update(Setting).where(Setting.name==name).values(value=value)
        return db.exe(stmt, commit=True)


