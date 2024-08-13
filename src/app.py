from flask import Flask

app = Flask(__name__)

from flask import Flask, jsonify
from data_managers.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('C:/Users/osher/PycharmProjects/moviweb_app/src/data/movieweb_data.json')


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)


@app.route('/user/<int:user_id>/movies')
def list_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return jsonify(movies)


@app.route('/user/<int:user_id>/add_movie')
def add_movie_to_user(user_id):
    movie_data = {
        "name": "Interstellar",
        "director": "Christopher Nolan",
        "year": 2014,
        "rating": 8.6
    }
    success = data_manager.add_movie_to_user(user_id, 3, movie_data)
    return jsonify({"success": success})


if __name__ == '__main__':
    app.run(debug=True)
