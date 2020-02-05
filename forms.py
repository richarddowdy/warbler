from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired(), Length(max=140)])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[
                           DataRequired(), Length(max=20)])
    email = StringField(
        'E-mail', validators=[DataRequired(), Email(), Length(max=60)])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL', validators=[URL()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[
                           DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditUserForm(FlaskForm):
    """Edit user form. """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL', validators=[URL()])
    header_image_url = StringField(
        '(Optional) Header Image URL', validators=[URL()])
    bio = StringField('(Optional) bio',  validators=[Length(max=140)])
    password = PasswordField('Password', validators=[Length(min=6)])
    # only authenticate pw
