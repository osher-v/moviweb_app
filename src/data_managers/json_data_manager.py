import json
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        """Load data from the JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"users": {}}

    def save_data(self):
        """Save the current state of data back to the JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_all_users(self):
        """Return all the users as a dictionary."""
        return self.data['users']

    def get_user_movies(self, user_id):
        """Return all the movies for a given user."""
        user = self.data['users'].get(str(user_id))
        if user:
            return user.get('movies', {})
        return None

    def add_movie_to_user(self, user_id, movie_id, movie_data):
        """Add a new movie to a user's list."""
        user = self.data['users'].get(str(user_id))
        if user:
            user['movies'][str(movie_id)] = movie_data
            self.save_data()
            return True
        return False

    def update_movie_for_user(self, user_id, movie_id, movie_data):
        """Update the details of an existing movie."""
        user = self.data['users'].get(str(user_id))
        if user and str(movie_id) in user['movies']:
            user['movies'][str(movie_id)] = movie_data
            self.save_data()
            return True
        return False

    def delete_movie_for_user(self, user_id, movie_id):
        """Delete a movie from a user's list."""
        user = self.data['users'].get(str(user_id))
        if user and str(movie_id) in user['movies']:
            del user['movies'][str(movie_id)]
            self.save_data()
            return True
        return False

    def find_user_by_id(self, user_id):
        """Find and return a user by their ID."""
        return self.data['users'].get(str(user_id), None)
