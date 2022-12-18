from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from software_design_lab.models import User


class RegistrationFormUser(FlaskForm):
    first_name = StringField('FirstName', 
                            validators=[DataRequired(), Length(min=2, max=60)])
    surname = StringField('Surname', 
                            validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already used')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=60)])
    surname = StringField('Surname',
                           validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RegistrationFormAuthor(FlaskForm):
    first_name = StringField('FirstName', 
                            validators=[DataRequired(), Length(min=2, max=60)])
    surname = StringField('Surname', 
                            validators=[DataRequired(), Length(min=2, max=60)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField()
    submit = SubmitField('Login')

class PublishForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    publication_pdf = FileField('Upload article as PDF', validators=[FileAllowed(['pdf']), DataRequired()])
    article_authors = StringField('Article authors', validators=[DataRequired()])
    submit = SubmitField('Publish')

class UpdatePublicationForm(FlaskForm):
    title = StringField('Title',
                           validators=[DataRequired(), Length(max=200)])
    article_authors = StringField('Aricle authors',
                           validators=[DataRequired(), Length(max=200)])
    abstract = TextAreaField('Abstract',
                           validators=[DataRequired(), Length(max=3000)])
    simple_desc = TextAreaField('Simple Description',
                           validators=[DataRequired(), Length(max=3000)])
    submit = SubmitField('Update')