"""
"""
from .core import Core
from .hash_password_mixin import HashPasswordMixin
from .create_mixin import CreateMixin
from .current_mixin import CurrentMixin


class User(
    Core,
    HashPasswordMixin,
    CreateMixin,
    CurrentMixin):
    pass
