from flask import request, url_for, app
from flask_admin import AdminIndexView, form
# from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from markupsafe import Markup
from werkzeug.utils import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from setting import FILE_PATH


class SecuredAdminIndexView(AdminIndexView):
    def __init__(self):
        super(SecuredAdminIndexView, self).__init__(template='admin/index.html', url='/admin')

    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(request.full_path)
        return redirect(url_for('security.login',next=request.full_path))


class AdminOnlyView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(request.full_path)
        return redirect(url_for('security.login',next=request.full_path))




# ckeditor di admin
class CKEditorWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKEditorWidget, self).__call__(field, **kwargs)


class CKEditorField(TextAreaField):
    widget = CKEditorWidget()

class PageModelView(AdminOnlyView):
    form_overrides = dict(contents=CKEditorField)
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
    column_list = ('title', 'contents')

class UserModelView(AdminOnlyView):
    pass

class MenuModelView(AdminOnlyView):
    pass


class ImageView(AdminOnlyView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ''
        url='/static/upload/' + form.thumbgen_filename(model.path)
        return Markup('<a href="{}" target="_blank"><img src="{}"></a>'.format(url, url))

    column_formatters = {
        'path': _list_thumbnail
    }

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'path': form.ImageUploadField('Image',
                                      base_path=FILE_PATH,
                                      thumbnail_size=(100, 100, True))



    }