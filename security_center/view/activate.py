from sanic.response import redirect
import itsdangerous
from security_center.utils.init_serializer import activate_ser
from security_center.model.user import User
from .init import views



@views.get("/user/activate", name="user_activate")
async def view_user_activate(request):
    try:
        token = request.raw_args["token"]
        uid = activate_ser.loads(token)["uid"]
    except itsdangerous.SignatureExpired:
        request['flash']('Activate Signature Expired !', 'warning')

    except Exception as e:
        request['flash']('token error !', 'danger')
    try:
        user = await User.get(User.uid == uid)
    except Exception as e:
        request['flash']('user not find !', 'danger')
    else:
        if user.status == "已认证":
            request['flash']('already activated !', 'info')
        try:
            await user.set_status("已认证")
        except:
            request['flash']('activate error !', 'danger')
        else:
            request['flash']('activate done !', 'success')
    return redirect("/")
