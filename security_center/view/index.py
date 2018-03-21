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
    user = await verify_logined(request)
    if user:
        request['flash']('用户已登录', 'info')
        return redirect('/')
    inputEmail = request.form.get("inputEmail")
    inputPassword = request.form.get("inputPassword")
    user = await User.get(User._email == inputEmail)
    if user is None:
        request['flash']('未找到用户', 'warning')
        return redirect('/')
    if user.check_password(inputPassword) is False:
        request['flash']('密码错误', 'danger')
        return redirect('/')
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
    if user.status == "已认证":
        request['flash']('登录成功', 'success')
        request['session']['uid'] = str(user.uid)
    else:
        request['flash']('登录成功,请激活用户', 'success')
        request['session']['uid'] = str(user.uid)
    return redirect('/')


@views.post("/signup", name="signup")
async def func_signup(request):
    print(request.form)
    inputNickname = request.form.get("inputNickname")
    inputEmail = request.form.get("inputEmail")
    inputPassword = request.form.get("inputPassword")
    user = await User.get(User._nickname==inputNickname)
    if user is not None:
        request['flash'](f'user {inputNickname} already exist!', 'warning')
        return redirect('/')
    user = await User.get(User._email==inputEmail)
    if user is not None:
        request['flash'](f'email {inputEmail} already used!', 'warning')
        return redirect('/')
    if "@" not in inputEmail:
        request['flash']('email format error', 'danger')
        return redirect('/')
    pwd = inputPassword
    if len(pwd) < 6:
        request['flash']('password must longger than 6', 'danger')
        return redirect('/')
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
        request['flash']('password must have upper,lower and numeric', 'danger')
        return redirect('/')
    try:
        kwargs = {
            "nickname": inputNickname,
            'password': inputPassword,
            "email": inputEmail
        }
        u = await User.create_user(**kwargs)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        request['flash']('user create error', 'danger')
        return redirect('/')
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
