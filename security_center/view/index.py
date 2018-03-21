import sys
import traceback
from sanic.response import redirect, json
from sanic.exceptions import NotFound, Unauthorized, ServerError
from user_agents import parse
from security_center.utils.init_jinja import jinja
from security_center.utils.init_serializer import activate_ser
from security_center.model.user import User
from .init import views, verify_logined


@views.get("/", name="home")
@jinja.template('index.html')
async def index(request):
    user = await verify_logined(request)
    sections = [i for i in views.routes if i.name in ("profile")]
    return dict(
        title="home",
        base_url=request.app.config.BASE_URL,
        sections=sections,
        logined=True if user else False
    )

@views.post("/login", name="login")
async def func_login(request):
    print(request.form)
    inputEmail = request.form.get("inputEmail")
    inputPassword = request.form.get("inputPassword")
    user = await User.get(User._email == inputEmail)
    if user is None:
        raise NotFound("未找到用户", status_code=404)
    if user.check_password(inputPassword) is False:
        raise Unauthorized("密码错误", 401)
    device = "api"
    if request.headers.get('user-agent'):
        user_agent = parse(request.headers['user-agent'])
        if user_agent.is_touch_capable:
            device = "touch_capable"
        if user_agent.is_pc:
            device = "pc"
        if user_agent.is_mobile:
            device = "mobile"
        if user_agent.is_tablet:
            device = "tablet"
        if user_agent.is_bot:
            device = "bot"
    await user.set_login_info(
        ip=request.ip,
        device=device
    )
    request['session']['uid'] = str(user.uid)
    return redirect('/')


@views.post("/signup", name="signup")
async def func_signup(request):
    print(request.form)
    inputNickname = request.form.get("inputNickname")
    inputEmail = request.form.get("inputEmail")
    inputPassword = request.form.get("inputPassword")
    if "@" not in inputEmail:
        raise Unauthorized("email format error", 401)
    pwd = inputPassword
    if len(pwd) < 6:
        raise Unauthorized("password must longger than 6", 401)
    numeric = False
    lower = False
    upper = False
    for i in pwd:
        if i.isnumeric():
            numeric = True
        if i.islower():
            lower = True
        if i.isupper():
            upper = True
    if not all([numeric, lower, upper]):
        raise Unauthorized("password must have upper,lower and numeric", 401)
    try:
        kwargs = {
            "nickname": inputNickname,
            'password': inputPassword,
            "email": inputEmail
        }
        u = await User.create_user(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise ServerError(str(e), 500)
    else:
        token = activate_ser.dumps({"uid": str(u.uid)})
        activate_url = request.app.config.BASE_URL + "/user/activate/?token=" + token
        content = jinja.env.get_template('emails/activate.html').render(
            activate_url=activate_url
        )
        await request.app.send_email(
            targetlist=u.email,
            subject="激活邮件",
            content=content,
            html=True
        )
        request['flash']('have sent activate email to your email address', 'info')
        request['session']['uid'] = str(u.uid)
        return redirect('/')
