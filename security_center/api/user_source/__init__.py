"""用户"""
from sanic.views import HTTPMethodView
from sanic.response import json
from security_center.model import User


class UserView(HTTPMethodView):
    """用户资源的创建"""

    async def post(self, request):
        """创建一个新用户.

        Args:
            nickname (str): - 昵称
            password (str): - 密码
            email (str): - 注册邮箱
            access_authority (str): - 其他服务的访问权限(Optional)
            role (str): - 用户在本服务中的权限,可选的有["超级用户", "管理员用户","普通用户"]

        Raises:
            message (500) : - 未知错误的错误信息
            message (501) : - 权限设置的错误信息

        Returns:
            message (str): - 返回ok
        """
        try:
            await User.create_user(**request.json)
        except ValueError as ve:
            return json(
                {"message": str(ve)},
                501)
        except Exception as e:
            return json(
                {"message": str(e)},
                500
            )
        else:
            return json({"message": 'ok'})

