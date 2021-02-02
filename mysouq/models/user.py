from mongoengine import *
from passlib.hash import pbkdf2_sha256

class User(Document):

    meta = {'collection': 'Users'}

    username = StringField(required = True)
    birthday = DateTimeField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    role = IntField(default = 0)
    disable = BooleanField(default = False) 
    maintenance = BooleanField(default = False)
    favorites_list = ListField(StringField())
    


    def authenticate(self, username, password):
        if username == self.username and pbkdf2_sha256.verify(password, self.password):
            return True
        else:
            return False


    def encrypt_password(self, password):
        return pbkdf2_sha256.hash(password)


    def change_password(self, current_password, new_password):
        if pbkdf2_sha256.verify(current_password, self.password):
            self.password = self.encrypt_password(new_password)

    
    def serialize(self):
        serialized = {
            "id": str(self.pk),
            'username': self.username,
            'email': self.email,
            'birthday': self.birthday,
            'role': self.role,
            'disable': self.disable,
            'maintenance': self.maintenance,
            'favorites': self.favorites_list            
        }
        return serialized