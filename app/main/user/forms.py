# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, URL
from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileField, FileAllowed
from app import avatars


class EditProfileForm(FlaskForm):
    name = StringField(u'Username', validators=[DataRequired(message=u"You forgot to fill in this item!"), Length(1, 64, message=u"1 to 64 characters in length")])
    major = StringField(u'Major', validators=[Length(0, 128, message=u"Up to 64 characters in length")])
    headline = StringField(u'Introduce yourself in one sentence', validators=[Length(0, 32, message=u"Up to 32 characters in length")])
    about_me = PageDownField(u"Personal profile")
    submit = SubmitField(u"Save Changes")


class AvatarEditForm(FlaskForm):
    avatar_url = StringField('', validators=[Length(1, 100, message=u"The length is limited to 100 characters"), URL(message=u"Please fill in the correct URL")])
    submit = SubmitField(u"Save")


class AvatarUploadForm(FlaskForm):
    avatar = FileField('', validators=[FileAllowed(avatars, message=u"Only allow images to be uploaded")])
