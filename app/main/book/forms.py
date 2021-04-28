# -*- coding:utf-8 -*-
from app.models import Book
from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import ValidationError
from wtforms.validators import Length, DataRequired, Regexp


class EditBookForm(FlaskForm):
    isbn = StringField(u"ISBN",
                       validators=[DataRequired(message=u"You forgot to fill in this item!"),
                                   Regexp('[0-9]{13,13}', message=u"ISBN must be 13 digits")])
    title = StringField(u"Title",
                        validators=[DataRequired(message=u"You forgot to fill in this item!"), Length(1, 128, message=u"1 to 128 characters in length")])
    origin_title = StringField(u"Origin title", validators=[Length(0, 128, message=u"Up to 128 characters in length")])
    subtitle = StringField(u"Subtitle", validators=[Length(0, 128, message=u"Up to 128 characters in length")])
    author = StringField(u"Author", validators=[Length(0, 128, message=u"Up to 64 characters in length")])
    translator = StringField(u"translator", validators=[Length(0, 64, message=u"Up to 64 characters in length")])
    publisher = StringField(u"Publisher", validators=[Length(0, 64, message=u"Up to 64 characters in length")])
    image = StringField(u"Image", validators=[Length(0, 128, message=u"Up to 128 characters in length")])
    pubdate = StringField(u"Publication date", validators=[Length(0, 32, message=u"Up to 32 characters in length")])
    tags = StringField(u"Tags", validators=[Length(0, 128, message=u"Up to 128 characters in length")])
    pages = IntegerField(u"Pages")
    price = StringField(u"Price", validators=[Length(0, 64, message=u"Up to 32 characters in length")])
    binding = StringField(u"Binding", validators=[Length(0, 16, message=u"Up to 16 characters in length")])
    numbers = IntegerField(u"Collection", validators=[DataRequired(message=u"You forgot to fill in this item!")])
    summary = PageDownField(u"Brief introduction")
    catalog = PageDownField(u"Table of contents")
    submit = SubmitField(u"Save Changes")


class AddBookForm(EditBookForm):
    def validate_isbn(self, filed):
        if Book.query.filter_by(isbn=filed.data).count():
            raise ValidationError(u'The same ISBN already exists and cannot be entered, please check carefully whether the book is already in stock.')


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField(u"Search for")


