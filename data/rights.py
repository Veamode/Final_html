import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data import db_session


class Rights(db_session.SqlAlchemyBase, SerializerMixin):
    print('rights')
    __tablename__ = 'rights'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


