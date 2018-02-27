
from sanic import Sanic
from sanic import response
from sanic.response import json
from App.api import api
from App.view import view

__VERSION__ = '0.0.5'
app =  app = Sanic("auth-center")

default_settings = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'WORKERS': 1,
    'ACCESS_LOG': True,
    'CAPTCHA_FONT_PATH': str(font_path),
    'LOGO_PATH': None,
    "SSL":None
}
app.config.update(default_settings)

app.blueprint(api, url_prefix='/api')


