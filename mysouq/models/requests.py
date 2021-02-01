from mongoengine import *
from .item import Item
from .user import User


class BuyRequest(Document):

    meta = {'collection' : 'Buy Requests'}
   
    user = ReferenceField(User)
    item = ReferenceField(Item)
    status = StringField(required = True)


class UpgradeRequest(Document):

    meta = {'collection' : 'Upgrade Requests'}    
  
    user = ReferenceField(User)
    status = StringField(required = True)        