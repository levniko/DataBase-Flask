from flask_login import UserMixin, LoginManager
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



