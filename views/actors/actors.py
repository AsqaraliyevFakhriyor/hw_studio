
import sys
from flask import Blueprint, request, render_template, url_for, flash, redirect
from database.models import Actors, Users
from flask_login import current_user, login_required
from datetime import date
from forms import ActorsForm


actor_app = Blueprint("actors", __name__) 


"""
actors route which returns all actors with pagination 
"""
@actor_app.route("/actors")
def get_actors(page=1):

	per_page = 8

	if request.args:
		page = int(request.args.get("page"))

	actors = Actors.query.paginate(page, per_page, error_out=False)
	return render_template("home.html", actors=actors, user = current_user, current_day = date.today())



"""
actors route which returns actor by id 
"""
@actor_app.route("/actor/<int:actor_id>")
def get_actor_by_id(actor_id):

	if not actor_id:
		flash("Actor id is missing! Ty agian!")
		redirect("/actors")

	actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

	if actor is None:
		flash(f"Actor in id: {actor_id} is not found!")

	return render_template("actorbyid.html", actor=actor, current_user=current_user)	


"""
edit route for actors
"""
@actor_app.route("/actor/<int:actor_id>/edit", methods=["POST", "GET"])
@login_required
def edit_actor_by_id(actor_id):

	if not current_user.is_admin:
		flash("Admin role needed!")
		return reidrect(f"/actor/{actor_id}")

	form =  ActorsForm()

	actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
	if actor is None:
		flash(f"Actor for id: {actor_id} not found!")
		return redirect(f"/actor/{ actor_id }")

	if form.validate_on_submit():
		actor.name = form.name.data
		actor.age = form.age.data
		actor.gender = form.gender.data
		actor.actor_slogan = form.actor_slogan.data
		actor.image_link = form.image_link.data
		actor.update()
		flash(f"Actor '{ actor.name }' updated successfully")
		return redirect(f"/actor/{ actor.id }")

	try:
		form.name.data = actor.name
		form.age.data = actor.age
		form.gender.data = actor.gender
		form.actor_slogan.data = actor.actor_slogan
		form.image_link.data = actor.image_link
	except Exception as e:
		print(sys.exc_info())
		flash("error occured, try again!")


	return render_template("edit_actor.html", form = form, actor = actor)


@actor_app.route("/actor/<int:actor_id>/delete", methods=["DELETE", "GET"])
@login_required
def delet_actor_by_id(actor_id):

	if not current_user.is_admin:
		flash("To complate action, admin role required!")

	actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
	if actor is None:
		flash(f"Actor for id: {actor_id} is missing!")
		return redirect("/actors")

	actor.delete()
	flash(f"Actor {actor_id} deleted successfully!")
	return redirect("/actors")


@actor_app.route("/actor/create", methods=["POST", "GET"])
@login_required
def create_actor():

	form = ActorsForm()

	if form.validate_on_submit():

		try:
			new_actor = Actors(
				name = form.name.data,
				age = form.age.data,
				gender = form.gender.data,
				actor_slogan = form.actor_slogan.data,
				image_link = form.image_link.data
				)
			new_actor.insert()
			flash(f"Actor '{form.name.data}' added successfully!")
			return redirect("/actors")
		except Exception as e:
			flash(f"{e}")
			return redirect("/actors")

	return render_template("new_actor.html", form = form)
