"""修改密码接口."""

from sanic.views import HTTPMethodView
from sanic.response import json


class UserChangePasswordView(HTTPMethodView):
    """用户修改密码"""

    def get(self, request):
        """请求修改密码,会发送包含token的邮件到注册邮箱"""
        return json({"message": 'I am get method'})

    def post(self, request):
        """修改密码"""
        return json({"message": 'I am post method'})

