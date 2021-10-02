from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, DateField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import Email, InputRequired, Length, EqualTo

class SignUpForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])
    password2 = PasswordField("Re-enter password", validators=[InputRequired(), EqualTo("password")])

    email = StringField("E-mail", 
    validators=[InputRequired(), Length(min=6, max=100), Email(message="Invalid email try again")])
   
class ChangeForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    image_link = StringField("image link")
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])
    password2 = PasswordField("Re-enter password", validators=[InputRequired(), EqualTo("password")])

    email = StringField("E-mail", 
    validators=[InputRequired(), Length(min=6, max=100), Email(message="Invalid email try again")])


class LogInForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=60)])
    rememberme = BooleanField("Remember me")


class MoviesForm(Form):
    title = StringField("title", validators=[InputRequired(), Length(min=4, max=50)])
    description = TextAreaField("description")
    image_link = StringField("image link")
    