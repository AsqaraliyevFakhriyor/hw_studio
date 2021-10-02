import sys
from flask import ( 
flash,
jsonify,
render_template,
redirect,
url_for,
Blueprint,
current_app,
)
from forms import (
    SignUpForm,
    LogInForm
)
from database.models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user


auth = Blueprint("auth", __name__)

"""
Sign up for Users
"""
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        users = Users.query.all()

        for user in users:
            if user.username == form.username.data:
                flash("Username '" + form.username.data + "' is already exist!")
                return redirect(url_for("auth.signup"))

        if form.password.data != form.password2.data:
            flash("Passwords does not match")
            return redirect(url_for("auth.signup"))

        try:
            hashed_password = generate_password_hash(form.password.data, method="sha256")
            new_user = Users(
                username = form.username.data,
                email = form.email.data,
                password = hashed_password
            )
            new_user.insert()


        except Exception as e:
            error = sys.exc_info()
            print(error)
            flash("An error occured!"+ str(error))
            return redirect(url_for("auth.signup"))

        finally:
            flash("Successfully signed!")
            login_user(new_user, remember=True)
            return redirect(url_for("movie_app.get_movies"))

    return render_template('signup.html', form=form)


"""
Login for users
"""
@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LogInForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).one_or_none()

        if user:
            if check_password_hash(user.password, form.password.data):
                flash("Successfully authorized!")
                login_user(user, remember=form.rememberme.data)
                return redirect(url_for('movie_app.get_movies'))
                
            else:
                flash("Password for user '" + form.username.data + "' is wrong!")
                redirect(url_for("auth.login"))
        else:
            flash("User '" + form.username.data + "' doesn\'t exist!")
            return redirect(url_for("auth.login"))    
    return render_template("login.html", form=form)


"""
Logout for users
"""
@auth.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully!")
    return redirect(url_for("movie_app.get_movies"))