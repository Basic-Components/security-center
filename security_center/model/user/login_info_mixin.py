from datetime import datetime
import async_timeout


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
            city = _get_city(ip)
        except:
            city = None
        self._login_info = {
            "ip": ip,
            'device': device,  # 设备
            'platform': platform,  # 操作系统平台
            'city': city,  # ip地址指定的城市
            'time': now_str
        }
        if self._login_history:
            old_history = dict(self._login_history)
        else:
            old_history = {
                'last': None,
                "statistics": {
                    "ip": [],
                    'device': [],  # 设备
                    'platform': [],  # 操作系统平台
                    'city': []
                }
            }

        print("########")
        print(old_info)
        result = {
            "last": old_info,
            "statistics": {}
        }
        if old_info["last"] is None and old_info["statistics"]['ip'] is None
        for att, value in old_info.items():
            if old_history["statistics"][att] is None:
                result["statistics"][att] = {
                    "count": 1,
                    "first_time": old_info['time'],
                    "last_time": old_info['time']
                }
            if value in old_history["statistics"][att]:
                result["statistics"][att] = [{
                    "count": old_history["statistics"][att]["count"] + 1,
                    "first_time": old_history["statistics"][att]["first_time"],
                    "last_time": old_info['time']
                }]
            else:
                result["statistics"][att] = {
                    "count": 1,
                    "first_time": old_info['time'],
                    "last_time": old_info['time']
                }
        self._login_history = result
        await self.save()

    @property
    def login_history(self):
        return self._login_history
