from flask_login import UserMixin, LoginManager
from passlib.apps import custom_app_context as pwd_context

login_manager = LoginManager()


class User(UserMixin):
    def __init__(self,name,surname,email, username, password):
        self.name=name
        self.surname=surname
        self.username = username
        self.password = password
        self.email = email
        self.is_admin = False
        self.authenticated = True

    def get_id(self):
        return self.username
    
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

def hashing(password):
    secret_key = 'helloworld'
    return pwd_context.encrypt(password)