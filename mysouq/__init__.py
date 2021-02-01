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


    @app.route('/init-db')
    def init_db():

        common_password = pbkdf2_sha256.hash('1234')

        user_1 = User(username='admin', password = pbkdf2_sha256.hash('1234') , birthday = "2009-12-30 14:09:01" , email = 'aaa@gmail.com' , role = 2 ).save()

        user_2 = User(username='hamza_96',password = common_password , birthday = "2009-12-30 14:09:01" , email = 'aaa@gmail.com' , role = 0 ).save()
        

        item_1 = Item(title = "First", description = 'First' ,date = "2009-12-30 14:09:01", price = "0" , category = "clothes").save()

        item_2 = Item(title = "Sec" , description = 'First' ,date = "2020-12-30 14:09:01", price = "0" , category = "clothes").save()

        item_3 = Item(title = "Third", description = 'First' ,date = "2011-12-30 14:09:01", price = "0" , category = "clothes").save()
        

        return "Database initialized"


    # register the 'user' blueprint
    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    return app