import string
import random
import requests
from config import (
    number_of_users,
    max_posts_per_user,
    max_like_per_user
)

url = 'http://127.0.0.1:8000/api/'
email_domain = 'gmail.com'

class GenerateUserData:
    """
    Generating user data for bot application.
    """

    def generate_chars(self, start, stop):
        random_chars = ''.join(random.sample(string.ascii_letters,
                                random.randint(start, stop)))
        return random_chars

    def generate_email(self):
        user_email = '%s@%s' % (self.generate_chars(4, 12), email_domain)
        return user_email

    def generate_username(self):
        username = self.generate_chars(4, 10)
        return username

    def _generate_password(self):
        password = self.generate_chars(8, 10)
        return password

    def generate_post_text(self):
        text = ''.join([random.choice(string.printable) for _ in range(500)])
        return text


class Bot:
    """
    Automated bot for user registration, post creation and post liked.
    """

    def __init__(self, number_of_users, max_posts_per_user, max_like_per_user):
        self.users_count = number_of_users
        self.max_posts = max_posts_per_user
        self.max_likes = max_like_per_user

    def user_signup(self):
        url_method = url + 'user/signup/'
        _password = GenerateUserData()._generate_password()
        data = {
            'email': GenerateUserData().generate_email(),
            'username': GenerateUserData().generate_username(),
            'password': _password
        }
        resp = requests.post(url=url_method, data=data)
        return resp.json().get('username'), _password


    def user_login(self, username, _password):
        url_method = url + 'user/login/'
        data = {
            'username': username,
            'password': _password
        }
        resp = requests.post(url=url_method, data=data)
        _token = resp.json().get('token')
        return _token

    def create_post(self, _token):
        url_method = url + 'post/create/'
        data = {'text': GenerateUserData().generate_post_text()}
        headers = {'Authorization': 'Token %s' % _token}
        resp = requests.post(url=url_method, data=data, headers=headers)
        post_id = resp.json().get('id')
        return post_id

    def liked_post(self, _token, post_id):
        url_method = url + 'post/%d/like' % post_id
        headers = {'Authorization': 'Token %s' % _token}
        resp = requests.get(url=url_method, headers=headers)

    def start_bot(self):

        for _ in range(self.users_count):
            username, _password = self.user_signup()
            _token = self.user_login(username, _password)
            count_of_posts = random.randint(1, self.max_posts)
            count_of_likes = random.randint(1, self.max_likes)
            all_posts = []
            while count_of_posts != 0:
                post_id = self.create_post(_token)
                all_posts.append(post_id)
                count_of_posts -= 1
            while count_of_likes != 0:
                random_post = random.choice(all_posts)
                self.liked_post(_token, random_post)
                count_of_likes -= 1


if __name__ == "__main__":
    Bot(number_of_users, max_posts_per_user, max_like_per_user).start_bot()
