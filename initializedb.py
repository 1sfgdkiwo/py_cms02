from flask_sqlalchemy import SQLAlchemy

from model import Page, User, Role, Image
from setting import app

db = SQLAlchemy(app)


# db.drop_all()
# db.create_all()

page = Page()
x=page.query.filter_by(title='homepage').first()
if x is None:
    page.title='homepage'
    page.contents='<h1> Selamat datang di dunia python </h1>'
    page.is_homepage=True
    db.session.add(page)
    db.session.commit()

# x1=page.query.filter_by(title='Hallo Dunia').first()
# if x1 is None:
#     page.title='Hallo Dunia'
#     page.contents='<h1> Hallo Dunia ? apa kabar... </h1>'
#     page.is_homepage=False
#     page.url='page/hallo-dunia'
#     page.image_id=1
#     db.session.add(page)
#     db.session.commit()

gbr=Image()
x=gbr.query.filter_by(path='beranda.jpeg').first()
if x is None:
    gbr.path='beranda.jpeg'
    db.session.add(gbr)
    db.session.commit()


role = Role()
x=role.query.filter_by(name='admin').first()
# db.session.delete(x)
# db.session.commit()
if x is None :
    role.name='admin'
    role.description='admin'
    db.session.add(role)
    db.session.commit()

user = User()
y=user.query.filter_by(email='aryotejow@gmail.com').first()
if y is None:
    user.email='aryotejow@gmail.com'
    user.password='123456'
    user.active=True
    user.roles.append(role)  # bagian ini yg beda
    db.session.add(user)
    db.session.commit()



