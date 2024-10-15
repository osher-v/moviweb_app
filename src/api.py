from flask import Blueprint, jsonify, request
from sqlite_data_manager import SQLiteDataManager
from models import Movie, db

api = Blueprint('api', __name__)
data_manager = SQLiteDataManager(db)

@api.route('/users', methods=['GET'])
def get_users():
    users = data_manager.list_all_users()
    users_data = [{'user_id': user.user_id, 'username': user.username} for user in users]
    return jsonify(users_data)

@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = data_manager.find_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    movies = [{'movie_id': movie.movie_id, 'name': movie.name, 'year': movie.year, 'rating': movie.rating}
              for movie in user.movies]
    return jsonify(movies)

@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    user = data_manager.find_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    name = data.get('name')
    year = data.get('year')
    rating = data.get('rating')

    if not all([name, year, rating]):
        return jsonify({'error': 'Missing data'}), 400

    new_movie = Movie(name=name, year=year, rating=rating, user_id=user_id)
    data_manager.add_movie(new_movie)

    return jsonify({'message': 'Movie added successfully'}), 201
