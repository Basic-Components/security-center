"""
"""
from .core import Core
from .hash_password_mixin import HashPasswordMixin
from .create_mixin import CreateMixin
from .get_user_mixin import GetUserMixin
from .social_account_mixin import SocialAccountMixin
from .status_mixin import StatusMixin
from .role_mixin import RoleMixin
from .real_name_auth_mixin import RealNameAuthMixin
from .thirdpart_auth_mixin import ThirdPartAuthMixin
from .login_info_mixin import LoginInfoMixin
from .img_mixin import ImgMixin

class User(
        Core,
        HashPasswordMixin,
        CreateMixin,
        GetUserMixin,
        SocialAccountMixin,
        StatusMixin,
        RoleMixin,
        RealNameAuthMixin,
        ThirdPartAuthMixin,
        LoginInfoMixin,
        ImgMixin):
    pass
