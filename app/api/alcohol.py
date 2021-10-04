from app.models import Alcohol as model_Alcohol
from flask import url_for
from flask_restful import Resource, marshal_with, abort
from . import api, parser, default_per_page
from .fields import alcohol_detail_fields, alcohol_list


@api.route('/alcohols/<int:alcohol_id>/')
class Alcohol(Resource):
    @marshal_with(alcohol_detail_fields)
    def get(self, alcohol_id):
        alcohol = model_Alcohol.query.get_or_404(alcohol_id)
        if alcohol.hidden:
            abort(404)
            abort(404)
        return alcohol


@api.route('/alcohols/')
class AlcoholList(Resource):
    @marshal_with(alcohol_list)
    def get(self):
        args = parser.parse_args()
        page = args['page'] or 1
        per_page = args['per_page'] or default_per_page
        pagination = model_Alcohol.query.paginate(page=page, per_page=per_page)
        items = pagination.items
        prev = None
        if pagination.has_prev:
            prev = url_for('api.alcohollist', page=page - 1, count=per_page, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('api.alcohollist', page=page + 1, count=per_page, _external=True)
        return {
            'items': items,
            'prev': prev,
            'next': next,
            'total': pagination.total,
            'pages_count': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page,
        }