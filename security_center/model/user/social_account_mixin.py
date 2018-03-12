from datetime import datetime


class SocialAccountMixin:
    @property
    def social_accounts(self):
        return self._social_accounts

    async def _set_social_accounts(self, new_value):
        self._social_accounts = new_value
        self._update_time = datetime.now()
        await self.save()

    async def update_social_accounts(self, **new_value):
        Limit_value = {
            "google": None,
            "qq": None,
            "weichat": None,
            "weibo": None
        }
        value = self.social_accounts
        if value:
            Limit_value.update({
                "google": value.get("google"),
                "qq": value.get("qq"),
                "weichat": value.get("weichat"),
                "weibo": value.get("weibo")
            })
        Limit_value.update({
            "google": new_value.get("google"),
            "qq": new_value.get("qq"),
            "weichat": new_value.get("weichat"),
            "weibo": new_value.get("weibo")
        })
        await self._set_social_accounts(Limit_value)
        return True

    async def remove_social_accounts(self, delete_value: str):
        Limit_value = {
            "google": None,
            "qq": None,
            "weichat": None,
            "weibo": None
        }
        value = self.social_accounts
        if value:
            Limit_value.update({
                "google": value.get("google"),
                "qq": value.get("qq"),
                "weichat": value.get("weichat"),
                "weibo": value.get("weibo")
            })
        f = Limit_value.get(delete_value)
        if not f:
            return False
        else:
            Limit_value[delete_value] = None
            await self._set_social_accounts(Limit_value)
            return True
