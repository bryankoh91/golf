from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

#Defining the method to create and initialise Flask app
def create_app():
    app = Flask(__name__)
    app.static_folder = "assets"
    app.config["SECRET_KEY"] = "9OLWxND4o83j4K4iuopO"
    
    app.config["MONGODB_SETTINGS"] = {
    'db':'my_golf',
    'host':'localhost'
    }
    db = MongoEngine(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "please log in to access this page"

    return app, db , login_manager

#Calling the create_app method
app, db , login_manager = create_app()