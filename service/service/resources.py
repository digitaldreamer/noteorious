from pyramid.security import Allow, Deny, Everyone, Authenticated, ALL_PERMISSIONS


class RootFactory(object):
    __acl__ = [
        (Allow, 'group:admins', ALL_PERMISSIONS),
        (Deny, Everyone, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


class AuthFactory(object):
    __acl__ = [
        (Allow, Authenticated, ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


class AppFactory(object):
    __acl__ = [
        (Allow, 'group:admins', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request


class UserFactory(object):
    __acl__ = [
        (Allow, 'group:admins', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        user = {'username': key}
        user.__parent__ = self
        user.__name__ = key
        return user
