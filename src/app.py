from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Movie
from sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = SQLiteDataManager(db)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.find_user_by_id(user_id)
    if user is None:
        return f"User with ID {user_id} not found", 404
    movies = data_manager.list_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        new_user = User(username=username)
        data_manager.add_user(new_user)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.find_user_by_id(user_id)
    if user is None:
        return f"User with ID {user_id} not found", 404

    if request.method == 'POST':
        movie_name = request.form['name']
        year = request.form['year']
        rating = request.form['rating']
        new_movie = Movie(name=movie_name, year=year, rating=rating, user_id=user_id)
        data_manager.add_movie(new_movie)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user, user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = data_manager.find_user_by_id(user_id)
    if user is None:
        return f"User with ID {user_id} not found", 404

    movie = data_manager.find_movie_by_id(movie_id)
    if movie is None:
        return f"Movie with ID {movie_id} not found", 404

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.year = request.form['year']
        movie.rating = request.form['rating']
        data_manager.update_movie(movie)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie, user_id=user_id)



@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    user = data_manager.find_user_by_id(user_id)
    if user is None:
        return f"User with ID {user_id} not found", 404

    success = data_manager.delete_movie(movie_id)
    if not success:
        return f"Failed to delete movie with ID {movie_id}", 400

    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
