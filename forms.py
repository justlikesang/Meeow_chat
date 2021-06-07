from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField
from wtforms.validators import Optional, DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])
    picture = StringField('picture', validators=[Optional()])
    emoji = RadioField('emoji', choices=[('😺', '😺'),
        ('😹', '😹'), ('🙀', '🙀'), ('😼', '😼'), 
        ('😾', '😾'), ('🐱', '🐱'), ('😻', '😻')], validators=[Optional()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[Optional()])
    email = StringField('E-mail', validators=[Email(), Optional()])
    password = PasswordField('Password', validators=[Length(min=6),
                                                     Optional()])
    image_url = StringField('(Optional) Image URL', validators=[Optional()])
    header_image_url = StringField('(Optional) Image URL',
                                   validators=[Optional()])
    bio = StringField('Bio', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
