import bcrypt
import copy
import json

from bson import ObjectId
from datetime import datetime

from service import logger
from service.utils.jsonencoder import ComplexEncoder
from storage.mongo import mongodb
from auth.exceptions import UserSaveError


class User(object):
    data = {}

    def __init__(self, email='', password='', active=False, mongo=None):
        now = datetime.utcnow()
        self.data = {
            'active': 'false',
            'email': '',
            'password': '',
            'created': now,
        }

        if email:
            self.email = email
        if password:
            self.password = password

        if mongo:
            self.data = mongo
            self.data['_id'] = ObjectId(mongo['_id'])

    @property
    def json_raw(self):
        """
        generate the raw json
        """
        return json.dumps(self.data, cls=ComplexEncoder)

    @property
    def json(self):
        """
        generate cleaned json
        """
        data = copy.deepcopy(self.data)
        data['id'] = data.pop('_id')
        data.pop('password')
        return json.dumps(data, cls=ComplexEncoder)

    @property
    def id(self):
        return self.data.get('_id', None)

    @property
    def email(self):
        return self.data.get('email', '')

    @email.setter
    def email(self, email):
        self.data['email'] = email

    @property
    def password(self):
        return self.data.get('password', '')

    @password.setter
    def password(self, password):
        from settings import config

        pepper = config.get('pepper', '')
        hashed = bcrypt.hashpw(str(password) + pepper, bcrypt.gensalt())
        self.data['password'] = hashed

    def authenticate(self, password):
        """
        checks to see if the password matches the user's saved password
        """
        from settings import config

        validated = False
        pepper = config.get('pepper', '')
        hashed = bcrypt.hashpw(str(password) + pepper, self.data.get('password', '').encode('utf8'))

        if hashed == self.data.get('password', ''):
            validated = True

        return validated

    def save(self):
        """
        saves the user
        """
        saved = False
        existing_user = User.get_by_email(self.email)

        # check for duplicate emails
        if existing_user and existing_user.id != self.id:
            raise UserSaveError('email already exists')

        if '_id' in self.data.keys():
            # the user needs updating
            ret = mongodb.users.update({'_id': self.data['_id']}, self.data)

            if ret['n']:
                saved = True
        else:
            # new user
            ret = mongodb.users.insert(self.data)

            if ret:
                saved = True

        return saved

    def delete(self):
        deleted = False
        ret = mongodb.users.remove({'_id': self.data['_id']})

        if ret['n']:
            deleted = True

        return deleted

    @classmethod
    def authenticate_user(cls, email, password):
        """
        returns the user if the email and passwords authenticate,
        otherwise returns None
        """
        user = cls.get_by_email(email)

        if user and not user.authenticate(password):
            user = None

        return user

    @classmethod
    def get_by_email(cls, email):
        user = None

        mongo_user = mongodb.users.find_one({'email': email})

        if mongo_user:
            user = User(mongo=mongo_user)

        return user

    @classmethod
    def get_by_id(cls, id):
        user = None
        mongo_user = mongodb.users.find_one({'_id': ObjectId(id)})

        if mongo_user:
            user = User(mongo=mongo_user)
        else:
            logger.debug('did not find user id: {}'.format(id))

        return user

    @classmethod
    def create(cls, email, password, active=False):
        """
        creates, saves, and returns a new user
        """
        # check for dumplicate emails
        if cls.get_by_email(email):
            return None

        user = User(email=email, password=password, active=active)
        user.save()

        return user
