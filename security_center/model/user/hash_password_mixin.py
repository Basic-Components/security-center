import hmac


class HashPasswordMixin:
    @classmethod
    def hash_password(cls, org_pwd: str):
        """原始密码计算hash值.

        使用hmac计算hash值,salt被设置在`datebase`对象的`salt`字段上.

        Args:
            org_pwd (str): - 原始密码

        Returns:
            (str): 原始密码计算hash值的16进制表示.

        """
        salt = cls._meta.database.salt.encode("utf-8")
        org_pwd = org_pwd.encode("utf-8")
        hash_pwd = hmac.new(salt, org_pwd,digestmod="md5")
        return hash_pwd.hexdigest()

    @property
    def cpassword_time(self):
        return self._time_to_str('password')

    def check_password(self, org_pwd):
        """判断用户密码是否正确.

        Args:
            org_pwd (str): - 输入的密码

        Returns:
            (bool): - 是否输入的密码的hash值和保存的密码hash值一致

        """
        hash_pwd = self.__class__.hash_password(org_pwd)
        if hmac.compare_digest(self._password,hash_pwd):
            return True
        else:
            return False

    async def set_password(self, new_password: str)->None:
        """更新用户密码.

        需要使用到core中的`_change_attr`

        Args:
            new_password (str): -用于更新的密码
        """
        hashed_new_password = self.__class__.hash_password(new_password)
        await self._change_attr("password",hashed_new_password)
       