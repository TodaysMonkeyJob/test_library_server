# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import bleach
from app import db, lm, avatars
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64))
    password_hash = db.deferred(db.Column(db.String(128)))
    major = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    headline = db.Column(db.String(32), nullable=True)
    about_me = db.deferred(db.Column(db.Text, nullable=True))
    about_me_html = db.deferred(db.Column(db.Text, nullable=True))
    avatar = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email.lower() == current_app.config['FLASKY_ADMIN'].lower():
                self.role = Role.query.filter_by(permissions=0x1ff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        self.member_since = datetime.now()

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    logs = db.relationship('Log',
                           backref=db.backref('user', lazy='joined'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')

    comments = db.relationship('Comment',
                               backref=db.backref('user', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.email

    def purchase(self, alcohol):
        return self.logs.filter_by(alcohol_id=alcohol.id, returned=0).first()

    def can_buy_alcohol(self):
        return self.logs.filter(Log.returned == 0, Log.return_timestamp < datetime.now()).count() == 0

    def buy_alcohol(self, alcohol):
        if self.logs.filter(Log.returned == 0, Log.return_timestamp < datetime.now()).count() > 0:
            return False, u"Unable to buy, you have overdue alcohols that have not been returned"
        if self.purchase(alcohol):
            return False, u'It looks like you have already purchased this alcohol!!'
        if not alcohol.can_buy():
            return False, u'This alcohol is too popular, we no longer have the collection, please wait for someone to return it and buy it later'

        db.session.add(Log(self, alcohol))
        return True, u'You successfully GET a copy %s' % alcohol.title

    def return_alcohol(self, log):
        if log.returned == 1 or log.user_id != self.id:
            return False, u'This record was not found'
        log.returned = 1
        log.return_timestamp = datetime.now()
        db.session.add(log)
        return True, u'You returned a copy %s' % log.alcohol.title

    def avatar_url(self, _external=False):
        if self.avatar:
            avatar_json = json.loads(self.avatar)
            if avatar_json['use_out_url']:
                return avatar_json['url']
            else:
                return url_for('_uploads.uploaded_file', setname=avatars.name, filename=avatar_json['url'],
                               _external=_external)
        else:
            return url_for('static', filename='img/avatar.png', _external=_external)

    @staticmethod
    def on_changed_about_me(target, value, oldvalue, initiaor):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquate', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.about_me_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True))


db.event.listen(User.about_me, 'set', User.on_changed_about_me)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


lm.anonymous_user = AnonymousUser


class Permission(object):
    RETURN_ALCOHOL = 0x01
    BUY_ALCOHOL = 0x02
    WRITE_COMMENT = 0x04
    DELETE_OTHERS_COMMENT = 0x08
    UPDATE_OTHERS_INFORMATION = 0x10
    UPDATE_ALCOHOL_INFORMATION = 0x20
    ADD_ALCOHOL = 0x40
    DELETE_ALCOHOL = 0x80
    ADMINISTER = 0x100


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.RETURN_ALCOHOL |
                     Permission.BUY_ALCOHOL |
                     Permission.WRITE_COMMENT, True),
            'Moderator': (Permission.RETURN_ALCOHOL |
                          Permission.BUY_ALCOHOL |
                          Permission.WRITE_COMMENT |
                          Permission.DELETE_OTHERS_COMMENT, False),
            'Administrator': (0x1ff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Alcohol(db.Model):
    __tablename__ = 'alcohols'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(16), unique=True)
    title = db.Column(db.String(128))
    origin_title = db.Column(db.String(128))
    subtitle = db.Column(db.String(128))
    manufacturer = db.Column(db.String(128))
    translator = db.Column(db.String(64))
    distributor = db.Column(db.String(64))
    image = db.Column(db.String(128))
    pubdate = db.Column(db.String(32))
    pages = db.Column(db.Integer)
    price = db.Column(db.String(16))
    binding = db.Column(db.String(16))
    numbers = db.Column(db.Integer, default=10)
    summary = db.deferred(db.Column(db.Text, default=""))
    summary_html = db.deferred(db.Column(db.Text))
    catalog = db.deferred(db.Column(db.Text, default=""))
    catalog_html = db.deferred(db.Column(db.Text))
    hidden = db.Column(db.Boolean, default=0)

    logs = db.relationship('Log',
                           backref=db.backref('alcohol', lazy='joined'),
                           lazy='dynamic',
                           cascade='all, delete-orphan')

    comments = db.relationship('Comment', backref='alcohol',
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    @property
    def tags_string(self):
        return ",".join([tag.name for tag in self.tags.all()])

    @tags_string.setter
    def tags_string(self, value):
        self.tags = []
        tags_list = value.split(u',')
        for str in tags_list:
            tag = Tag.query.filter(Tag.name.ilike(str)).first()
            if tag is None:
                tag = Tag(name=str)

            self.tags.append(tag)

        db.session.add(self)
        db.session.commit()

    def can_buy(self):
        return (not self.hidden) and self.can_buy_number() > 0

    def can_buy_number(self):
        return self.numbers - Log.query.filter_by(alcohol_id=self.id, returned=0).count()

    @staticmethod
    def on_changed_summary(target, value, oldvalue, initiaor):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquate', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.summary_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True))

    @staticmethod
    def on_changed_catalog(target, value, oldvalue, initiaor):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquate', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.catalog_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags, strip=True))

    def __repr__(self):
        return u'<Alcohol %r>' % self.title


db.event.listen(Alcohol.summary, 'set', Alcohol.on_changed_summary)
db.event.listen(Alcohol.catalog, 'set', Alcohol.on_changed_catalog)


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    alcohol_id = db.Column(db.Integer, db.ForeignKey('alcohols.id'))
    buy_timestamp = db.Column(db.DateTime, default=datetime.now())
    return_timestamp = db.Column(db.DateTime, default=datetime.now())
    returned = db.Column(db.Boolean, default=0)

    def __init__(self, user, alcohol):
        self.user = user
        self.alcohol = alcohol
        self.buy_timestamp = datetime.now()
        self.return_timestamp = datetime.now() + timedelta(days=30)
        self.returned = 0

    def __repr__(self):
        return u'<%r - %r>' % (self.user.name, self.alcohol.title)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    alcohol_id = db.Column(db.Integer, db.ForeignKey('alcohols.id'))
    comment = db.Column(db.String(1024))
    create_timestamp = db.Column(db.DateTime, default=datetime.now())
    edit_timestamp = db.Column(db.DateTime, default=datetime.now())
    deleted = db.Column(db.Boolean, default=0)

    def __init__(self, alcohol, user, comment):
        self.user = user
        self.alcohol = alcohol
        self.comment = comment
        self.create_timestamp = datetime.now()
        self.edit_timestamp = self.create_timestamp
        self.deleted = 0


alcohol_tag = db.Table('alcohols_tags',
                    db.Column('alcohol_id', db.Integer, db.ForeignKey('alcohols.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                    )


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    alcohols = db.relationship('Alcohol',
                            secondary=alcohol_tag,
                            backref=db.backref('tags', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return u'<Tag %s>' % self.name
