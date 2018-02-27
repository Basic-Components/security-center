from sanic import Blueprint

api = Blueprint('api',url_prefix="/api")

from .source import sample_source


api.add_route(sample_source.as_view(), 'path/<_id>')

