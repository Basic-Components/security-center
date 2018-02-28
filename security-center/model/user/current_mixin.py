"""用于通过session获取当前用户."""

class CurrentMixin:
    @classmethod
    async def current_user(cls, session):
        """获取当前session指定的user实例.

        Args:
            org_pwd (str): - 原始密码

        Returns:
            (str): 原始密码计算hash值的16进制表示

        """
        uid = session['uid']
        user = await cls.get(cls.uid == uid)
        return user