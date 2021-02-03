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

        user_1 = User(username='admin', password = pbkdf2_sha256.hash('1234'), birthday = "1990-01-01 14:09:01", email = 'admin@gmail.com', role = 2 ).save()

        user_2 = User(username='reema_95', password = pbkdf2_sha256.hash('1234'), birthday = "1995-10-06 14:09:01", email = 'reema@gmail.com', role = 0 ).save()

        user_3 = User(username='salma_93', password = pbkdf2_sha256.hash('1234'), birthday = "1993-07-23 14:09:01", email = 'salma@gmail.com', role = 1 ).save()
        

        item_1 = Item(user = user_3, title = "Scarf", description = 'New, Handmade Knitted Scarf, Blue and Black, Size: Medium', date = "2021-01-15 14:09:01", price = "5" , category = "Clothes").save()

        item_2 = Item(user = user_3, title = "iPhone XR" , description = 'Used, In Good Condition', date = "2021-01-30 03:40:26", price = "700" , category = "Digital Devices").save()

        item_3 = Item(user = user_3, title = "Toyota Prius 2010", description = 'Used, White, 165000KM, 1800CC, Hybrid', date = "2021-02-04 18:22:06", price = "9500" , category = "Vehicles").save()
        


        category_1 = Category(value = '1', label = 'Clothes').save()

        category_2 = Category(value = '2', label = 'Vehicles').save()
        
        category_3 = Category(value = '3', label = 'Digital Devices').save()



        return "Database Initialized Successfully."


    # register the 'user' blueprint
    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    # register the 'item' blueprint
    from .blueprints.item import item_bp
    app.register_blueprint(item_bp)

    return app