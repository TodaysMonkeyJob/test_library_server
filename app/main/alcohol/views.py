# -*- coding:utf-8 -*-
from app import db
from app.models import Alcohol, Log, Comment, Permission, Tag, alcohol_tag
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user
from . import alcohol
from .forms import SearchForm, EditAlcoholForm, AddAlcoholForm
from ..comment.forms import CommentForm
from ..decorators import admin_required, permission_required


@alcohol.route('/')
def index():
    search_word = request.args.get('search', None)
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)

    the_alcohols = Alcohol.query
    if not current_user.can(Permission.UPDATE_ALCOHOL_INFORMATION):
        the_alcohols = Alcohol.query.filter_by(hidden=0)

    if search_word:
        search_word = search_word.strip()
        the_alcohols = the_alcohols.filter(db.or_(
            Alcohol.title.ilike(u"%%%s%%" % search_word), Alcohol.manufacturer.ilike(u"%%%s%%" % search_word), Alcohol.isbn.ilike(
                u"%%%s%%" % search_word), Alcohol.tags.any(Tag.name.ilike(u"%%%s%%" % search_word)), Alcohol.subtitle.ilike(
                u"%%%s%%" % search_word))).outerjoin(Log).group_by(Alcohol.id).order_by(db.func.count(Log.id).desc())
        search_form.search.data = search_word
    else:
        the_alcohols = Alcohol.query.order_by(Alcohol.id.desc())

    pagination = the_alcohols.paginate(page, per_page=8)
    result_alcohols = pagination.items
    return render_template("alcohol.html", alcohols=result_alcohols, pagination=pagination, search_form=search_form,
                           title=u"List of alcohols")


@alcohol.route('/<alcohol_id>/')
def detail(alcohol_id):
    the_alcohol = Alcohol.query.get_or_404(alcohol_id)

    if the_alcohol.hidden and (not current_user.is_authenticated or not current_user.is_administrator()):
        abort(404)

    show = request.args.get('show', 0, type=int)
    page = request.args.get('page', 1, type=int)
    form = CommentForm()

    if show in (1, 2):
        pagination = the_alcohol.logs.filter_by(returned=show - 1) \
            .order_by(Log.buy_timestamp.desc()).paginate(page, per_page=5)
    else:
        pagination = the_alcohol.comments.filter_by(deleted=0) \
            .order_by(Comment.edit_timestamp.desc()).paginate(page, per_page=5)

    data = pagination.items
    return render_template("alcohol_detail.html", alcohol=the_alcohol, data=data, pagination=pagination, form=form,
                           title=the_alcohol.title)


@alcohol.route('/<int:alcohol_id>/edit/', methods=['GET', 'POST'])
@permission_required(Permission.UPDATE_ALCOHOL_INFORMATION)
def edit(alcohol_id):
    alcohol = Alcohol.query.get_or_404(alcohol_id)
    form = EditAlcoholForm()
    if form.validate_on_submit():
        alcohol.isbn = form.isbn.data
        alcohol.title = form.title.data
        alcohol.origin_title = form.origin_title.data
        alcohol.subtitle = form.subtitle.data
        alcohol.manufacturer = form.manufacturer.data
        alcohol.translator = form.translator.data
        alcohol.distributor = form.distributor.data
        alcohol.image = form.image.data
        alcohol.pubdate = form.pubdate.data
        alcohol.tags_string = form.tags.data
        alcohol.pages = form.pages.data
        alcohol.price = form.price.data
        alcohol.binding = form.binding.data
        alcohol.numbers = form.numbers.data
        alcohol.summary = form.summary.data
        alcohol.catalog = form.catalog.data
        db.session.add(alcohol)
        db.session.commit()
        flash(u'Alcohol data has been saved!', 'success')
        return redirect(url_for('alcohol.detail', alcohol_id=alcohol_id))
    form.isbn.data = alcohol.isbn
    form.title.data = alcohol.title
    form.origin_title.data = alcohol.origin_title
    form.subtitle.data = alcohol.subtitle
    form.manufacturer.data = alcohol.manufacturer
    form.translator.data = alcohol.translator
    form.distributor.data = alcohol.distributor
    form.image.data = alcohol.image
    form.pubdate.data = alcohol.pubdate
    form.tags.data = alcohol.tags_string
    form.pages.data = alcohol.pages
    form.price.data = alcohol.price
    form.binding.data = alcohol.binding
    form.numbers.data = alcohol.numbers
    form.summary.data = alcohol.summary or ""
    form.catalog.data = alcohol.catalog or ""
    return render_template("alcohol_edit.html", form=form, alcohol=alcohol, title=u"Edit alcohol information")


@alcohol.route('/add/', methods=['GET', 'POST'])
@permission_required(Permission.ADD_ALCOHOL)
def add():
    form = AddAlcoholForm()
    form.numbers.data = 3
    if form.validate_on_submit():
        new_alcohol = Alcohol(
            isbn=form.isbn.data,
            title=form.title.data,
            origin_title=form.origin_title.data,
            subtitle=form.subtitle.data,
            manufacturer=form.manufacturer.data,
            translator=form.translator.data,
            distributor=form.distributor.data,
            image=form.image.data,
            pubdate=form.pubdate.data,
            tags_string=form.tags.data,
            pages=form.pages.data,
            price=form.price.data,
            binding=form.binding.data,
            numbers=form.numbers.data,
            summary=form.summary.data or "",
            catalog=form.catalog.data or "")
        db.session.add(new_alcohol)
        db.session.commit()
        flash(u'Alcohol %s has been added to the library!' % new_alcohol.title, 'success')
        return redirect(url_for('alcohol.detail', alcohol_id=new_alcohol.id))
    return render_template("alcohol_edit.html", form=form, title=u"Add new alcohol")


@alcohol.route('/<int:alcohol_id>/delete/')
@permission_required(Permission.DELETE_ALCOHOL)
def delete(alcohol_id):
    the_alcohol = Alcohol.query.get_or_404(alcohol_id)
    the_alcohol.hidden = 1
    db.session.add(the_alcohol)
    db.session.commit()
    flash(u'The alcohol was successfully deleted, and the user can no longer view the alcohol', 'info')
    return redirect(request.args.get('next') or url_for('alcohol.detail', alcohol_id=alcohol_id))


@alcohol.route('/<int:alcohol_id>/put_back/')
@admin_required
def put_back(alcohol_id):
    the_alcohol = Alcohol.query.get_or_404(alcohol_id)
    the_alcohol.hidden = 0
    db.session.add(the_alcohol)
    db.session.commit()
    flash(u'The alcohol was successfully restored, and the user can now view the alcohol', 'info')
    return redirect(request.args.get('next') or url_for('alcohol.detail', alcohol_id=alcohol_id))


@alcohol.route('/tags/')
def tags():
    search_tags = request.args.get('search', None)
    page = request.args.get('page', 1, type=int)
    the_tags = Tag.query.outerjoin(alcohol_tag).group_by(alcohol_tag.c.tag_id).order_by(
        db.func.count(alcohol_tag.c.alcohol_id).desc()).limit(30).all()
    search_form = SearchForm()
    search_form.search.data = search_tags

    data = None
    pagination = None

    if search_tags:
        tags_list = [s.strip() for s in search_tags.split(',') if len(s.strip()) > 0]
        if len(tags_list) > 0:
            the_alcohols = Alcohol.query
            if not current_user.can(Permission.UPDATE_ALCOHOL_INFORMATION):
                the_alcohols = Alcohol.query.filter_by(hidden=0)
            the_alcohols = the_alcohols.filter(
                db.and_(*[Alcohol.tags.any(Tag.name.ilike(word)) for word in tags_list])).outerjoin(Log).group_by(
                Alcohol.id).order_by(db.func.count(Log.id).desc())
            pagination = the_alcohols.paginate(page, per_page=8)
            data = pagination.items

    return render_template('alcohol_tag.html', tags=the_tags, title='Tags', search_form=search_form, alcohols=data,
                           pagination=pagination)
