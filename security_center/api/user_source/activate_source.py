"""激活和注销用户接口."""
from sanic.views import HTTPMethodView
from sanic.response import json
from security_center.init_jinja import jinja
from security_center.model import User

class UserActivateView(HTTPMethodView):
    """"""

    async def get(self, request):
        """获取激活或者注销token"""
        user = await User.get(id=request.json["id"])
        email = user.email
        operate = request.json["operate"]
        if operate == "activate":
            content = jinja.env.get_template('activate.html').render(
                name='sanic!', pic1="猫"
            )
            request.app.send()
        elif operate == "log off":
            content = jinja.env.get_template('activate.html').render(
                name='sanic!', pic1="猫"
            )
            request.app.send()
            return json({"message": 'unknown operate'},501)
        else:
            return json({"message": 'unknown operate'},501)
        
    

    def post(self, request):
        """使用激活token激活用户"""
        return json({"message": 'I am post method'})

    def delete(self, request):
        """使用注销token注销用户"""
        return json({"message": 'I am post method'})
