import os
import sys

from pyramid.config import Configurator
from pyramid.events import subscriber, BeforeRender
from pyramid.httpexceptions import HTTPNotFound

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.sep.join(PROJECT_PATH.split(os.sep)[:-1])

# include paths
sys.path.insert(0, PROJECT_PATH)
sys.path.insert(0, os.path.join(PROJECT_PATH, 'apps'))

# logging
import logging
logger = logging.getLogger(__name__)

def notfound(request):
    return HTTPNotFound('Page not found.')

@subscriber(BeforeRender)
def add_global(event):
    """
    add template context procesors
    """
    event['STATIC_URL'] = event['request'].registry.settings.get('static_url', '/static/')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(
        settings=settings,
        # session_factory=session_factory,
        # root_factory='resources.RootFactory',
        # authentication_policy=authn_policy,
        # authorization_policy=authz_policy,
    )
    config.include('pyramid_jinja2')
    config.include('cornice')

    config.add_static_view('static', 'static', cache_max_age=3600)

    # templates
    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')
    config.add_renderer('.jinja2', 'pyramid_jinja2.renderer_factory')
    config.add_jinja2_search_path('templates')

    config.add_notfound_view(notfound, append_slash=True)
    config.include('main')
    config.include('auth')

    return config.make_wsgi_app()
