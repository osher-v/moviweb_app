from flask import Flask, render_template, request, redirect, url_for
from src.data_managers.json_data_manager import JSONDataManager

app = Flask(__name__)

data_manager = JSONDataManager('C:/Users/osher/PycharmProjects/moviweb_app/src/data/movieweb_data.json')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.find_user_by_id(user_id)
    if user is None:
        return f"User with ID {user_id} not found", 404
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        new_user_id = len(data_manager.get_all_users()) + 1
        data_manager.data['users'][str(new_user_id)] = {
            "name": name,
            "movies": {}
        }
        data_manager.save_data()
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
        new_movie_id = len(user['movies']) + 1
        data_manager.add_movie_to_user(user_id, new_movie_id, {
            "name": movie_name,
            "year": year,
            "rating": rating
        })
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user, user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = data_manager.find_user_by_id(user_id)
    if user is None:
        return f"User with ID {user_id} not found", 404

    movie = user['movies'].get(str(movie_id))
    if movie is None:
        return f"Movie with ID {movie_id} not found", 404

    if request.method == 'POST':
        # קבלת נתונים מהטופס
        movie_name = request.form['name']
        year = request.form['year']
        rating = request.form['rating']
        # עדכון הסרט
        data_manager.update_movie_for_user(user_id, movie_id, {
            "name": movie_name,
            "year": year,
            "rating": rating
        })
        return redirect(url_for('user_movies', user_id=user_id))

    # הוספת movie_id למשתנים המועברים לתבנית
    return render_template('update_movie.html', user=user, user_id=user_id, movie=movie, movie_id=movie_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    user = data_manager.find_user_by_id(user_id)
    if user is None:
        return f"User with ID {user_id} not found", 404

    success = data_manager.delete_movie_for_user(user_id, movie_id)
    if not success:
        return f"Failed to delete movie with ID {movie_id}", 400

    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
