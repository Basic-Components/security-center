"""用于通过session获取当前用户."""

class GetUserMixin:
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

    def to_dict(self):
        return dict(
            status=self.status,
            role=self.role,
            auth_time=self.auth_time,
            close_time=self.close_time,
            ctime=self.ctime,
            utime=self.utime,
            nickname=self.nickname,
            email=self.email,
            phone=self.phone,
            real_name_auth=self.real_name_auth,
            access_authority=self.access_authority,
            info=self.info
        )