from sanic.response import html, redirect, json
import itsdangerous
from security_center.utils.init_jinja import jinja
from security_center.utils.init_serializer import activate_ser
from security_center.model.user import User
from .init import views, verify_logined



@views.get("/activate", name="activate")
async def view_activate(request):
    try:
        token = request.raw_args["token"]
        uid = activate_ser.loads(token)["uid"]
    except itsdangerous.SignatureExpired:
        return json({
            "message": "Activate Signature Expired"
        }, 410)

    except Exception as e:
        return json({
            "message": "token error"
        }, 400)
    try:
        user = await User.get(User.uid == uid)
    except Exception as e:
        return json({
            "message": "user not find!"
        }, 404)
    else:
        if user.status == "已认证":
            return json(
                {
                    "message": "already activated"
                }
            )
        try:
            await user.set_status("已认证")
        except:
            return json({
                "message": "activate error"
            }, 500)
        else:
            return json(
                {
                    "message": "success activate"
                }
            )



__all__ = ["index"]
