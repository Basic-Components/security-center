from sanic.response import html, redirect, json
import itsdangerous
from security_center.utils.init_jinja import jinja
from security_center.utils.init_serializer import activate_ser
from security_center.model.user import User
from .init import views, verify_logined


@views.get("/", name="home")
async def index(request):
    user = await verify_logined(request)
    sections = [i for i in views.routes if i.name in ("login", "signup")]
    content = jinja.env.get_template('index.html').render(
        title="home",
        base_url=request.app.config.BASE_URL,
        sections=sections,
        logined=True if user else False
    )
    return html(content)


@views.get("/login", name="login")
async def view_login(request):
    pass

    # try:
    #     uid = request['session']['uid']
    # except KeyError:
    #     content = jinja.env.get_template('login.html').render(
    #     )
    #     return html(content)
    # else:
    #     return redirect('/')


@views.get("/signup", name="signup")
async def view_signup(request):
    try:
        uid = request['session']['uid']
    except KeyError:
        content = jinja.env.get_template('sighup.html').render(
        )
        return html(content)
    else:
        return redirect('/')


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


@views.get("/reset_password", name="reset_password")
async def view_forget_password(request):
    pass


@views.get("/reset_password/activate", name="reset_password_activate")
async def view_forget_password_activate(request):
    pass

__all__ = ["index"]
