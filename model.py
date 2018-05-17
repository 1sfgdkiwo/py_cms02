import os
import os.path as op

from flask_admin import form
from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship, backref

import setting
from setting import app


db = SQLAlchemy(app)

class Page(db.Model):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    title =  db.Column(db.String(150))
    tag = db.Column(db.String(100))
    contents = db.Column(db.Text)
    url = db.Column(db.String(100))
    is_homepage = Column(Boolean)
    image_id=Column(Integer, ForeignKey('image.id'))
    feature_image=relationship('Image', backref='Page', cascade='all,delete')

    def __repr__(self):
        return self.title

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Unicode(128))

    def __repr__(self):
        return self.path


@listens_for(Image, 'after_delete')
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(setting.FILE_PATH, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(setting.FILE_PATH,
                              form.thumbgen_filename(target.path)))
        except OSError:
            pass




class Menu(db.Model):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    title = db.Column(db.String(100))
    order = Column(Integer)

    page_id = Column(Integer, ForeignKey('page.id'))
    page = relationship('Page', backref=backref('Linked from Menu', uselist=False))

    def __repr__(self):
        return self.title

# Define models
roles_users=db.Table('roles_users',
                     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(100), unique=True)
    description=db.Column(db.String(255))

    def __repr__(self):
        return self.name

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(255), unique=True)
    password=db.Column(db.String(255))
    active=db.Column(db.Boolean())
    confirmed_at=db.Column(db.DateTime())
    roles=db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return self.email

# udah ditangani oleh alembic , tp mesti pakai docker
db.create_all()
db.session.commit()