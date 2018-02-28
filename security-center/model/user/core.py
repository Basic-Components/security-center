import hmac
from uuid import uuid4
from model.base import BaseModel
from peewee import (
    CharField,
    DateTimeField,
    UUIDField,
    BooleanField,
    IntegerField,
)
from playhouse.postgres_ext import (
    BinaryJSONField
)


class Core(BaseModel):

    STATUS_CHOICES = ((0, "未认证"), (1, "已认证"), (2, "已注销"))
    DATETIME_FMT = '%Y-%m-%d %H:%M:%S.%f'
    # 主键的uid
    uid = UUIDField(primary_key=True, default=uuid4)
    # 账户状态,
    _status = IntegerField(default=0, choices=Core.STATUS_CHOICES)
    # 认证时间
    auth_time = DateTimeField(formats=Core.DATETIME_FMT, null=True)
    # 注销时间
    close_time = DateTimeField(formats=Core.DATETIME_FMT, null=True)

    # 用户创建时间
    ctime = DateTimeField(formats=Core.DATETIME_FMT, default=datetime.now)
    # 用户信息更新时间
    utime = DateTimeField(formats=Core.DATETIME_FMT, default=datetime.now)
    # 用户别名
    _nickname = CharField(unique=True, index=True)
    # 用户创建当前别名的时间
    _cnickname_time = DateTimeField(formats=Core.DATETIME_FMT, default=datetime.now)

    # 用户密码
    _password = CharField()
    # 用户创建当前密码的时间
    _cpassword_time = DateTimeField(formats=Core.DATETIME_FMT, default=datetime.now)

    # 用户邮箱
    _email = CharField()
    # 用户当前邮箱写入时间
    _cemail_time = DateTimeField(formats=Core.DATETIME_FMT, default=datetime.now)

    # 用户手机号
    _phone = CharField(null=True)
    # 用户当前写入手机号时间
    _cphone_time = DateTimeField(formats=Core.DATETIME_FMT, null=True)

    # 用户个人信息
    info = BinaryJSONField(default=User.info_default)

    # 社交账号
    social_accounts = BinaryJSONField(null=True)

    # 用户是否通过实名认证
    real_name_authentication = BooleanField(default=False)
    # 用户实名认证通过的日期
    real_name_authentication_time = DateTimeField(formats=Core.DATETIME_FMT, null=True)

    # 用于的第三方登录账号
    thirdpart_auth = BinaryJSONField(null=True)

    # 用于的登录权限
    access_authority = BinaryJSONField(default=User.access_authority_default)

    # 用户的登录信息
    login_info = BinaryJSONField(default=User.access_info_default)
    # 用户上次登录的时间,每次登录会刷新
    login_time = DateTimeField(formats=Core.DATETIME_FMT, null=True)

    # 用户信息修改时间
    changed_history = BinaryJSONField(default=User.changed_history_default)
    # 用户登录历史记录
    login_history = BinaryJSONField(null=True)

    def __unicode__(self):
        return dict(self.STATUS_CHOICES)[self._status]

    @property
    def status(self):
        return dict(self.STATUS_CHOICES)[self._status]

    @status.setter(self):
    async def status(self, value: str):
        now = datetime.now()
        real_value = {v: i for i, v in self.STATUS_CHOICES}.get(value)
        if real_value:
            self._status = real_value
            self.utime = now
            now = datetime.now()
            if real_value == 1:
                self.auth_time = now
            elif real_value == 2:
                self.close_time = now
            await self.save()
        else:
            raise ValueError("Illegal status")

    async _change_attr(self, attr_name: str,new_value):
        value = getattr(self, "_" + attr_name)
        now = datetime.now()
        if value is not  None:
            now_str = now.strftime(self.DATETIME_FMT)
            history = dict(self.history)
            attr_history = history.get(attr_name)
            nn = {
                "value": value,
                "ctime": getattr(self, "_c" + attr_name + "_time").strftime(self.DATETIME_FMT),
                "dtime": now_str
            }
            if attr_history:
                attr_history.append(nn)
            else:
                attr_history = [nn]
            history.update({
                attr_name: attr_history
            })
            self.history = history
        setattr(self,"_c"+attr_name+"_time",now)
        setattr(self,"_"+attr_name,new_value)
        self.utime = now
        await self.save()

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    async def nickname(self,newname):
        await self._change_attr("nickname",newname):

    @property
    def email(self):
        return self._email

    @email.setter
    async def email(self,newemail):
        await self._change_attr("email",newemail):

    @property
    def phone(self):
        return self._phone

    @phone.setter
    async def phone(self,newemail):
        await self._change_attr("phone",newphone):

    @staticmethod
    def info_default():
        """默认的用户个人信息字段"""
        return {
            'realname': None,  # 真实姓名
            "id_card": None,  # 身份证号
            "sex": None,  # 姓名
            'nation': None,  # 国籍
            'province': None,  # 省
            'city': None,  # 城市
            'birthday': None,  # 生日
        }

    @staticmethod
    def login_info_default():
        """用户登录信息"""
        return {
            'ip': None,  # ip地址
            'device': None,  # 设备
            'platform': None,  # 操作系统平台
            'city': None  # ip地址指定的城市
        }

    @staticmethod
    def changed_history_default():
        return {
            'password': None,  # 使用过的密码
            'nickname': None  # 使用过的用户名
            'email': None,  # 使用过的email
            'phone': None,  # 使用过的手机号
            'access_authority': None,  # 访问权限变更历史
        }

    @staticmethod
    def access_authority_default():
        return [{
            'name': 'security-center',
            "ctime": datetime.now().strftime(DATETIME_FMT)
        }]
