"""用户登录资源."""
import sys
import traceback
from sanic.views import HTTPMethodView
from sanic.response import json
from security_center.model import User


class UserProfileView(HTTPMethodView):

    async def get(self, request):
        """获取用户的信息.

        需要已经有session


        Raises:
            message (401): - session错误
            message (500): - 未知错误

        Returns:
            message (str): - 用户信息

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
            print(user.info)
            return json(
                {
                    "message": dict(user.info)
                }
            )

    async def post(self, request):
        """修改用户的信息.

        需要session.

        Args:
            URL (str): - 个人主页地址
            bio (str): - 个人简介
            company (str): - 公司信息
            nation (str): - 国家
            city (str): - 城市

        Raises:
            message (401): - session错误
            message (500): - 未知错误

        Returns:
            message (str): - 登录信息

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
            if user.status != "已激活":
                return json({"message": "should activate first!"}, 502)
            try:
                await user.set_info(**request.json)
            except:
                return json({"message": "save error!"}, 501)
            else:
                return json(
                    {
                        "message": "save done!"
                    }
                )
