from flask import (
Flask,
render_template,
url_for,
jsonify,
redirect,
flash
)
from views.actors.actors import actor_app
from views.movies.movies import movie_app
from auth.auth import auth
from flask_bootstrap import Bootstrap
from database.models import setup_db, Users, db
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required
from helpers import insert_actor, inserting_movie, insert_user_admin, insert_movies_rates, insert_movies_comments
from forms import ChangeForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
setup_db(app)



Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
# app.register_blueprint(actors, url_perfix = "/app")
app.register_blueprint(movie_app, url_perfix = "/")
app.register_blueprint(auth)
app.register_blueprint(actor_app, url_perfix = "/")


CORS(
    app,
    resources = {r"/api/*": {"origins": "*"}}
)


"""
Adding headers 
"""
@app.after_request
def after_request(response):
	response.headers.add('Access-Conrool-Allow-Headers', 'Content-Type, Authorization, true')
	response.headers.add('Access-Conrool-Allow-Methods', 'GET, POST, PUT, PATCH, OPTION')
	return response


"""
Home page endpoint
"""
@app.route("/")
def redirect_to_home():
    return redirect(url_for("movie_app.get_movies"))


@app.route("/userprofile" , methods=["POST", "GET"])
@login_required
def user_profile():
    cur_user = Users.query.filter(Users.id == current_user.id).one_or_none()
    form = ChangeForm()

    """this script will work when user submit to change profile data"""
    if form.validate_on_submit():
        all_users = Users.query.filter(Users.id.notin_([current_user.id])).all()

        for user in all_users:
            if form.username.data == user.username:
                flash("The username already taken! please try again!")
                return redirect("http://127.0.0.1:5000/userprofile")

            if form.email.data == user.email:
                flash("The email already taken! try again!")
                return redirect("http://127.0.0.1:5000/userprofile")


        if form.password.data != form.password2.data:
            flash("Passwords does not match!, try agian!")
            return redirect("http://127.0.0.1:5000/userprofile")

        try:
            cur_user.username = form.username.data
            hashed_password = generate_password_hash(form.password.data, method="sha256")
            cur_user.password = hashed_password
            cur_user.email = form.email.data
            cur_user.image_link = form.image_link.data
            cur_user.update()
            flash("updated successfully!")
            return redirect("http://127.0.0.1:5000/userprofile")

        except Exception as e:
            print(sys.exc_info())
            flash("oops somthing went wrong!")
            return redirect("http://127.0.0.1:5000/userprofile")


    """geting data to send to front side"""
    try:
        form.username.data = current_user.username
        form.image_link.data = current_user.image_link
        form.email.data = current_user.email
    except Exception as e:
        flash("Error with geting data from database!")


    return render_template("profile.html", user=cur_user, form=form)

@app.route("/reset-database")
def reset_database():
    inserting_movie()
    insert_actor()
    insert_user_admin()
    insert_movies_rates()
    insert_movies_comments()
    return "successfully reseted"

"""
Login helper function
"""
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)