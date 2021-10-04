from datetime import date
from database.models import (
    Actors, 
    Movies, 
    db, 
    MoviesComments, 
    MoviesRates,
    Users
    )
from flask import current_app
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash



"""
inserting new user for testing (user will be admin)
"""
user_admin = Users(
    username = "admin",
    email = "admin@mail.ru",
    password = generate_password_hash("password",method="sha256"),
    is_admin = True,
    )

def insert_user_admin():
    user_admin.insert()
    # login_user(user_admin, remember = True)


"""
inserting data in movies for testing
"""
movie1 = Movies(title="King Kong",
description="""King Kong is a fictional monster, resembling an enormous gorilla, 
that has appeared in various media since 1933. He has been dubbed The Eighth Wonder 
of the World, a phrase commonly used within the films. His first appearance was in 
the novelization of the 1933 film King Kong from RKO Pictures, with the film 
premiering a little over two months later. Upon its initial release and subsequent 
re-releases, the film received universal acclaim. A sequel quickly followed that 
same year with The Son of Kong, featuring Little Kong. Toho produced King Kong vs. 
Godzilla (1962) featuring a giant Kong battling Toho's Godzilla and King Kong Escapes 
(1967), a series loosely based on Rankin/Bass' The King Kong Show (1966-1969). In 1976,
 Dino De Laurentiis produced a modern remake of the original film directed by John Guillermin.
  A sequel, King Kong Lives, followed a decade later featuring a Lady Kong. Another remake of 
  the original, this time set in 1933, was released in 2005 from filmmaker Peter Jackson.""",
date=date(2005,7,3))
movie2 = Movies(title="Avengers", description="""Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ab, ipsa, deserunt. Voluptates cupiditate, maiores saepe eveniet eius sequi laboriosam perspiciatis molestias quas praesentium! Id aut doloribus maiores excepturi illo rerum?""", date=date( 1981, 11, 12))
movie3 = Movies(title="Terminator", 
description="""The Terminator is a 1984 science fiction action film directed by James 
Cameron. It stars Arnold Schwarzenegger as the Terminator, a cyborg assassin sent back 
in time from 2029 to 1984 to kill Sarah Connor (Linda Hamilton), whose unborn son will 
one day save mankind from extinction by a hostile artificial intelligence in a 
post-apocalyptic future. Michael Biehn plays Kyle Reese, a soldier sent back in 
time to protect Sarah. The screenplay is credited to Cameron and producer Gale Anne 
Hurd, while co-writer William Wisher Jr. received a credit for additional dialogu""",
date=date(1999, 1, 29))
movie4 = Movies(title="Assassin's Creed", description="Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ab, ipsa, deserunt. Voluptates cupiditate, maiores saepe eveniet eius sequi laboriosam perspiciatis molestias quas praesentium! Id aut doloribus maiores excepturi illo rerum?", date=date(2001, 9, 21))
movie5 = Movies(title="Test Movies5", date=date( 2001, 11, 12))
movie6 = Movies(title="Test Movies6", date=date( 1981, 11, 12))
movie7 = Movies(title="Test Movies7", date=date( 1981, 11, 12))
movie8 = Movies(title="Test Movies8", date=date( 1981, 11, 12))
movie9 = Movies(title="Test Moives9", date=date( 1981, 11, 12))
movie10 = Movies(title="Test Movies10", date=date( 1981, 11, 12))
movie11 = Movies(title="Test Movies11", date=date( 1981, 11, 12))
movie12 = Movies(title="Test Movies12", date=date( 1981, 11, 12))
movie13 = Movies(title="Test Movies13", date=date( 1981, 11, 12))

all_movie = [
    movie1, movie2, movie3,movie4, movie5, movie6, movie7, movie8, movie9, movie10, movie11, movie12, movie13
    ]


def inserting_movie():
    for movie in all_movie:
        movie.insert()


"""
inserting data in actors for testing!
"""
actors1 = Actors(name="Sarah Conor", age="21", gender="famale", actor_slogan="want to be superstar", movie_id = 3)
actors2= Actors(name="Naomi Watts", age="32", gender="famale", actor_slogan="My childs my future", movie_id = 1)
actors3 = Actors(name="Maxi Emerson", age="19", gender="male", actor_slogan="Funny boy looks cool!", movie_id = 2)
actors4 = Actors(name="Arnold Schwarzenegger", age="74", gender="male", actor_slogan="Never stop believing!", movie_id = 3)
actors5 = Actors(name="Chris Evans", age="49", gender="male", actor_slogan="Being capitan, rather than Chris", movie_id = 2)
actors6 = Actors(name="Robert Downey", age="56", gender="male", actor_slogan="Be funny, so you will live beatifull life!", movie_id = 2)
actors7 = Actors(name="Scarlett Johansson", age="32", gender="", actor_slogan="Still doughter of my fahter", movie_id = 2)
actors8 = Actors(name="Linda Hamilton", age="65", gender="famale", actor_slogan="I am still strong!", movie_id = 3)
actors9 = Actors(name="Michael Fassbender", age="44", gender="male", actor_slogan="It's more interesting isn't it, if I've got a hedonistic dark side?", movie_id = 3)
actors10 = Actors(name="Marion Cotillard", age="45", gender="male", actor_slogan="Without darknes sun never be sun we know!", movie_id = 3)

all_actors = [
    actors1, actors2, actors3, actors4,
    actors5, actors6, actors7, actors8, actors9, actors10
]

def insert_actor():
    for actor in all_actors:
        actor.insert()


"""
inserting rates for movies
"""

rate1 = MoviesRates(rate = True, user_id = 1, movie_id = 1)
rate2 = MoviesRates(rate = False, user_id = 1, movie_id = 2)
rate3 = MoviesRates(rate = True, user_id = 1, movie_id = 3)
rate4 = MoviesRates(rate = True, user_id = 1, movie_id = 4)
rate5 = MoviesRates(rate = False, user_id = 1, movie_id = 5)
rate6 = MoviesRates(rate = True, user_id = 1, movie_id = 6)

movies_rates = [ rate1, rate2, rate3, rate4, rate5, rate6]

def insert_movies_rates():
    for rate in movies_rates:
        rate.insert()



"""
inserting comments for testing app!
"""
comment1 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment2 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment3 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment4 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment5 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment6 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment7 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment8 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment9 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)
comment10 = MoviesComments(comment="this is comments for movies!", user_id = 1, movie_id = 1)

movie_comments = [
    comment1,
    comment2,
    comment3,
    comment4,
    comment5,
    comment6,
    comment7,
    comment8,
    comment9,
    comment10
    ]

def insert_movies_comments():
    for comment in movie_comments:
        comment.insert()






"""
helper function to format data form database( i never used them!)
"""
def movie_format(movie):
    return {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "date": movie.date,
        "image_link": movie.image_link
    }

def actor_format(actor):
    return {
        "id": actor.id,
        "name": actor.name,
        "age": actor.age,
        "gender": actor.gender,
        "actor_slogan": actor.actor_slogan,
        "image_link": actor.image_link,
    }

def user_format(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "is_admin": user.is_admin,
        "image_link": user.image_link
    }

# def comments(comment):
#     return {
#     "id": comment.id,
#     "comment": comment.comment,
#     "comment_date": comment.comment_date,
#     "user_id": comment.user_id,
#     "username": (Users.query.filter(User.id == user_id).one_or_none()).username
#     }

def rate_format(obj):
        return {
        "id": obj.id,
        "rate": obj.rate,
        "date": obj.rate_date,
        "user_id": obj.user_id
    }

# def pagination(request, section):
#     page = reqeust.args.get("page", 1, type=int)
#     start = obj_per_page * (page - 1)
#     end = start + obj_per_page
#     return section[start: end]