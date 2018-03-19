"""用户登录资源."""
import sys
import traceback
from sanic.views import HTTPMethodView
from sanic.response import json
from security_center.model import User
from user_agents import parse


class UserLoginView(HTTPMethodView):

    async def get(self, request):
        """查看已登录用户是否有访问特定应用的权限.

        需要已经有session

        Parameters:
            application (str): - 登录的应用名

        Raises:
            message (401): - session错误
            message (500): - 未知错误

        Returns:
            can_access (bool): - 是否可以登录应用

        """
        try:
            uid = request['session']['uid']
        except KeyError:
            return json({
                "message": "wrong session,log in again!"
            }, 401)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return json({
                "message": str(e)
            }, 500)
        else:
            user = await User.get(User.uid == uid)
            if request.raw_args["application"] in [i["name"] for i in user.access_authority] and user.status == "已认证":
                return json({
                    "can_access": True
                })
            else:
                return json({
                    "can_access": False
                })

    async def post(self, request):
        """用户登录.

        无视session.

        Args:
            username (str): - 用户的nickname或者email
            password (str): - 用户的密码
            application (str): - 用户要登录的应用名[Optinal]

        Raises:
            message (404): - 登录信息的用户未找到
            message (401): - 密码错误
            message (500): - 未知错误

        Returns:
            message (str): - 登录信息
            token (str): - 用于后续快速登录的token
            can_access (bool): - 是否有权限登录[Optinal]

        """
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
        device = "api"
        if request.headers.get('user-agent'):
            user_agent = parse(request.headers['user-agent'])
            if user_agent.is_touch_capable:
                device = "touch_capable"
            if user_agent.is_pc:
                device = "pc"
            if user_agent.is_mobile:
                device = "mobile"
            if user_agent.is_tablet:
                device = "tablet"
            if user_agent.is_bot:
                device = "bot"
        await user.set_login_info(
            ip=request.ip,
            device=device
        )

        request['session']['uid'] = str(user.uid)
        if request.json.get("application"):
            if request.json["application"] in [i["name"] for i in user.access_authority] and user.status == "已认证":
                return json(
                    {
                        "message": 'set token in your session',
                        "token": request['session'].sid,
                        "can_access": True
                    }
                )
            else:
                return json(
                    {
                        "message": 'set token in your session',
                        "token": request['session'].sid,
                        "can_access": False
                    }
                )
        else:
            return json(
                {
                    "message": 'set token in your session',
                    "token": request['session'].sid
                }
            )

    async def delete(self, request):
        """退出登录.

        需要已经有session.

        Raises:
            message (401): - session错误
            message (500): - 未知错误

        Returns:
            message (str): - 退出信息

        """
        try:
            uid = request['session']['uid']
        except KeyError:
            traceback.print_exc(file=sys.stdout)
            return json({
                "message": "wrong session,log in again!"
            }, 401)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return json({
                "message": str(e)
            }, 500)
        else:
            request['session'] == None
            return json({"message": 'log out done'})
