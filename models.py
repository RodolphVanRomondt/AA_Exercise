from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """ Connect to DataBase. """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ Model for User. """

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        usernameInput = cls.query.filter(cls.username == username).first()
        if usernameInput:
            return "Username"
        
        emailInput = cls.query.filter(cls.email == email).first()
        if emailInput:
            return "Email"

        hashed = bcrypt.generate_password_hash(password)
        hashed = hashed.decode("utf8")

        return cls(username=username, password=hashed, email=email,
                   first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter(cls.username == username).first()
        password = bcrypt.check_password_hash(user.password, password)

        if user and password:
            return True
        else:
            return False
    
class Feedback(db.Model):
    """ Model for feedback. """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"))

    user = db.relationship("User", backref="feedback")