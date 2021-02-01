from mongoengine import *
from datetime import datetime

class Item(Document):

    meta = {'collection' : 'Items'}

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