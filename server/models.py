# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Use db.DateTime and default to datetime.utcnow
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    def __repr__(self):
        return f'<Message {self.id}>'
