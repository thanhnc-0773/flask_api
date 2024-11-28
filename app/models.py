from app import db
from sqlalchemy import asc, desc
from contextlib import contextmanager
from datetime import datetime
from app.utils.s3_utils import get_presign_url_from_s3

class ModelBase(db.Model):
    __abstract__ = True

    @classmethod
    def get(cls, record_id):
        return cls.query.get(record_id)

    @classmethod
    def list(cls, filters=None, order_by=None):
        query = cls.query
        if filters:
            for attr, condition in filters.items():
                if isinstance(condition, dict):
                    for op, value in condition.items():
                        if op == '==':
                            query = query.filter(getattr(cls, attr) == value)
                        elif op == '!=':
                            query = query.filter(getattr(cls, attr) != value)
                        elif op == '<':
                            query = query.filter(getattr(cls, attr) < value)
                        elif op == '>':
                            query = query.filter(getattr(cls, attr) > value)
                        elif op == '<=':
                            query = query.filter(getattr(cls, attr) <= value)
                        elif op == '>=':
                            query = query.filter(getattr(cls, attr) >= value)
                        elif op == 'like':
                            query = query.filter(getattr(cls, attr).like(value))
                        elif op == 'ilike':
                            query = query.filter(getattr(cls, attr).ilike(value))
                else:
                    query = query.filter(getattr(cls, attr) == condition)
        if order_by:
            for field, direction in order_by:
                if direction == 'asc':
                    query = query.order_by(asc(field))
                elif direction == 'desc':
                    query = query.order_by(desc(field))
        return query.all()

    @classmethod
    def create(cls, data):
        cls.validate(data)
        new_record = cls(**data)
        with cls.transaction():
            db.session.add(new_record)
            db.session.commit()
        return new_record

    @classmethod
    def validate(cls, data):
        pass  # To be overridden by subclasses

    def update(self, data):
        self.validate(data)
        with self.transaction():
            for key, value in data.items():
                setattr(self, key, value)
            db.session.commit()
        return self
    
    def save(self):
        self.validate(self.to_dict())
        self.updated_at = datetime.now()
        with self.transaction():
            db.session.commit()
        return self

    def delete(self):
        with self.transaction():
            db.session.delete(self)
            db.session.commit()
        return True

    @staticmethod
    @contextmanager
    def transaction():
        try:
            yield
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            if column.name in ['avatar', 'picture'] and value:
                value = get_presign_url_from_s3(value, location=f"{self.__tablename__}/{self.id}")
            result[column.name] = value
        return result

class Artist(ModelBase):
    __tablename__ = 'Artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    link_x = db.Column(db.String(255))
    style = db.Column(db.String(255))
    x_tag = db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    @classmethod
    def validate(cls, data):
        if 'name' not in data or not data['name']:
            raise ValueError("Artist name is required")
        if 'style' not in data or not data['style']:
            raise ValueError("Style is required")

        
class Team(ModelBase):
    __tablename__ = 'Teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    position = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    @classmethod
    def validate(cls, data):
        if 'name' not in data or not data['name']:
            raise ValueError("Name is required")
        if 'position' not in data or not data['position']:
            raise ValueError("Position is required")

class Gallery(ModelBase):
    __tablename__ = 'Galleries'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    show_on_top = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    @classmethod
    def validate(cls, data):
        if 'artist_id' not in data or not data['artist_id']:
            raise ValueError("Artist ID is required")

