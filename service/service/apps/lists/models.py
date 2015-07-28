import copy
import json

from bson import ObjectId
from datetime import datetime

from main.models import MongoObject
from service import logger
from service.utils.jsonencoder import ComplexEncoder
from storage.mongo import mongodb


class List(MongoObject):
    collection = 'lists'

    def __init__(self, user_id=None, name='', order=-1, mongo=None):
        super(List, self).__init__(mongo=mongo)

        if not mongo:
            self.data = {
                'order': 0,
                'user_id': '',
                'name': '',
            }

        if order >= 0:
            self.order = order
        if name:
            self.name = name
        if user_id:
            self.data['user_id'] = ObjectId(user_id)

    @property
    def user(self):
        user = User.get_by_id(self.data.get('user_id'))
        return user

    @property
    def name(self):
        return self.data.get('name', '')

    @name.setter
    def name(self, name):
        self.data['name'] = name

    @property
    def order(self):
        return self.data.get('order')

    @order.setter
    def order(self, order):
        self.data['order'] = order

    def fromJSON(self, data):
        """
        unpackages a json object
        """
        data = super(List, self).fromJSON(data)
        data['user_id'] = ObjectId(mongo['user_id'])
        return data

    @classmethod
    def create(cls, user_id, name):
        """
        creates, saves, and returns a new list
        """
        list = List(user_id=user_id, name=name)
        list.save()

        return list


class Task(object):
    data = {}

    def __init__(self, list_id=None, title='', mongo=None):
        now = datetime.utcnow()
        self.data = {
            'list_id': '',
            'title': '',
            'created': now,
            'modified': now,
        }

        if title:
            self.title = title
        if list_id:
            self.list_id = ObjectId(list_id)

        if mongo:
            self.data = mongo
            self.data['_id'] = ObjectId(mongo['_id'])
            self.data['list_id'] = ObjectId(mongo['list_id'])

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
        return json.dumps(data, cls=ComplexEncoder)

    @property
    def id(self):
        return self.data.get('_id', None)

    @property
    def user(self):
        user = User.get_by_id(self.data.get('user_id'))
        return user

    @property
    def name(self):
        return self.data.get('name', '')

    @name.setter
    def name(self, name):
        self.data['name'] = name

    @property
    def modified(self):
        return self.data.get('modified', '')

    @modified.setter
    def modified(self, timestamp):
        self.data['modified'] = modified

    def save(self):
        """
        saves the list
        """
        saved = False
        now = datetime.utcnow()
        self.modified = now

        if '_id' in self.data.keys():
            # the list needs updating
            ret = mongodb.lists.update({'_id': self.data['_id']}, self.data)

            if ret['n']:
                saved = True
        else:
            # new list
            ret = mongodb.lists.insert(self.data)

            if ret:
                saved = True

        return saved

    def delete(self):
        deleted = False
        ret = mongodb.lists.remove({'_id': self.data['_id']})

        if ret['n']:
            deleted = True

        return deleted

    @classmethod
    def get_by_id(cls, id):
        list = None
        mongo_list = mongodb.lsits.find_one({'_id': ObjectId(id)})

        if mongo_list:
            list = List(mongo=mongo_user)
        else:
            logger.debug('did not find lsit id: {}'.format(id))

        return list

    @classmethod
    def create(cls, user_id, name):
        """
        creates, saves, and returns a new list
        """
        list = List(user_id=user_id, name=name)
        list.save()

        return list
