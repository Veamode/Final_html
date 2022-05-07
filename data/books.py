import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data import db_session


class Book(db_session.SqlAlchemyBase, SerializerMixin):
    print('photos')
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)