from datetime import datetime
from pathlib import Path
from uuid import uuid4
from peewee import (
    CharField,
    DateTimeField,
    UUIDField,
    BooleanField,
    IntegerField,
    # BlobField
    TextField
)
from playhouse.postgres_ext import (
    BinaryJSONField
)
from ..base import BaseModel

DATETIME_FMT = '%Y-%m-%d %H:%M:%S.%f'


def info_default():
    """默认的用户个人信息字段"""
    return {
        'URL': None,  # 自己的博客站
        "bio": None,  # 简单描述(200字内)
        "company": None,  # 企业名
        'nation': None,  # 设置的所在国家
        'city': None,  # 设置的所在城市
    }


def realinfo_default():
    """默认的用户个人真实信息字段"""
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
        'city': None,  # ip地址指定的城市
        'time': None  # 登录的时间
    }


def changed_history_default():
    return {
        'password': None,  # 使用过的密码
        'nickname': None,  # 使用过的用户名
        'email': None,  # 使用过的email
        'phone': None,  # 使用过的手机号
        'access_authority': None,  # 访问权限变更历史
    }


def login_history_default():
    return {
        "last": None,
        "statistics": {
            'ip': {},
            'device': {},
            'platform': {},
            'city': {},
        }
    }


def access_authority_default():
    return [{
        'name': 'security-center',
        "ctime": datetime.now().strftime(DATETIME_FMT)
    }]


class Core(BaseModel):

    STATUS_CHOICES = ((0, "未认证"), (1, "已认证"), (2, "已注销"))
    ROLE_CHOICES = ((0, "超级用户"), (1, "管理员用户"), (2, "普通用户"))
    DATETIME_FMT = DATETIME_FMT
    # 主键的uid
    uid = UUIDField(primary_key=True, default=uuid4)
    # 账户状态,
    _status = IntegerField(default=0, choices=STATUS_CHOICES)
    # 账户权限
    _role = IntegerField(default=2, choices=STATUS_CHOICES)
    # 认证时间
    _auth_time = DateTimeField(formats=DATETIME_FMT, null=True)
    # 注销时间
    _close_time = DateTimeField(formats=DATETIME_FMT, null=True)

    # 用户创建时间
    _create_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)
    # 用户信息更新时间
    _update_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)
    # 用户别名
    _nickname = CharField(unique=True, max_length=40,index=True)
    # 用户创建当前别名的时间
    _nickname_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    # 用户密码
    _password = CharField(max_length=40)
    # 用户创建当前密码的时间
    _password_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    # 用户邮箱
    _email = CharField(unique=True,max_length=40)
    # 用户当前邮箱写入时间
    _email_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    # 用户头像
    _img_type = CharField(null=True)
    _img_base64 = TextField(null=True)

    # 用户手机号
    _phone = CharField(null=True)
    # 用户当前写入手机号时间
    _phone_time = DateTimeField(formats=DATETIME_FMT, null=True)

    # 用户个人信息
    _info = BinaryJSONField(default=info_default)

    # 社交账号
    _social_accounts = BinaryJSONField(null=True)

    # 用户是否通过实名认证
    _real_name_auth = BooleanField(default=False)
    # 用户实名认证通过的日期
    _real_name_auth_time = DateTimeField(formats=DATETIME_FMT, null=True)
    # 用户真实信息
    _realinfo = BinaryJSONField(default=realinfo_default)

    # 用于的第三方登录账号
    _thirdpart_auth = BinaryJSONField(null=True)

    # 用于的登录权限
    access_authority = BinaryJSONField(default=access_authority_default)

    # 用户上次的的登录信息
    _login_info = BinaryJSONField(default=login_info_default)

    # 用户信息修改时间
    _changed_history = BinaryJSONField(default=changed_history_default)
    # 用户登录历史记录
    _login_history = BinaryJSONField(default=login_history_default)

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
        setattr(self, "_" + attr_name + "_time", now)
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

    async def set_nickname(self, newname):
        await self._change_attr("nickname", newname)

    @property
    def cnickname_time(self):
        return self._time_to_str("nickname")

    @property
    def email(self):
        return self._email

    async def set_email(self, newemail):
        await self._change_attr("email", newemail)

    @property
    def cemail_time(self):
        return self._time_to_str("email")

    @property
    def phone(self):
        return self._phone

    async def set_phone(self, newphone):
        await self._change_attr("phone", newphone)

    @property
    def cphone_time(self):
        return self._time_to_str("phone")

    @property
    def info(self):
        return self._info

    async def set_info(self, **kwargs):
        info = self.info
        info.update(kwargs)
        data = {
            'URL': info.get('URL'),
            "bio": info.get('bio'),
            "company": info.get('company'),
            'nation': info.get('nation'),
            'city': info.get('city'),
        }
        self._info = data
        self._update_time = datetime.now()
        await self.save()

    @property
    def changed_history(self):
        return self._changed_history
