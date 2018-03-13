from pathlib import Path
from sanic import Sanic
from sanic import response
from sanic.response import json
from sanic_session import InMemorySessionInterface
#from sanic_mail import Sanic_Mail
from jinja2 import FileSystemLoader
from .api import apis
from .view import views
from .init_jinja import jinja
from .model import db, User


__VERSION__ = '0.0.5'
app = Sanic("pmfptest")
default_settings = {
    'DEBUG': True,
    "TEST":False,
    'SECRET':"cant guess",
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'WORKERS': 1,
    'ACCESS_LOG': True,
    'LOGO_PATH': None,
    "SSL": None,
    "TEST_DB_URL": "postgresql://huangsizhe:@127.0.0.1:5432/test_sql",
    "DB_URL": "postgresql://huangsizhe:@127.0.0.1:5432/test_ext",
    #"TEST_DB_URL": "postgresql://postgres:rstrst@127.0.0.1:5432/test",
    #"DB_URL": "postgresql://postgres:rstrst@127.0.0.1:5432/test",
    # "TEST_DB_URL": "postgresql://postgres:hsz881224@127.0.0.1:5432/test",
    # "DB_URL": "postgresql://postgres:hsz881224@127.0.0.1:5432/test",
    "TEMPLATE_PATH": str(Path("./templates").absolute()),
    "STATIC_FOLDER": str(Path("./static").absolute()),
    'MAIL_SENDER': "csd@hszofficial.site",
    'MAIL_SENDER_PASSWORD': "Hszsword881224",
    'MAIL_SEND_HOST': "smtp.exmail.qq.com",
    'MAIL_SEND_PORT': 465,
    'MAIL_TLS': True}
app.config.update(default_settings)
loader = FileSystemLoader(app.config.TEMPLATE_PATH)
jinja.init_app(app, loader=loader)
#sender = Sanic_Mail(app)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)
app.blueprint(views)
app.blueprint(apis)


@app.listener('before_server_start')
async def setup_db(app, loop):
    await db.connect(loop)
    await User.create_table(fail_silently=True)


@app.listener('after_server_stop')
async def close_db(app, loop):
    # if app.config.TEST:
    #     await db.drop_tables([User], safe=True)
    #     print("[drop table]")
    await db.close()


@app.middleware('request')
async def add_session_to_request(request):
    await session.open(request)


@app.middleware('response')
async def save_session(request, response):
    await session.save(request, response)
