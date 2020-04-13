from flask import session, request, abort, url_for
from flask_restplus import Namespace, Resource
from CTFd.models import (
    db,
    Category,
)
from CTFd.utils.decorators import (
    during_ctf_time_only,
    require_verified_emails,
    admins_only,
    authed_only
)

category_namespace = Namespace('category',
                                 description="Endpoint to retrieve Category")


@category_namespace.route('')
class ShowCategory(Resource):
    @during_ctf_time_only
    @require_verified_emails
    def get(self):
        from fyp import showCategoryDesc
        return {
            "success":True,
            'data': showCategoryDesc()
        }


    @admins_only
    def post(self):
        if request.content_type != 'application/json':
            request_data = request.form
        else:
            request_data = request.get_json()
        data = request_data.get("data")
        Category.query.delete()
        db.session.commit()
        import re
        for i in re.findall("<span>(.*)</span>",data):
            db.session.add(Category(name=i))
        db.session.commit()
        return "Success"



@category_namespace.route('/new')
class NewCategory(Resource):
    @admins_only
    def post(self):
        if request.content_type != 'application/json':
            request_data = request.form
        else:
            request_data = request.get_json()
        name = request_data.get("name")
        db.session.add(Category(name=name))
        db.session.commit()
        return "Success"

@category_namespace.route('/edit')
class EditCategory(Resource):
    @admins_only
    def post(self):
        if request.content_type != 'application/json':
            request_data = request.form
        else:
            request_data = request.get_json()
        id = int(request_data.get("id"))
        name = request_data.get("name")
        desc = request_data.get("description")
        c = Category.query.filter_by(id=id).first_or_404()
        c.name = name
        c.description = desc
        db.session.commit()
        return "Success"