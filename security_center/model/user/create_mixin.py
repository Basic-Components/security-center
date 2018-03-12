from datetime import datetime


class CreateMixin:

    @classmethod
    async def create_user(cls, *,
                          nickname: str,
                          password: str,
                          email: str,
                          access_authority: str=None,
                          role: str=None)->None:
        now_str = datetime.now().strftime(cls.DATETIME_FMT)
        data = {
            '_nickname': nickname,
            '_password': cls.hash_password(password),
            '_email': email
        }
        
        if role:
            role_value = {v: i for i, v in cls.ROLE_CHOICES}.get(role)
            if role_value is None:
                raise ValueError("unknown role {}".format(role))
            else:

                data.update({"_role": role_value})
        if access_authority:
            access_authority = [
                {
                    'name': 'security-center',
                    "ctime": now_str
                },
                {
                    'name': access_authority,
                    'ctime': now_str
                }
            ]
            data.update({"access_authority": access_authority})

        await cls.create(
            **data
        )
