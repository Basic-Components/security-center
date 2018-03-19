from sanic import Blueprint
from .user_source import UserView
from .user_source.login_source import UserLoginView
from .user_source.profile_source import UserProfileView

apis = Blueprint('api', url_prefix='/api')
apis.add_route(UserView.as_view(), '/user')
apis.add_route(UserLoginView.as_view(), '/user/login')
apis.add_route(UserProfileView.as_view(), '/user/profile')
