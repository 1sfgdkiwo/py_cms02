# from urllib import urlopen

from flask import render_template, url_for
# from flask_admin import Admin
from flask_admin import Admin
from setting import app
from view import SecuredAdminIndexView, PageModelView, UserModelView, MenuModelView, ImageView

app.config.from_pyfile('setting.py')

from flask_security import SQLAlchemyUserDatastore, Security

# from setting import app
from model import db, Page, Menu, User, Role, Image  #
import global_vars as global_vars
from bs4 import BeautifulSoup
import requests

# app.config.from_pyfile('setting.py')

db.init_app(app)
# build_sample_db()

admin = Admin(app, 'Admin', template_mode='bootstrap3',\
                    index_view=SecuredAdminIndexView())

admin.add_view(PageModelView(Page, db.session))
admin.add_view(MenuModelView(Menu, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(ImageView(Image, db.session))

user_datastore = SQLAlchemyUserDatastore(db,User,Role)
security = Security(app,user_datastore)



@app.route('/')
@app.route('/<url>')
def index(url=None):
    if url is not None:
        page = Page.query.filter_by(url=url).first()
        isi_hal = Page.query.filter_by(url=url).first()
    else:
        page = Page.query.filter_by(is_homepage=True).first()
        isi_hal = Page.query.filter(Page.title != 'homepage' ,Page.title != 'about').all()
    if page is None:
        # arahkan ke halaman 404
        return "Hal tdk ditemukan. ".format(url)
    contents = 'empty'
    # contents_isi='empty'
    if page is not None:
        contents = page.contents
        # judul_isi = isi_hal.title
        isinya = isi_hal
    # menu = Menu.query.order_by('order')
    # return render_template('index.html',TITLE='Flask Web App',CONTENTS=contents, \
    #                        isinya=isinya, global_vars=global_vars,MENU=menu)
    return render_template('index.html', TITLE='Flask Web App', CONTENTS=contents, \
                           isinya=isinya, global_vars=global_vars)
@app.route('/about')
def about():
    isi_about=Page.query.filter_by(title='About').first()
    if isi_about is not None:
        aboutnya = isi_about
        menu=Menu.query.order_by('order')
    return render_template('about.html',TITLE='Flask Web App',Aboutnya=aboutnya, global_vars=global_vars,MENU=menu)

@app.route('/page/<url>')
def page(url=None):



    isi_hal = Page.query.filter(Page.url=='page/'+ url).first()

    isi_semua=Page.query.filter(Page.title != 'homepage' ,Page.title != 'about').all()


    req=requests.get\
    ('http://rumahkode.wordpress.com')
    # req=requests.get\
    #     ('https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-the-tree')
    c=req.content
    soup=BeautifulSoup(c)

    # soup=BeautifulSoup('page/'+ url)
    bacah3=soup.find_all('h2')
    # bacah3=soup.find_all('title')


    if isi_hal is None:
        # arahkan ke halaman 404
        return "Hal tdk ditemukan !".format(url)

    if isi_hal is not None:
        isi_hal=isi_hal
        isi_semua=isi_semua
        bacah3=bacah3
    return render_template('page/page.html', TITLE='Flask Web App', \
                           isinya=isi_hal,bacah3=bacah3,isi_semua=isi_semua)

    # return render_template('page/page.html', TITLE='Flask Web App', \
    #                        isinya=isi_hal,isi_semua=isi_semua)



if __name__ == '__main__':
    app.run(debug=True, port=5555)