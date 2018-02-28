
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
        salt = cls.Meta.database.salt.encode("utf-8")
        org_pwd = org_pwd.encode("utf-8")
        hash_pwd = hmac.new(salt, org_pwd)
        return hash_pwd.hexdigest()


    def check_password(self, org_pwd):
        """判断用户密码是否正确.

        Args:
            org_pwd (str): - 输入的密码

        Returns:
            (bool): - 是否输入的密码的hash值和保存的密码hash值一致

        """
        hash_pwd = User.hash_password(org_pwd)
        if self.password == hash_pwd:
            return True
        else:
            return False

    async def change_password(self, new_password: str)->None:
        """更新用户密码.

        Args:
            new_password (str): -用于更新的密码
        """
        hashed_new_password = self.__class__.hash_password(new_password)
        history = dict(self.history)
        password_history = history.get("password")
        if password_history:
            password_history.append({
                self.password
            })
        else:
            password_history
        history.update({
            "password": password_history
        })
        self.password = hashed_new_password

        await self.save()