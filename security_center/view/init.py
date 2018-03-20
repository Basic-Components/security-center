from sanic import Blueprint
from security_center.model.user import User
views = Blueprint('views', url_prefix='/')


async def verify_logined(request):
    try:
        uid = request['session']['uid']
    except:
        return False
    else:
        try:
            user = await User.get(User.uid==uid)
        except:
            return False
        else:
            if user is None:
                return False
            else:
                return user
