# -*- coding:utf-8 -*-
from app import db
from app.models import Alcohol, Comment, Permission
from flask import url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from . import comment
from .forms import CommentForm
from ..decorators import permission_required


@comment.route('/add/<int:alcohol_id>/', methods=['POST', ])
@login_required
@permission_required(Permission.WRITE_COMMENT)
def add(alcohol_id):
    form = CommentForm()
    the_alcohol = Alcohol.query.get_or_404(alcohol_id)
    if the_alcohol.hidden and not current_user.is_administrator():
        abort(404)

    if form.validate_on_submit():
        the_comment = Comment(user=current_user, alcohol=the_alcohol, comment=form.comment.data)
        db.session.add(the_comment)
        db.session.commit()
        flash(u'Alcohol review has been successfully published', 'success')
    return redirect(request.args.get('next') or url_for('alcohol.detail', alcohol_id=alcohol_id))


@comment.route('/delete/<int:comment_id>')
@login_required
def delete(comment_id):
    the_comment = Comment.query.get_or_404(comment_id)
    if current_user.id == the_comment.user_id or current_user.can(Permission.DELETE_OTHERS_COMMENT):
        the_comment.deleted = 1
        alcohol_id = the_comment.alcohol_id
        db.session.add(the_comment)
        db.session.commit()
        flash(u'Successfully deleted a comment.', 'info')
        return redirect(request.args.get('next') or url_for('alcohol.detail', alcohol_id=alcohol_id))
    else:
        abort(403)
