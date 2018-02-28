class CreateMixin:

    @classmethod
    async def create_user(cls, *, nickname, password, email, access_authority=None):
        #
        #uid = str(uuid4())
        now_str = datetime.now().strftime(DATETIME_FMT)
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
            await cls.create(
                _nickname=nickname,
                _password=password,
                _email=email,
                _access_authority=access_authority
            )
        else:
            await cls.create(
                nickname=nickname,
                password=password,
                email=email
            )
            
