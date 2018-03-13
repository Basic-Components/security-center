"""用户登录资源"""
from sanic.views import HTTPMethodView
from sanic.response import json


class UserLoginView(HTTPMethodView):

    def post(self, request):
        return json({"message": 'I am post method'})

    def delete(self, request):
        return json({"message": 'I am delete method'})
