from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey
    )
from datetime import date
from flask_login import UserMixin


# creating database object 
db = SQLAlchemy()

def setup_db(app):
    db.app = app
    app.config.from_pyfile('config.py')
    db.init_app(app)
    db.drop_all()
    db.create_all()


class CommandHelper():

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
MOVIES table
"""
class Movies(db.Model, CommandHelper):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(String(4000), default="Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ab, ipsa, deserunt. Voluptates cupiditate, maiores saepe eveniet eius sequi laboriosam perspiciatis molestias quas praesentium! Id aut doloribus maiores excepturi illo rerum?")
    date = Column(Date, default=date.today())
    image_link = Column(String(), default="https://www.logolynx.com/images/logolynx/be/bea931a4c99c709e1b3e1f7cb7cc70f0.jpeg")
    actor = db.relationship("Actors", cascade="all,delete",backref="movie", lazy = True)
    rate = db.relationship("MoviesRates",cascade="all, delete", backref="movie", lazy = True)
    comment = db.relationship("MoviesComments",cascade="all, delete", backref="movie", lazy = True)

"""
ACTORS TABLE
"""
class Actors(db.Model, CommandHelper):
    __tablename__="actors"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    actor_slogan = Column(String(255), default="slogan must be here")
    image_link = Column(String(), default="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")
    movie_id = Column(Integer, ForeignKey(Movies.id))




"""
USERS TABLE
"""
class Users(UserMixin, db.Model, CommandHelper):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(55), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_admin = Column(Boolean(), default=True)
    image_link = Column(String(), default="https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")
    comment = db.relationship("MoviesComments",cascade="all, delete", backref="user", lazy = True)
    movie_rate = db.relationship("MoviesRates",cascade="all, delete", backref="user", lazy = True)


"""
COMMENTS TABEL
"""

class MoviesComments(db.Model, CommandHelper):
    __tablename__ = "moviescomments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(255), default="there must be comment")
    comment_date = Column(Date, default=date.today())
    changed = Column(Boolean(), default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"))


"""
Rates table
"""


class MoviesRates(db.Model, CommandHelper):
    __tablename__ = "moviesrates"
    id = Column(Integer, primary_key=True)
    rate_date = Column(Date, default=date.today())
    rate = Column(Boolean())
    changed = Column(Boolean(), default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"))