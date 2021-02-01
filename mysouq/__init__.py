print(f'Invoking __init__.py for {__name__}')

import os

from flask import Flask
from mongoengine import *
from mysouq.models import *
import json

def create_app(test_config=None):
    # create the Flask
    app = Flask(__name__, instance_relative_config=True)

    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://root:example@localhost:27017/mysouq?authSource=admin"
    )

    # connect to MongoDB using mongoengine
    connect(
        db='mysouq',
        username='root',
        password='example',
        authentication_source='admin'
    )

    # define our collections
    # users = mongo.mysouq.users

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    @app.route('init-db')
    def init_db():

        user_2 = User(username='reema_95',password = '1234', first_name='Reema', last_name='Eilouti').save()

        return "Database initialized"


    # register the 'post' blueprint
    from .blueprints.post import post_bp
    app.register_blueprint(post_bp)

    # register the 'user' blueprint
    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    # register the 'login' blueprint
    from .blueprints.login import login_bp
    app.register_blueprint(login_bp)

    return app