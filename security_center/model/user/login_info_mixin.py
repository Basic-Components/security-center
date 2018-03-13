from datetime import datetime
import async_timeout
import aiohttp
from requests_html import HTML


async def _get_city(ip):
    url = 'http://www.ip138.com/ips138.asp'
    async with aiohttp.ClientSession() as session:
        # async with async_timeout.timeout(10):
        async with session.get(
            url,
            params={
                "ip": ip
            }
        ) as response:
            txt = await response.text()
            # txt.encode('gb18030')#.decode("utf-8")
            html = HTML(html=txt)
            html.encoding = "utf-8"
            lis = html.find('li')
            city = lis[0].text.split("：")[-1].split(" ")[0]
            return city


class LoginInfoMixin:
    @property
    def login_info(self):
        return self._login_info

    async def set_login_info(self, *, ip, device, platform):
        old_info = dict(self._login_info)
        now_str = datetime.now().strftime(self.DATETIME_FMT)
        try:
            city = await _get_city(ip)
        except:
            city = None
        self._login_info = {
            "ip": ip,
            'device': device,  # 设备
            'platform': platform,  # 操作系统平台
            'city': city,  # ip地址指定的城市
            'time': now_str
        }
        if old_info['ip'] is None:
            await self.save()
            return

        old_history = dict(self._login_history)

        for att, value in old_info.items():
            if att == "time":
                continue
            if value in old_history["statistics"][att].keys():
                old_history["statistics"][att][value] = {
                    "count": old_history["statistics"][att][value]["count"] + 1,
                    "first_time": old_history["statistics"][att][value]["first_time"],
                    "last_time": old_info['time']
                }
            else:

                old_history["statistics"][att][value] = {
                    "count": 1,
                    "first_time": old_info['time'],
                    "last_time": old_info['time']
                }
        old_history["last"] = old_info
        self._login_history = old_history
        await self.save()

    @property
    def login_history(self):
        return self._login_history
