from flask_wtf import FlaskForm as Form
from wtforms import (
    StringField, 
    PasswordField, 
    BooleanField, 
    IntegerField, 
    SubmitField, 
    TextAreaField,
    SelectField)
from wtforms.validators import Email, InputRequired, Length, EqualTo
from wtforms.fields.html5 import DateField

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
    date = DateField("Release date", format='%Y-%m-%d')


class ActorsForm(Form):
    name = StringField("name", validators=[InputRequired(), Length(min=4, max=40)])
    age = IntegerField("age", validators=[InputRequired()])
    gender =  SelectField(u"Gender", choices=[("male", "male"), ("famale","famale")])
    actor_slogan = TextAreaField("actor slogan")
    image_link = StringField("image link", validators=[Length(min=6, max=2000)])  