from app.models import Log, Comment
from flask import url_for
from flask_restful import fields
from . import default_per_page

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'major': fields.String,
    'headline': fields.String,
    'about_me': fields.String,
    'about_me_html': fields.String,
    'avatar': fields.String(attribute=lambda x: x.avatar_url(_external=True)),
    'uri': fields.String(attribute=lambda x: url_for('api.user', user_id=x.id, _external=True)),
}
user_list = {
    'items': fields.List(fields.Nested(user_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'per_page': fields.Integer,
}

tag_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'alcohols_count': fields.Integer(attribute=lambda x: x.alcohols.count()),
    'uri': fields.String(attribute=lambda x: url_for('api.tag', tag_id=x.id, _external=True)),
}
tag_list = {
    'items': fields.List(fields.Nested(tag_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'count': fields.Integer,
}
alcohol_fields = {
    'id': fields.Integer,
    'isbn': fields.String,
    'title': fields.String,
    'origin_title': fields.String,
    'subtitle': fields.String,
    'manufacturer': fields.String,
    'translator': fields.String,
    'distributor': fields.String,
    'image': fields.String,
    'pubdate': fields.String,
    'pages': fields.Integer,
    'price': fields.String,
    'binding': fields.String,
    'numbers': fields.Integer,
    'hidden': fields.Boolean,
    'can_buy': fields.Boolean(attribute=lambda x: x.can_buy()),
    'can_buy_number': fields.Integer(attribute=lambda x: x.can_buy_number()),
    'tags': fields.List(fields.Nested(tag_fields), attribute=lambda x: x.tags),
    'uri': fields.String(attribute=lambda x: url_for('api.alcohol', alcohol_id=x.id, _external=True)),
}
alcohol_list = {
    'items': fields.List(fields.Nested(alcohol_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'per_page': fields.Integer,
}
logs_info_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'user_name': fields.String(attribute=lambda x: x.user.name),
    'alcohol_id': fields.Integer,
    'alcohol_title': fields.String(attribute=lambda x: x.alcohol.title),
    'buy_timestamp': fields.DateTime(dt_format='rfc822'),
    'return_timestamp': fields.DateTime(dt_format='rfc822'),
    'returned': fields.Boolean,
    'uri': fields.String(attribute=lambda x: url_for('api.log', log_id=x.id, _external=True)),
}
logs_info_list = {
    'items': fields.List(fields.Nested(logs_info_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'count': fields.Integer,
}
comment_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'user_name': fields.String(attribute=lambda x: x.user.name),
    'alcohol_id': fields.Integer,
    'alcohol_title': fields.String(attribute=lambda x: x.alcohol.title),
    'comment': fields.String,
    'create_timestamp': fields.DateTime,
    'edit_timestamp': fields.DateTime,
    'deleted': fields.Boolean,
    'uri': fields.String(attribute=lambda x: url_for('api.comment', comment_id=x.id, _external=True)),
}
comment_list = {
    'items': fields.List(fields.Nested(comment_fields)),
    'next': fields.String,
    'prev': fields.String,
    'total': fields.Integer,
    'pages_count': fields.Integer,
    'current_page': fields.Integer,
    'per_page': fields.Integer,
}
comment_detail_fields = dict(comment_fields, **{
    'user': fields.Nested(user_fields, attribute=lambda x: x.user),
    'alcohol': fields.Nested(alcohol_fields, attribute=lambda x: x.alcohol),
})

user_detail_fields = dict \
    (user_fields, **{
        'purchase_logs': fields.Nested(
            {
                'items': fields.List(fields.Nested(logs_info_fields),
                                     attribute=lambda this: this.items),
                'next': fields.String(
                    attribute=lambda this: url_for('api.loglist', user_id=this.items[0].alcohol_id, returned=0, page=2,
                                                   count=default_per_page,
                                                   _external=True) if this.has_next else None),
                'prev': fields.String(attribute=''),
                'total': fields.Integer,
                'pages_count': fields.Integer(attribute='pages'),
                'current_page': fields.Integer(default=1),
                'per_page': fields.Integer,
            }, attribute=lambda this: this.logs.filter_by(returned=0).order_by(Log.id.desc()).paginate(page=1,
                                                                                                       per_page=default_per_page)),

        'purchased_logs': fields.Nested(
            {
                'items': fields.List(fields.Nested(logs_info_fields),
                                     attribute=lambda this: this.items),
                'next': fields.String(
                    attribute=lambda this: url_for('api.loglist', user_id=this.items[0].alcohol_id, returned=1, page=2,
                                                   per_page=default_per_page,
                                                   _external=True) if this.has_next else None),
                'prev': fields.String(attribute=''),
                'total': fields.Integer,
                'pages_count': fields.Integer(attribute='pages'),
                'current_page': fields.Integer(default=1),
                'per_page': fields.Integer,
            }, attribute=lambda this: this.logs.filter_by(returned=1).order_by(Log.id.desc()).paginate(page=1,
                                                                                                       per_page=default_per_page)),

        'comments': fields.Nested(
            {
                'items': fields.List(fields.Nested(comment_fields),
                                     attribute=lambda this: this.items),
                'next': fields.String(
                    attribute=lambda this: url_for('api.commentlist', user_id=this.items[0].alcohol_id, deleted=0,
                                                   page=2, per_page=default_per_page,
                                                   _external=True) if this.has_next else None),
                'prev': fields.String(attribute=''),
                'total': fields.Integer,
                'pages_count': fields.Integer(attribute='pages'),
                'current_page': fields.Integer(default=1),
                'per_page': fields.Integer,
            },
            attribute=lambda this: this.comments.filter_by(deleted=0).order_by(Comment.id.desc()).paginate(page=1,
                                                                                                           per_page=default_per_page)),

    }
     )
alcohol_detail_fields = \
    dict(alcohol_fields,
         **{'summary': fields.String,
            'summary_html': fields.String,
            'catalog': fields.String,
            'catalog_html': fields.String,
            'purchase_logs': fields.Nested(
                {
                    'items': fields.List(fields.Nested(logs_info_fields),
                                         attribute=lambda this: this.items),
                    'next': fields.String(
                        attribute=lambda this: url_for('api.loglist', alcohol_id=this.items[0].alcohol_id,
                                                       returned=0, page=2,
                                                       count=default_per_page,
                                                       _external=True) if this.has_next else None),
                    'prev': fields.String(attribute=''),
                    'total': fields.Integer,
                    'pages_count': fields.Integer(attribute='pages'),
                    'current_page': fields.Integer(default=1),
                    'per_page': fields.Integer,
                }, attribute=lambda this: this.logs.filter_by(returned=0).order_by(
                    Log.id.desc()).paginate(page=1,
                                            per_page=default_per_page)),

            'purchased_logs': fields.Nested(
                {
                    'items': fields.List(fields.Nested(logs_info_fields),
                                         attribute=lambda this: this.items),
                    'next': fields.String(
                        attribute=lambda this: url_for('api.loglist', alcohol_id=this.items[0].alcohol_id,
                                                       returned=1, page=2,
                                                       per_page=default_per_page,
                                                       _external=True) if this.has_next else None),
                    'prev': fields.String(attribute=''),
                    'total': fields.Integer,
                    'pages_count': fields.Integer(attribute='pages'),
                    'current_page': fields.Integer(default=1),
                    'per_page': fields.Integer,
                }, attribute=lambda this: this.logs.filter_by(returned=1).order_by(
                    Log.id.desc()).paginate(page=1,
                                            per_page=default_per_page)),

            'comments': fields.Nested(
                {
                    'items': fields.List(fields.Nested(comment_fields),
                                         attribute=lambda this: this.items),
                    'next': fields.String(
                        attribute=lambda this: url_for('api.commentlist',
                                                       alcohol_id=this.items[0].alcohol_id, deleted=0,
                                                       page=2, per_page=default_per_page,
                                                       _external=True) if this.has_next else None),
                    'prev': fields.String(attribute=''),
                    'total': fields.Integer,
                    'pages_count': fields.Integer(attribute='pages'),
                    'current_page': fields.Integer(default=1),
                    'per_page': fields.Integer,
                },
                attribute=lambda this: this.comments.filter_by(deleted=0).order_by(
                    Comment.id.desc()).paginate(page=1,
                                                per_page=default_per_page)),

            }
         )

logs_info_detail_fields = dict(logs_info_fields, **{'user': fields.Nested(user_fields, attribute=lambda x: x.user),
                                                    'alcohol': fields.Nested(alcohol_fields, attribute=lambda x: x.alcohol)})

tag_detail_fields = dict(tag_fields, **{'alcohols': fields.List(fields.Nested(alcohol_fields), attribute=lambda x: x.alcohols)})
