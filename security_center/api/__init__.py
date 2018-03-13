from sanic import Blueprint
from .user_source import UserView
from .user_source.login_source import UserLoginView
from .user_source.activate_source import UserActivateView
from .user_source.change_password_source import UserChangePasswordView


apis = Blueprint('api', url_prefix='/api')
apis.add_route(UserView.as_view(), '/user')
apis.add_route(UserLoginView.as_view(), '/user/login')
apis.add_route(UserActivateView.as_view(), '/user/activate')
apis.add_route(UserChangePasswordView.as_view(), '/change_password')
