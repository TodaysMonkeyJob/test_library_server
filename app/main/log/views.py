# -*- coding:utf-8 -*-
from app import db
from app.models import Alcohol, Log, Permission
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from . import log
from ..decorators import permission_required


@log.route('/buy/')
@login_required
@permission_required(Permission.BUY_ALCOHOL)
def alcohol_buy():
    alcohol_id = request.args.get('alcohol_id')
    the_alcohol = Alcohol.query.get_or_404(alcohol_id)
    if the_alcohol.hidden and not current_user.is_administrator():
        abort(404)

    result, message = current_user.buy_alcohol(the_alcohol)
    flash(message, 'success' if result else 'danger')
    db.session.commit()
    return redirect(request.args.get('next') or url_for('alcohol.detail', alcohol_id=alcohol_id))


@log.route('/return/')
@login_required
@permission_required(Permission.RETURN_ALCOHOL)
def alcohol_return():
    log_id = request.args.get('log_id')
    alcohol_id = request.args.get('alcohol_id')
    the_log = None
    if log_id:
        the_log = Log.query.get(log_id)
    if alcohol_id:
        the_log = Log.query.filter_by(user_id=current_user.id, alcohol_id=alcohol_id).first()
    if log is None:
        flash(u'This record was not found', 'warning')
    else:
        result, message = current_user.return_alcohol(the_log)
        flash(message, 'success' if result else 'danger')
        db.session.commit()
    return redirect(request.args.get('next') or url_for('alcohol.detail', alcohol_id=log_id))


@log.route('/')
@login_required
def index():
    show = request.args.get('show', 0, type=int)
    if show != 0:
        show = 1

    page = request.args.get('page', 1, type=int)
    pagination = Log.query.filter_by(returned=show).order_by(Log.buy_timestamp.desc()).paginate(page, per_page=10)
    logs = pagination.items
    return render_template("logs_info.html", logs=logs, pagination=pagination, title=u"Purchase information")
