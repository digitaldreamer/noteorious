import os
import unittest

from pyramid import testing
from auth.models import User


class UserTests(unittest.TestCase):
    def setUp(self):
        from service import main
        from paste.deploy import appconfig
        from webtest import TestApp

        # set settings
        os.environ['PYRAMID_SETTINGS'] = 'development.ini#main'
        self.config = testing.setUp()
        self.reset()

    def tearDown(self):
        self.reset()
        testing.tearDown()

    def test_user_management(self):
        """
        test user creation and deletion
        """
        # creation
        user = User.create('world@example.com', 'world')
        self.assertTrue(user)

        user2 = User.get_by_id(user.id)
        self.assertTrue(user2)

        user3 = User.get_by_email(user.email)
        self.assertTrue(user3)

        # deletion
        self.assertTrue(user.delete())
        user4 = User.get_by_email('world@example.com')
        self.assertFalse(user4)

    def test_user(self):
        user = self.create_user()
        self.email(user)
        self.password(user)
        self.assertTrue(user.delete())

    def create_user(self):
        # check user
        user = User.create('hello@example.com', 'hello')
        self.assertTrue(user)
        return user

    def email(self, user):
        """
        check updating and email retrieval
        """
        self.assertEqual(user.email, 'hello@example.com')
        self.assertTrue(User.get_by_email(user.email))

        # change email
        user.email = 'hello2@example.com'
        user.save()

        self.assertEqual(user.email, 'hello2@example.com')
        self.assertTrue(User.get_by_email(user.email))
        self.assertFalse(User.get_by_email('hello@example.com'))

        # reset email
        user.email = 'hello@example.com'
        user.save()

    def password(self, user):
        # password
        self.assertTrue(user.authenticate('hello'))
        user.password = 'world'
        user.save()

        # check updating password
        user2 = User.get_by_id(user.id)
        self.assertFalse(user2.authenticate('hello'))
        self.assertTrue(user2.authenticate('world'))

        # reset password
        user.password = 'hello'
        user.save()

    def reset(self):
        """
        clean up any remaining test users
        """
        emails = ['hello@example.com', 'hello2@example.com', 'world@example.com']

        for email in emails:
            user = User.get_by_email(email)

            if user:
                user.delete()
