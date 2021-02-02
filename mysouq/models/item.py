from mongoengine import *
from datetime import datetime
from .user import User

class Item(Document):

    meta = {'collection' : 'Items',
             'indexes': [
                {'fields': ['$title', '$description'],
                 'default_language': 'english',
                 'weights': {'title': 2, 'description': 1}
                 }
            ]}

    user = ReferenceField(User)
    title = StringField(required = True)
    description = StringField(required = True)
    date = DateTimeField(default = datetime.now())
    price = FloatField(required = True)
    sold = BooleanField(default = False)
    category = StringField(required = True)
    hidden = BooleanField(default = False)
    buy_requests_list = ListField(StringField())


class Category(Document):

    meta = {'collection' : 'Categories'}

    value = StringField(required = True)
    label = StringField(required = True)