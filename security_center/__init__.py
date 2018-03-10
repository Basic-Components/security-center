from pathlib import Path
from sanic import Sanic
from sanic import response
from sanic.response import json
from sanic_session import InMemorySessionInterface
from jinja2 import FileSystemLoader
from .api import apis
from .view import views, jinja
from .model import db, User


__VERSION__ = '0.0.5'
app = Sanic("pmfptest")
default_settings = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'WORKERS': 1,
    'ACCESS_LOG': True,
    'LOGO_PATH': None,
    "SSL": None,
    "TEST_DB_URL": "postgresql://huangsizhe:@127.0.0.1:5432/test_sql",
    "DB_URL": "postgresql://huangsizhe:@127.0.0.1:5432/test_ext",
    "TEMPLATE_PATH": str(Path("./templates").absolute()),
    "STATIC_FOLDER": str(Path("./static").absolute())
}
app.config.update(default_settings)
loader = FileSystemLoader(app.config.TEMPLATE_PATH)
jinja.init_app(app, loader=loader)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)
app.blueprint(views)
app.blueprint(apis)


@app.listener('before_server_start')
async def setup_db(app, loop):
    await db.connect(loop)
    await User.create_table(fail_silently=True)


@app.listener('after_server_stop')
async def close_db(app, loop):
    await db.close()


@app.middleware('request')
async def add_session_to_request(request):
    await session.open(request)


@app.middleware('response')
async def save_session(request, response):
    await session.save(request, response)