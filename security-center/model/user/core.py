from datetime import datetime
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

DATETIME_FMT = '%Y-%m-%d %H:%M:%S.%f'


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


def login_info_default():
    """用户登录信息"""
    return {
        'ip': None,  # ip地址
        'device': None,  # 设备
        'platform': None,  # 操作系统平台
        'city': None  # ip地址指定的城市
    }


def changed_history_default():
    return {
        'password': None,  # 使用过的密码
        'nickname': None,  # 使用过的用户名
        'email': None,  # 使用过的email
        'phone': None,  # 使用过的手机号
        'access_authority': None,  # 访问权限变更历史
    }


def access_authority_default():
    return [{
        'name': 'security-center',
        "ctime": datetime.now().strftime(DATETIME_FMT)
    }]


class Core(BaseModel):

    STATUS_CHOICES = ((0, "未认证"), (1, "已认证"), (2, "已注销"))
    DATETIME_FMT = DATETIME_FMT
    # 主键的uid
    uid = UUIDField(primary_key=True, default=uuid4)
    # 账户状态,
    _status = IntegerField(default=0, choices=STATUS_CHOICES)
    # 认证时间
    _auth_time = DateTimeField(formats=DATETIME_FMT, null=True)
    # 注销时间
    _close_time = DateTimeField(formats=DATETIME_FMT, null=True)

    # 用户创建时间
    _create_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)
    # 用户信息更新时间
    _update_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)
    # 用户别名
    _nickname = CharField(unique=True, index=True)
    # 用户创建当前别名的时间
    _nickname_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    # 用户密码
    _password = CharField()
    # 用户创建当前密码的时间
    _password_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    # 用户邮箱
    _email = CharField()
    # 用户当前邮箱写入时间
    _email_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    # 用户手机号
    _phone = CharField(null=True)
    # 用户当前写入手机号时间
    _phone_time = DateTimeField(formats=DATETIME_FMT, null=True)

    # 用户个人信息
    _info = BinaryJSONField(default=info_default)

    # 社交账号
    _social_accounts = BinaryJSONField(null=True)

    # 用户是否通过实名认证
    real_name_auth = BooleanField(default=False)
    # 用户实名认证通过的日期
    _real_name_auth_time = DateTimeField(formats=DATETIME_FMT, null=True)

    # 用于的第三方登录账号
    _thirdpart_auth = BinaryJSONField(null=True)

    # 用于的登录权限
    access_authority = BinaryJSONField(default=access_authority_default)

    # 用户上次的的登录信息
    _login_info = BinaryJSONField(default=login_info_default)

    # 用户信息修改时间
    _changed_history = BinaryJSONField(default=changed_history_default)
    # 用户登录历史记录
    _login_history = BinaryJSONField(null=True)

    def __unicode__(self):
        return dict(self.STATUS_CHOICES)[self._status]

    async def _change_attr(self, attr_name, new_value):
        value = getattr(self, "_" + attr_name)
        now = datetime.now()
        if value is not None:
            now_str = now.strftime(self.DATETIME_FMT)
            history = dict(self.changed_history)
            attr_history = history.get(attr_name)
            nn = {
                "value": value,
                "ctime": getattr(self, "_" + attr_name + "_time").strftime(self.DATETIME_FMT),
                "dtime": now_str
            }
            if attr_history:
                attr_history.append(nn)
            else:
                attr_history = [nn]
            history.update({
                attr_name: attr_history
            })
            self._changed_history = history
        setattr(self, "_c" + attr_name + "_time", now)
        setattr(self, "_" + attr_name, new_value)
        self._update_time = now
        await self.save()

    def _time_to_str(self, attr_name):
        attr_time = getattr(self, "_" + attr_name + "_time")
        if attr_time:
            result = attr_time.strftime(self.DATETIME_FMT)
        else:
            result = None
        return result

    @property
    def status(self):
        return dict(self.STATUS_CHOICES)[self._status]

    @status.setter
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

    @property
    def auth_time(self):
        return self._time_to_str("auth")

    @property
    def close_time(self):
        return self._time_to_str("close")

    @property
    def ctime(self):
        return self._time_to_str("create")

    @property
    def utime(self):
        return self._time_to_str("update")

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    async def nickname(self, newname):
        await self._change_attr("nickname", newname)

    @property
    def cnickname_time(self):
        return self._time_to_str("nickname")

    @property
    def email(self):
        return self._email

    @email.setter
    async def email(self, newemail):
        await self._change_attr("email", newemail)

    @property
    def cemail_time(self):
        return self._time_to_str("email")

    @property
    def phone(self):
        return self._phone

    @phone.setter
    async def phone(self, newemail):
        await self._change_attr("phone", newphone)

    @property
    def cphone_time(self):
        return self._time_to_str("phone")

    @property
    def info(self):
        return self._info

    @info.setter
    async def info(self, new_value):
        self._info = new_value
        self._update_time = datetime.now()
        await self.save()

    @property
    def social_accounts(self):
        return self._social_accounts

    @social_accounts.setter
    async def social_accounts(self, new_value):
        self._social_accounts = new_value
        self._update_time = datetime.now()
        await self.save()

    @property
    def real_name_auth_time(self):
        return self._time_to_str("real_name_auth")

    @property
    def thirdpart_auth(self):
        return self._thirdpart_auth

    @thirdpart_auth.setter
    async def thirdpart_auth(self, new_value):
        self._thirdpart_auth = new_value
        self._update_time = datetime.now()
        await self.save()

    @property
    def login_info(self):
        return self._login_info

    @login_info.setter
    async def login_info(self, *, ip, device, platform, city):
        old_info = dict(self._login_info)
        now_str = datetime.now().strftime(self.DATETIME_FMT)
        self._login_info = {
            "ip": ip,
            'device': device,  # 设备
            'platform': platform,  # 操作系统平台
            'city': city,  # ip地址指定的城市
            'time': now_str
        }
        if self._login_history:
            old_history = dict(self._login_history)
        else:
            old_history = {
                'last': None,
                "statistics": {
                    "ip": [],
                    'device': [],  # 设备
                    'platform': [],  # 操作系统平台
                    'city': []
                }
            }
        result = {
            "last": old_info,
            "statistics": {}
        }
        for att, value in old_info.items():
            if value in old_history["statistics"][att]:
                result["statistics"][att] = {
                    "count": old_history["statistics"][att]["count"] + 1,
                    "first_time": old_history["statistics"][att]["first_time"],
                    "last_time": old_info['time']
                }
            else:
                result["statistics"][att] = {
                    "count": 1,
                    "first_time": old_info['time'],
                    "last_time": old_info['time']
                }

        self._login_history = result
        await self.save()

    @property
    def changed_history(self):
        return self._changed_history

    @property
    def login_history(self):
        return self._login_history

    def to_dict(self):
        return dict(
            uid=self.uid,
            status=self.status,
            auth_time=self.auth_time,
            close_time=self.close_time,
            ctime=self.ctime,
            utime=self.utime,
            nickname=self.nickname,
            cnickname_time=self.cnickname_time,
            cpassword_time=self.cpassword_time,
            email=self.email,
            cemail_time=self.cemail_time,
            phone=self.phone,
            cphone_time=self.cphone_time,
            real_name_auth=self.real_name_auth,
            real_name_auth_time=self._real_name_auth_time,
            access_authority=self.access_authority
        )

    # 用户的登录信息
    #login_info = BinaryJSONField(default=login_info_default)
