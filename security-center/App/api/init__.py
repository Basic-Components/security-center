from sanic import Blueprint
from .source import sample_source

api = Blueprint('api',url_prefix="/api")




api.add_route(sample_source.as_view(), 'path/<_id>')

