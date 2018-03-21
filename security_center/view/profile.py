from sanic.response import html, redirect
from security_center.utils.init_jinja import jinja
from security_center.model.user import User
from .init import views, verify_logined


@views.get("/profile", name="profile")
async def profile(request):
    user = await verify_logined(request)
    if user:
        sections = [i for i in views.routes if i.name in ("profile",)]
        return jinja.render(
            'profile.html',
            request,
            title="profile",
            base_url=request.app.config.BASE_URL,
            sections=sections,
            user=user
        )
    else:
        return redirect("/")


__all__ = ["profile"]
