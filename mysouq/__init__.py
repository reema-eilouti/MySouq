import os

from flask import Flask
from mongoengine import *
from blog.models import *
import json

def create_app(test_config=None):
    # create the Flask
    app = Flask(__name__, instance_relative_config=True)

    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://root:example@localhost:27017/blog?authSource=admin"
    )

    # connect to MongoDB using mongoengine
    connect(
        db='blog',
        username='root',
        password='example',
        authentication_source='admin'
    )

    # define our collections
    # users = mongo.blog.users

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    @app.route('/dummy/init-db')
    def init_db():
        user_1 = User(username='hamza_96',password = '1234', first_name='Hamza', last_name='Rdaideh').save()

        user_2 = User(username='reema_95',password = '1234', first_name='Reema', last_name='Eilouti').save()

        user_3 = User(username='hesham_94',password = '1234', first_name='Hesham', last_name='Marei').save()

        user_4 = User(username='Editor-1',password = '1234', first_name='Editor', last_name='Editor' , role = 1).save()

        user_5 = User(username='Admin',password = '1234', first_name='Admin', last_name='Admin' , role = 2).save()

        reply_1 = Reply(identification = 1, author = user_3 , body = "Hello" , created = "2020-12-30 14:09:01")

        reply_2 = Reply(identification = 2, author = user_2 , body = "Hi" , created = "2020-12-30 14:09:01")

        

        post_1 = Post(author = user_3 ,created = "2009-12-30 14:09:01", title = "POST1", body = "hello" ,
         likes = "0", dislikes = "0" , comments = [reply_1 , reply_2]).save()

        post_2 = Post(author = user_2 ,created = "2021-12-22 10:09:01", title = "POST2", body = "testing" ,
         likes = "0", dislikes = "0" , comments = []).save()

        post_3 = Post(author = user_1 ,created = "2020-1-3 04:09:01", title = "POST3", body = "mongodb is cool" ,
         likes = "1", dislikes = "0" , comments = []).save()
        

        reaction_1 = Reaction(user = user_2 , post = post_3, like = True, dislike = False , favorite = False ).save()


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
