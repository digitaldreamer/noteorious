from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/base.html')
def home(request):
    return {'project': 'service'}
