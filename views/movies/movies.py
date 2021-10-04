import sys
from flask import (
	Blueprint, 
	render_template, 
	request, 
	redirect, 
	url_for, 
	flash,
	)
from flask_login import current_user, login_required
from database.models import Movies, MoviesRates, Actors, MoviesComments, Users
from datetime import date
from forms import MoviesForm
# from helpers import comments
# from helpers import  movies_helper


movie_app = Blueprint("movie_app", __name__)
obj_per_page = 8


"""
Home route of Web Site
"""
@movie_app.route("/home")
@movie_app.route("/movies")
def get_movies(page=1):

	per_page = 8

	if request.args:
		page = int(request.args.get("page"))

	movies = Movies.query.order_by(Movies.date.desc()).paginate(page, per_page, error_out=False)

	return render_template('home.html', movies=movies, user = current_user, current_day = date.today())


"""
GET movie by id 
"""
@movie_app.route("/movie/<int:movie_id>")
def get_movie_by_id(movie_id):

	movie = Movies.query.filter(Movies.id == movie_id).one_or_none()


	"""getting actors which played role in specific movie"""	
	actors = Actors.query.filter(Actors.movie_id == movie_id).all()
	actors_count = Actors.query.filter(Actors.movie_id == movie_id).count()


	"""like section for movie"""
	like = MoviesRates.query.filter(MoviesRates.movie_id == movie_id).filter(MoviesRates.rate == True).all()
	dislikes = MoviesRates.query.filter(MoviesRates.movie_id == movie_id).filter(MoviesRates.rate == False).all()
	rates_count = MoviesRates.query.filter(MoviesRates.movie_id == movie_id).count()
	# liked_by = len(like) / rates_count * 100


	"""comment section for movie"""
	all_comments = MoviesComments.query.filter(
		MoviesComments.movie_id == movie_id
		).order_by(
		MoviesComments.comment_date.desc()
		).all()

	comments_count = len(all_comments)
	
	comments = []
	for comment in all_comments:
		comments.append({
		"id": comment.id,
		"comment": comment.comment,
		"comment_date": comment.comment_date,
		"user_id": comment.user_id,
		"username": (Users.query.filter(Users.id == comment.user_id).one_or_none()).username
		})
	print(comments)


	try:
		is_liked = MoviesRates.query.filter(
			MoviesRates.movie_id == movie_id
			).filter(
			 MoviesRates.user_id == current_user.id
			).one_or_none()

	except Exception as e:
		print(sys.exc_info())
		is_liked = "none"


	return render_template(
		"moviebyid.html", 
		movie = movie, 
		actors_data = actors, 
		current_user = current_user,
		actors_count = actors_count,
		likes = len(like),
		dislikes = len(dislikes),
		is_liked = is_liked,
		movie_rates_count = rates_count,
		comments = comments,
		comments_count = comments_count
		)


"""
Rate endpoint for Movies wihtout method definding
"""
@movie_app.route("/movie/rate")
@login_required
def movie_like():
	rate = bool(request.args.get("rate", ""))
	movie_id = int(request.args.get("movie_id"))
	already_liked = bool(request.args.get("is_liked", ""))

	old_rate = MoviesRates.query.filter(
		MoviesRates.user_id == current_user.id
		).filter(
		MoviesRates.movie_id == movie_id).one_or_none()

	if not already_liked and old_rate is None:
		rate = MoviesRates(
			rate = rate,
			user_id = current_user.id,
			movie_id = movie_id
			)
		rate.insert()
		return redirect("/movie/"+ str(movie_id))

	else:
		if old_rate is None:
			flash("Rate note found!")
			return redirect("/movie/"+ str(movie_id))

		if old_rate.rate == rate:
			old_rate.delete()
		else:
			old_rate.rate = rate
			old_rate.update() 

		flash("Rate updated successfully!")
		return redirect("/movie/"+ str(movie_id))



"""
new comments endpoint for movie
"""
@movie_app.route("/movie/<int:movie_id>/comment", methods=["POST", "PATCH", "DELETE", "GET"])
@login_required
def movie_comment(movie_id):

	if request.method == "POST":
		comment = request.form.get("comment")

		new_comment = MoviesComments(
			comment = comment,
			movie_id = movie_id,
			user_id = current_user.id
			)
		new_comment.insert()
		flash("commented successfully")
		return redirect("/movie/"+ str(movie_id))

	elif request.method == "PATCH":
		comment_data = request.form.get("comment")
		comment_id = request.form.get("comment_id")

		comment = MoviesComments.query.filter(MoviesComments.id == comment_id).one_or_none()
		if comment is None:
			flash(f"Comment with id:{comment_id} is missing!")
			return redirect("/movie/"+ str(movie_id))

		comment.comment = comment_data
		comment.is_changed = True
		comment.date = date.today()
		comment.update()

		flash(f"Comment with id:{comment_id} was updated!")
		return redirect("/movie/"+ str(movie_id))

	elif request.args.get("method") == "DELETE":
		comment_id = request.args.get("comment_id")

		comment = MoviesComments.query.filter(MoviesComments.id == comment_id).one_or_none()
		if comment is None:
			flash(f"Comment with id:{comment_id} is missing!")
			return redirect("/movie/"+ str(movie_id))

		comment.delete()

		flash(f"Comment with id:{comment_id} was deleted!")
		return redirect("/movie/"+ str(movie_id))


"""
to delete movies (required login and admin permissions)
"""
@movie_app.route("/movie/<int:movie_id>/delete")
@login_required
def delet_movie_by_id(movie_id):
	movie  = Movies.query.filter(Movies.id == movie_id).one_or_none()

	if movie is None:
		flash(f"movie:{movie_id} is not found in database")

	if current_user.is_admin:
		movie.delete()
		flash(f"movie with id: {movie_id} deleted successfully!")
	else:
		flash(f"User:{current_user.usernmae} does not have permission to delete movies!")

	return redirect("/movies")


"""
to edit movies (required login and admin permissions)
"""
@movie_app.route("/movie/<int:movie_id>/edit", methods=["GET", "POST"])
@login_required
def edit_movies_by_id(movie_id):


	if not current_user.is_admin:
		flash("Admin permissions needed to edit Movies!")
		return redirect("/movie/"+ str(movie_id))


	form = MoviesForm()

	movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
	if movie is None:
		flash(f"movie:{movie_id} is not found in database")
		return redirect("/movie/"+ str(movie_id))


	if form.validate_on_submit():

		movie.title = form.title.data
		movie.description = form.description.data
		movie.image_link = form.image_link.data
		movie.update()
		flash(f"Movie:{movie.title} Updated successfully!")
		return redirect("/movie/"+ str(movie_id))

	try:
		form.title.data = movie.title
		form.description.data = movie.description
		form.image_link.data = movie.image_link
		form.date.data = movie.date
	except Exception as e:
		print(sys.exc_info())
		flash("Error with geting data from database")
		return redirect("/movie/"+ str(movie_id))
	finally:
		return render_template("edit_movie.html", form = form, movie = movie)


"""
search for movies (working with database ilike mthod)
"""
@movie_app.route("/movies/search", methods=["POST","GET"])
def searching_data_movies():
	searchTerm = request.form.get("searchTerm")

	if searchTerm:
		print(searchTerm)
		movies = Movies.query.filter(Movies.title.ilike("%" + searchTerm + "%"))
	else:
		movies = Movies.query.all()
	searchContent = "movie"

	return render_template("search.html", search=searchTerm, datas=movies, searchContent=searchContent)


"""
post new movies endpoint 
"""
@movie_app.route("/movies/create", methods=["GET", "POST"])
def create_movies():

	form = MoviesForm()

	if form.validate_on_submit():
		new_movie = Movies(

			title = form.title.data,
			description = form.description.data,
			date = form.date.data,
			image_link = form.image_link.data

			)
		new_movie.insert()
		flash(f"the movie{form.title.data} successfully added!")
		return redirect("/movies")

	return render_template("new_movie.html", form = form)
