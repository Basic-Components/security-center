import base64
from functools import partial
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Ser:

    def __init__(self, app=None, timeout=30):
        if app is not None:
            self.init_app(app, timeout=timeout)
        else:
            self.timeout = timeout

    def init_app(self, app, timeout=None):
        self.app = app
        if timeout is not None:
            self.timeout = timeout
        self.serializer = Serializer(app.config.SECRET, self.timeout)

    def dumps(self, things):
        return base64.b64encode(self.serializer.dumps(things)).decode('ascii')

    def loads(self, things):
        return self.serializer.loads(base64.b64decode(things))


activate_ser = Ser()
