from flask import current_app as app, render_template, render_template_string, url_for
from CTFd.utils.decorators import admins_only
from CTFd.admin import admin


@admin.route('/admin/category')
@admins_only
def category_listing():
    from fyp import showCategoryDesc
    return render_template('admin/category/category.html', category=showCategoryDesc())

@admin.route('/admin/category/new')
@admins_only
def category_new():
    return render_template('admin/category/new.html')

@admin.route('/admin/category/edit/<int:category_id>')
@admins_only
def category_edit(category_id):
    from fyp import selectCategory
    return render_template('admin/category/edit.html',category=selectCategory(category_id))