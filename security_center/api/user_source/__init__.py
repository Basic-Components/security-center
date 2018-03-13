"""用户"""
from sanic.views import HTTPMethodView
from sanic.response import json
from security_center.model import User


class UserView(HTTPMethodView):
    """用户资源的创建."""

    async def post(self, request):
        """创建一个新用户.

        只允许创建普通用户.

        Args:
            nickname (str): - 昵称
            password (str): - 密码
            email (str): - 注册邮箱
            access_authority (str): - 其他服务的访问权限(Optional)
            role (str): - 用户在本服务中的权限,可选的有["超级用户", "管理员用户","普通用户"]

        Raises:
            message (500) : - 未知错误的错误信息
            message (501) : - 必要的请求数据不全
            message (502) : - email形式不正确
            message (503) : - 密码不能低于6位
            message (504) : - 密码必须有数字,大写字母,小写字母

        Returns:
            message (str): - 返回ok
        """
        for i in ("nickname", "password", "email"):
            if request.json.get(i) is None:
                return json(
                    {"message": "request must have {}".format(i)}, 501
                )
        if request.json.get("role"):
            return json(
                {"message": "cannot create {} user".format(request.json.get("role"))}
            )
        if "@" not in request.json.get("email"):
            return json(
                {"message": "email format error"}, 502
            )
        pwd = request.json.get('password')
        if len(pwd) < 6:
            return json(
                {"message": "password must longger than 6"}, 503
            )
        numeric = False
        lower = False
        upper = False
        for i in pwd:
            if i.isnumeric():
                numeric = True
            if i.islower():
                lower = True
            if i.isupper():
                upper = True
        if not all([numeric, lower, upper]):
            return json(
                {"message": "password must have upper,lower and numeric"}, 504
            )
        try:
            kwargs = {
                "nickname": request.json.get("nickname"),
                'password': request.json.get('password'),
                "email": request.json.get("email")
            }
            if request.json.get('access_authority'):
                kwargs.update({
                    'access_authority': request.json.get('access_authority')
                })
            u = await User.create_user(**kwargs)
        except Exception as e:
            return json(
                {"message": str(e)},
                500
            )
        else:
            print(u)
            return json({"message": u})
