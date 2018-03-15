"""用户登录资源."""
from sanic.views import HTTPMethodView
from sanic.response import json
from security_center.model import User


class UserLoginView(HTTPMethodView):

    async def post(self, request):
        """登录."""
        username = request.json["username"]
        user0 = await User.get(User._nickname == username)
        user1 = await User.get(User._email == username)

        if not any([user0, user1]):
            return json({"message": "can not find this user"}, 404)
        if user0 is not None:
            user = user0
        else:
            user = user1
        if user.check_password(request.json["password"]) is False:
            return json({"message": "password error"}, 401)
        request['session']['uid'] = user.uid
        return json(
            {
                "message": 'set token in your session',
                "token": request['session'].sid
            }
        )

    async def delete(self, request):
        """退出登录."""
        try:
            uid = request['session']['uid']
        except:
            return json({
                "message": "log in again!"
            }, 401)
        else:
            user = await User.get(User.uid == uid)
            if user is None:
                return json({
                    "message": "unknown user!"
                }, 404)
            else:
                request['session'] == None
                return json({"message": 'log out done'})
