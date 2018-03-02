"""
"""
from .core import Core
from .hash_password_mixin import HashPasswordMixin
from .create_mixin import CreateMixin
from .get_user_mixin import GetUserMixin


class User(
    Core,
    HashPasswordMixin,
    CreateMixin,
    GetUserMixin):
    pass
