from src.Configuration import Settings
from src.StringCleaner import colored_text


class Cookie:
    def __init__(self):
        self.settings = Settings()

    def run(self):
        """提取 Cookie 并写入配置文件"""
        if not (cookie := input("请粘贴 Cookie 内容：")):
            return
        try:
            index = int(input("请输入该 Cookie 的写入位置(索引，默认为0)：") or 0)
        except ValueError:
            print(colored_text("写入位置错误！", 91))
        else:
            self.extract(cookie, index)

    def extract(self, cookie: str, index: int):
        get_key = {
            "passport_csrf_token": None,
            "passport_csrf_token_default": None,
            "odin_tt": None,
            "sessionid": None,
            "sessionid_ss": None,
        }
        for i in cookie.split('; '):
            text = i.split("=", 1)
            if (k := text[0]) in get_key:
                get_key[k] = text[1]
        if all(
                value for key,
                value in get_key.items() if key in (
                        'passport_csrf_token',
                        'odin_tt')):
            self.check_key(get_key)
            self.write(get_key, index)
            print("写入 Cookie 成功！")
        else:
            print(colored_text("Cookie 缺少必需的键值对！", 93))

    @staticmethod
    def check_key(items):
        if not items["sessionid_ss"]:
            del items["sessionid_ss"]
            print("当前 Cookie 未登录")
        else:
            print("当前 Cookie 已登录")
        keys_to_remove = [key for key, value in items.items() if value is None]
        for key in keys_to_remove:
            del items[key]

    def write(self, text, index):
        data = self.settings.read()
        while len(data["cookie"]) < index + 1:
            data["cookie"].append({})
        data["cookie"][index] = text
        self.settings.update(data)

    def get_cookie(self, cookie):
        get_key = {
            "passport_csrf_token": None,
            "passport_csrf_token_default": None,
            "odin_tt": None,
            "sessionid": None,
            "sessionid_ss": None,
        }
        for i in cookie.split('; '):
            text = i.split("=", 1)
            if (k := text[0]) in get_key:
                get_key[k] = text[1]
        if all(
                value for key,
                value in get_key.items() if key in (
                        'passport_csrf_token',
                        'odin_tt')):
            self.check_key(get_key)
            return get_key
        else:
            print(colored_text("Cookie 缺少必需的键值对！", 93))

        return None
