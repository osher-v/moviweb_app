# sqlite_data_manager.py

import requests
from models import db, User, Movie

class SQLiteDataManager:
    def __init__(self, db):
        self.db = db
        self.tmdb_api_key = 'a67400fe7364c0fcec74bb20d7800f5b'  # Replace with your TMDb API key

    def get_movie_poster(self, movie_name):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={self.tmdb_api_key}&query={movie_name}"
        response = requests.get(url)
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_poster_url
        return None

    def list_all_users(self):
        return User.query.all()

    def find_user_by_id(self, user_id):
        return User.query.get(user_id)

    def list_user_movies(self, user_id):
        user = self.find_user_by_id(user_id)
        if user:
            return user.movies
        return []

    def add_user(self, user):
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, movie):
        movie.poster_url = self.get_movie_poster(movie.name)  # Fetch poster URL before saving
        self.db.session.add(movie)
        self.db.session.commit()

    def find_movie_by_id(self, movie_id):
        return Movie.query.get(movie_id)

    def update_movie(self, movie):
        self.db.session.commit()

    def delete_movie(self, movie_id):
        movie = self.find_movie_by_id(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        return False
