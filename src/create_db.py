# create_sample_data.py

from flask import Flask
from models import db, User, Movie
from sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = SQLiteDataManager(db)


def create_sample_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        users_data = [
            {"username": "SciFiFan", "movies": [
                {"name": "Interstellar", "year": 2014, "rating": 8.6},
                {"name": "Blade Runner 2049", "year": 2017, "rating": 8.0},
                {"name": "The Matrix", "year": 1999, "rating": 8.7},
                {"name": "Inception", "year": 2010, "rating": 8.8},
                {"name": "Dune", "year": 2021, "rating": 8.1}
            ]},
            {"username": "FantasyLover", "movies": [
                {"name": "The Lord of the Rings: The Fellowship of the Ring", "year": 2001, "rating": 8.8},
                {"name": "Harry Potter and the Sorcerer's Stone", "year": 2001, "rating": 7.6},
                {"name": "The Hobbit: An Unexpected Journey", "year": 2012, "rating": 7.8},
                {"name": "Pan's Labyrinth", "year": 2006, "rating": 8.2},
                {"name": "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe", "year": 2005, "rating": 6.9}
            ]},
            {"username": "RomanticGirl", "movies": [
                {"name": "The Notebook", "year": 2004, "rating": 7.8},
                {"name": "Pride and Prejudice", "year": 2005, "rating": 7.8},
                {"name": "Titanic", "year": 1997, "rating": 7.8},
                {"name": "La La Land", "year": 2016, "rating": 8.0},
                {"name": "A Walk to Remember", "year": 2002, "rating": 7.4}
            ]},
            {"username": "ActionMan", "movies": [
                {"name": "Mad Max: Fury Road", "year": 2015, "rating": 8.1},
                {"name": "Die Hard", "year": 1988, "rating": 8.2},
                {"name": "John Wick", "year": 2014, "rating": 7.4},
                {"name": "The Dark Knight", "year": 2008, "rating": 9.0},
                {"name": "Gladiator", "year": 2000, "rating": 8.5}
            ]},
            {"username": "ComedyKing", "movies": [
                {"name": "Superbad", "year": 2007, "rating": 7.6},
                {"name": "The Hangover", "year": 2009, "rating": 7.7},
                {"name": "Anchorman: The Legend of Ron Burgundy", "year": 2004, "rating": 7.2},
                {"name": "Dumb and Dumber", "year": 1994, "rating": 7.3},
                {"name": "Step Brothers", "year": 2008, "rating": 6.9}
            ]}
        ]

        for user_data in users_data:
            user = User(username=user_data["username"])
            data_manager.add_user(user)
            for movie_data in user_data["movies"]:
                movie = Movie(name=movie_data["name"], year=movie_data["year"], rating=movie_data["rating"],
                              user_id=user.user_id)
                data_manager.add_movie(movie)
        print("Sample data created!")


if __name__ == '__main__':
    create_sample_data()
