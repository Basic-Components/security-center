"""激活和注销用户接口."""
from sanic.views import HTTPMethodView
from sanic.response import json


class UserActivateView(HTTPMethodView):
    """"""
    def get(self, request):
        """获取激活或者注销token"""
        return json({"message": 'I am get method'})

    def post(self, request):
        """激活"""
        return json({"message": 'I am post method'})

    def delete(self,request):
        return 

