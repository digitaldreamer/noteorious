import json

from cornice import Service
from pyramid.exceptions import Forbidden
from pyramid.view import view_config

from auth.models import User
from auth.schemas import AuthSchema, UserSchema


auth = Service(name='authenticate', path='/authenticate', description='Authentication')
user = Service(name='user', path='/users/{user_id}', description='User')


class AuthViews(object):
    @auth.get()
    def auth_get(request):
        """
        a simple endpoint to run tests through
        """
        request.response.body = json.dumps({'hello': 'world'})
        request.response.content_type = 'application/json'
        return request.response

    @auth.post(schema=AuthSchema)
    def auth_post(request):
        """
        an endpoint to authenticate users
        returns a user if passes, otherwise sends 401 auth error

        email: the user's email
        password: the user's password
        """
        email = request.validated['email']
        password = request.validated['password']

        user = User.authenticate_user(email, password)
        response_body = {}

        if user:
            response_body = user.json
        else:
            request.response.status_int = 401
            response_body = json.dumps({
                'status': 'error',
                'message': 'user failed to authenticate',
            })

        request.response.body = response_body
        request.response.content_type = 'application/json'
        return request.response

