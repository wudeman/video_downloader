import contextlib
import time
from datetime import date
from datetime import datetime
from random import choice
from random import randrange
from re import compile
from urllib.parse import quote
from urllib.parse import urlparse

import requests

from src.Parameter import MsToken
from src.Parameter import TtWid
from src.Parameter import WebID
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.StringCleaner import Cleaner


def generate_user_agent():
    user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    ]

    return choice(user_agent)


def sleep():
    """避免频繁请求"""
    time.sleep(randrange(10, 40, 5) * 0.1)


def reset(function):
    """重置数据"""

    def inner(self, *args, **kwargs):
        if not isinstance(self.url, bool):
            self.id_ = None
        self.comment = []
        self.reply = []
        self.mix_total = []
        self.mix_data = []
        self.search_data = []
        self.cursor = 0
        self.name = None
        self.uid = None
        self.video_data = []  # 视频ID数据
        self.image_data = []  # 图集ID数据
        self.finish = False  # 是否获取完毕
        return function(self, *args, **kwargs)

    return inner


def check_cookie(function):
    """检查是否设置了Cookie"""

    def inner(self, *args, **kwargs):
        if self.cookie:
            return function(self, *args, **kwargs)
        print("未设置Cookie！")
        return False

    return inner


def retry(finish=False):
    """发生错误时尝试重新执行，装饰的函数需要返回布尔值"""

    def inner(function):
        def execute(self, *args, **kwargs):
            for i in range(self.retry):
                with contextlib.suppress(requests.exceptions.ConnectTimeout):
                    if result := function(self, *args, **kwargs):
                        return result
                    else:
                        print(f"正在尝试第 {i + 1} 次重试")
            if not (result := function(self, *args, **kwargs)) and finish:
                self.finish = True
            return result

        return execute

    return inner


class UserData:
    headers = {
        "User-Agent": generate_user_agent(),
        'Referer': 'https://www.douyin.com/',
    }
    # 抖音
    share = compile(
        r".*?(https://v\.douyin\.com/[A-Za-z0-9]+?/).*?")  # 分享短链
    account_link = compile(
        r".*?https://www\.douyin\.com/user/([a-zA-z0-9-_]+)(?:\?modal_id=([0-9]{19}))?.*?")  # 账号链接
    works_link = compile(
        r".*?https://www\.douyin\.com/(?:video|note)/([0-9]{19}).*?")  # 作品链接
    mix_link = compile(
        r".*?https://www.douyin.com/collection/(\d{19}).*?")  # 合集链接
    live_link = compile(r".*?https://live\.douyin\.com/([0-9]+).*?")  # 直播链接
    live_api = "https://live.douyin.com/webcast/room/web/enter/"  # 直播API
    comment_api = "https://www.douyin.com/aweme/v1/web/comment/list/"  # 评论API
    reply_api = "https://www.douyin.com/aweme/v1/web/comment/list/reply/"  # 评论回复API
    collection_api = "https://www.douyin.com/aweme/v1/web/aweme/listcollection/"  # 收藏API
    mix_api = "https://www.douyin.com/aweme/v1/web/mix/aweme/"  # 合集API
    mix_list_api = "https://www.douyin.com/aweme/v1/web/mix/listcollection/"  # 合集列表API
    info_api = "https://www.douyin.com/aweme/v1/web/im/user/info/"  # 账号简略数据API
    feed_api = "https://www.douyin.com/aweme/v1/web/tab/feed/"  # 推荐页API
    user_api = "https://www.douyin.com/aweme/v1/web/user/profile/other/"  # 账号详细数据API
    hot_api = "https://www.douyin.com/aweme/v1/web/hot/search/list/"  # 热点API
    spotlight_api = "https://www.douyin.com/aweme/v1/web/im/spotlight/relation/"  # 关注账号API
    familiar_api = "https://www.douyin.com/aweme/v1/web/familiar/feed/"  # 朋友作品推荐API
    follow_api = "https://www.douyin.com/aweme/v1/web/follow/feed/"  # 关注账号作品推荐API
    history_api = "https://www.douyin.com/aweme/v1/web/history/read/"  # 观看历史API
    following_api = "https://www.douyin.com/aweme/v1/web/user/following/list/"  # 关注列表API
    search_api = (
        ("https://www.douyin.com/aweme/v1/web/general/search/single/", 15, "aweme_general", "general",),
        ("https://www.douyin.com/aweme/v1/web/search/item/", 20, "aweme_video_web", "video",),
        ("https://www.douyin.com/aweme/v1/web/discover/search/", 12, "aweme_user_web", "user",),
        ("https://www.douyin.com/aweme/v1/web/live/search/", 15, "aweme_live", "",),
        ("API", "首次请求返回数量", "search_channel", "type")
    )
    # TikTok
    works_tiktok_link = compile(
        r".*?https://www\.tiktok\.com/@.+/video/(\d+).*?")  # 匹配作品链接
    recommend_api = "https://www.tiktok.com/api/recommend/item_list/"  # 推荐页API
    home_tiktok_api = "https://www.tiktok.com/api/post/item_list/"  # 发布页API
    user_tiktok_api = "https://www.tiktok.com/api/user/detail/"  # 账号数据API
    related_tiktok_api = "https://www.tiktok.com/api/related/item_list/"  # 猜你喜欢API
    comment_tiktok_api = "https://www.tiktok.com/api/comment/list/"  # 评论API
    reply_tiktok_api = "https://www.tiktok.com/api/comment/list/reply/"  # 评论回复API
    clean = Cleaner()  # 过滤非法字符
    max_comment = 256  # 评论字数限制

    def __init__(self, log: LoggerManager | BaseLogger, xb):
        self.log = log  # 日志记录对象，通用
        self.data = None  # 数据记录对象，评论抓取和账号数据抓取调用，调用前赋值
        self._cookie = {}  # Cookie，通用
        self.id_ = None  # sec_uid or item_ids
        self.comment = []  # 评论数据
        self.cursor = 0  # 最早创建日期，时间戳
        self.reply = []  # 评论回复的ID列表
        self.mix_total = []  # 合集作品数据
        self.mix_data = []  # 合集作品数据未处理JSON
        self.search_data = []  # 搜索结果
        self.uid = None  # 账号UID，运行时获取
        self.list = []  # 未处理的数据，循环时重置
        self.name = None  # 账号昵称，运行时获取
        self._mark = None  # 账号标识，调用前赋值
        self.video_data = []  # 视频ID数据
        self.image_data = []  # 图集ID数据
        self.finish = False  # 是否获取完毕
        self.favorite = False  # 喜欢页下载模式，调用前赋值
        self._earliest = None  # 最早发布时间，调用前赋值
        self._latest = None  # 最晚发布时间，调用前赋值
        self._url = None  # 账号链接，调用前赋值
        self._api = None  # 批量下载类型，调用前赋值
        self._proxies = None  # 代理，通用
        self._time = None  # 创建时间格式，通用
        self.retry = 10  # 重试最大次数，通用
        self.tiktok = False  # TikTok 平台
        self.xb = xb  # 加密参数对象
        self.__web = None

    def set_web_id(self):
        if not self.__web:
            self.__web = WebID.get_web_id(
                self.headers["User-Agent"]) or "7255854455597598219"

    def get_web_id(self):
        return self.__web

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if self.share.match(value):
            self._url = value
            self.log.info(f"当前账号链接: {value}", False)
        elif len(s := self.account_link.findall(value)) == 1:
            self._url = True
            self.id_ = s[0][0]
            self.log.info(f"当前账号链接: {value}", False)
        else:
            self.log.warning(f"无效的账号链接: {value}")

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        if value == "post":
            self._api = f"https://www.douyin.com/aweme/v1/web/aweme/{value}/"
            self.favorite = False
        elif value == "favorite":
            self._api = f"https://www.douyin.com/aweme/v1/web/aweme/{value}/"
            self.favorite = True
        else:
            self.log.warning(f"批量下载类型错误！必须设置为“post”或者“favorite”，错误值: {value}")

    @property
    def cookie(self):
        return self._cookie

    @cookie.setter
    def cookie(self, cookie: dict):
        if isinstance(cookie, dict):
            self._cookie = cookie
            for i in (MsToken.get_ms_token(), TtWid.get_tt_wid(),):
                if isinstance(i, dict):
                    self._cookie |= i
            self.headers["Cookie"] = "; ".join(
                [f"{i}={j}" for i, j in self._cookie.items()])

    @property
    def earliest(self):
        return self._earliest

    @earliest.setter
    def earliest(self, value):
        if not value:
            self._earliest = date(2016, 9, 20)
            return
        try:
            self._earliest = datetime.strptime(
                value, "%Y/%m/%d").date()
            self.log.info(f"作品最早发布日期: {value}")
        except ValueError:
            self.log.warning("作品最早发布日期无效")

    @property
    def latest(self):
        return self._latest

    @latest.setter
    def latest(self, value):
        if not value:
            self._latest = date.today()
            return
        try:
            self._latest = datetime.strptime(value, "%Y/%m/%d").date()
            self.log.info(f"作品最晚发布日期: {value}")
        except ValueError:
            self.log.warning("作品最晚发布日期无效")

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, value):
        if value and isinstance(value, str):
            test = {
                "http": value,
                "https": value,
                "ftp": value
            }
            try:
                response = requests.get(
                    "https://www.baidu.com/", proxies=test, timeout=10)
                if response.status_code == 200:
                    self.log.info("代理测试通过")
                    self._proxies = test
                    return
            except requests.exceptions.ReadTimeout:
                self.log.warning("代理测试超时")
            except (requests.exceptions.ProxyError, requests.exceptions.SSLError):
                self.log.warning("代理测试失败")
        self._proxies = {
            "http": None,
            "https": None,
            "ftp": None,
        }

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        if value:
            try:
                _ = time.strftime(value, time.localtime())
                self._time = value
                self.log.info(f"时间格式设置成功: {value}", False)
            except ValueError:
                self.log.warning(f"时间格式错误: {value}，将使用默认时间格式(年-月-日 时.分.秒)")
                self._time = "%Y-%m-%d %H.%M.%S"
        else:
            self.log.warning("错误的时间格式，将使用默认时间格式(年-月-日 时.分.秒)")
            self._time = "%Y-%m-%d %H.%M.%S"

    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        if not value or not isinstance(value, str):
            self._mark = None
        else:
            self._mark = s if (s := self.clean.filter(value)) else None

    @retry(finish=False)
    def get_id(self, value="sec_user_id", url="", return_=False) -> bool | str:
        """获取账号ID、作品ID、直播ID"""
        if self.id_:
            self.log.info(f"{url} {value}: {self.id_}", False)
            return True
        url = url or self.url
        try:
            response = requests.get(
                url,
                headers=self.headers,
                proxies=self.proxies,
                allow_redirects=False,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.warning(f"获取 {value} 超时")
            return False
        if response.content == b"":
            self.log.warning(f"{url} {value} 响应内容为空")
            return False
        params = urlparse(response.headers['Location'])
        url_list = params.path.rstrip("/").split("/")
        if return_:
            return url_list[-1] or url_list[-2]
        else:
            self.id_ = url_list[-1] or url_list[-2]
        self.log.info(f"{url} {value}: {self.id_}", False)
        return True

    def deal_url_params(self, params: dict):
        xb = self.xb.get_x_bogus(params, self.headers["User-Agent"])
        params["X-Bogus"] = xb

    @retry(finish=True)
    def get_user_data(self) -> bool:
        """获取账号作品数据"""
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "sec_user_id": self.id_,
            "max_cursor": self.cursor,
            "count": "18",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
            "webid": self.__web,
        }
        self.deal_url_params(params)
        self.list = []
        try:
            response = requests.get(
                self.api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取账号作品数据超时")
            return False
        except requests.exceptions.ConnectionError:
            self.log.error("获取账号作品数据时网络异常")
            return False
        if response.content == b"":
            self.log.warning("账号作品数据响应内容为空")
            return False
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            self.log.error("账号作品数据返回内容异常！疑似接口失效", False)
            return False
        try:
            if (list_ := data["aweme_list"]) is None:
                self.log.info("该账号为私密账号，需要使用登陆后的 Cookie，且登录的账号需要关注该私密账号")
                self.finish = True
            else:
                self.cursor = data['max_cursor']
                self.list = list_
                self.finish = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"账号作品数据响应内容异常: {data}", False)
            return False

    def deal_data(self):
        """对账号作品进行分类"""
        if len(self.list) == 0:
            return
        self.uid = f'UID{self.list[0]["author"]["uid"]}'
        self.name = self.clean.filter(
            self.list[0]["author"]["nickname"]) or self.uid
        for item in self.list:
            if item["images"]:
                self.image_data.append(
                    [item["create_time"], item])
            else:
                self.video_data.append(
                    [item["create_time"], item])

    def summary(self):
        """汇总账号作品数量"""
        self.log.info(f"账号 {self.name} 的视频总数: {len(self.video_data)}")
        for i in self.video_data:
            self.log.info(
                f"视频: {i['aweme_id']}", False)
        self.log.info(f"账号 {self.name} 的图集总数: {len(self.image_data)}")
        for i in self.image_data:
            self.log.info(f"图集: {i['aweme_id']}", False)

    @retry(finish=False)
    def get_nickname(self):
        """喜欢页下载模式需要额外发送请求获取账号昵称和UID"""
        params = {
            "aid": "6383",
            "sec_user_id": self.id_,
            "max_cursor": 0,
            "count": "18",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
            "webid": self.__web,
        }
        self.deal_url_params(params)
        self.name = str(time.time())[:10]
        try:
            response = requests.get(
                self.api.replace("favorite", "post"),
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            self.log.warning(
                f"请求超时，获取账号昵称失败，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
            return False
        if response.content == b"":
            self.log.warning(
                f"账号昵称响应内容为空，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
            return False
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            self.log.warning(
                f"数据接口返回内容异常，获取账号昵称失败，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
            return False
        try:
            self.uid = f'UID{data["aweme_list"][0]["author"]["uid"]}'
            self.name = self.clean.filter(
                data["aweme_list"][0]["author"]["nickname"]) or self.uid
            return True
        except KeyError:
            self.log.warning(
                f"响应内容异常，获取账号昵称失败，本次运行将默认使用当前时间戳作为帐号昵称: {self.name}")
            return False

    def early_stop(self):
        """如果获取数据的发布日期已经早于限制日期，就不需要再获取下一页的数据了"""
        if self.favorite:
            return
        if self.uid and self.earliest > datetime.fromtimestamp(
                max(self.cursor / 1000, 0)).date():
            self.finish = True

    def get_user_id(self, check=False):
        if check and not all(
                (self.api,
                 self.url,
                 self.earliest,
                 self.latest,)):
            self.log.warning("请检查账号链接、批量下载类型、最早发布日期、最晚发布日期是否正确")
            return False
        self.get_id()
        if not self.id_:
            self.log.error("获取账号 sec_user_id 失败")
            return False
        return True

    def get_public_num(self):
        """获取公开作品数量"""
        # 公开作品数量不准确
        if self.video_data:
            self.log.info(
                f'{self.name} 公开作品数量: {self.video_data[0][1]["author"]["aweme_count"]}')
        elif self.image_data:
            self.log.info(
                f'{self.name} 公开作品数量: {self.image_data[0][1]["author"]["aweme_count"]}')
        else:
            self.log.info(f"{self.name or '该账号'}未获取到公开作品")

    @reset
    @check_cookie
    def run(self, tip: str):
        """批量下载模式"""
        self.log.info(f"正在获取{tip}账号数据")
        if not self.get_user_id(True):
            return False
        while not self.finish:
            self.get_user_data()
            self.deal_data()
            self.early_stop()
        self.log.info("该账号的作品数据获取结束")
        if self.favorite:
            self.get_nickname()
        else:
            self.get_public_num()
        if not all((self.name, self.uid)):
            self.log.error(f"获取{tip}账号数据失败，请稍后重试")
            return False
        self.date_filters()
        self.summary()
        self.log.info(f"获取{tip}账号数据成功")
        if not self.mark:
            self.mark = self.name
        return True

    @reset
    @check_cookie
    def run_alone(
            self,
            text: str,
            value="aweme_id",
            solo=False,
            user=False, mix=False) -> list | bool | tuple:
        """单独下载模式"""
        url = self.check_url(text, user, mix)
        if not url:
            self.log.warning(f"提取账号链接或作品链接失败: {text}")
            return False
        if isinstance(url, bool):
            return self.id_[:1] if solo else self.id_
        elif isinstance(url, list):
            if solo:
                url = url[:1]
            result = [
                self.get_id(
                    value=value,
                    url=i,
                    return_=True) for i in url]
            result = [i for i in result if i]
            if user:
                return [f"https://www.douyin.com/user/{i}" for i in result]
            if mix:
                return (result,) if result else False
            return result or False
        elif isinstance(url, tuple):
            return (url[0][:1],) if solo else url
        else:
            raise TypeError

    def check_url(
            self,
            url: str,
            user: bool,
            mix=False) -> bool | list | tuple:
        self.tiktok = False
        if len(s := self.works_link.findall(url)) >= 1:
            self.id_ = s
            return True
        elif len(s := self.share.findall(url)) >= 1:
            return s
        elif len(s := self.account_link.findall(url)) >= 1:
            self.id_ = (
                [f"https://www.douyin.com/user/{i[0]}" for i in s]
                if user
                else [i[1] for i in s]
            )
            return True
        elif len(u := self.works_tiktok_link.findall(url)) >= 1:
            self.id_ = u
            self.tiktok = True
            return True
        elif mix and len(u := self.mix_link.findall(url)) >= 1:
            return (u,)
        return False

    def date_filters(self):
        """筛选发布时间"""
        earliest_date = self.earliest
        latest_date = self.latest
        filtered = []
        for item in self.video_data:
            date_ = datetime.fromtimestamp(item[0]).date()
            if earliest_date <= date_ <= latest_date:
                filtered.append(item[1])
        self.video_data = filtered
        filtered = []
        for item in self.image_data:
            date_ = datetime.fromtimestamp(item[0]).date()
            if earliest_date <= date_ <= latest_date:
                filtered.append(item[1])
        self.image_data = filtered

    def get_live_id(self, link: str) -> list:
        """检查直播链接并返回直播ID"""
        if len(s := self.live_link.findall(link)) >= 1:
            return s
        # elif len(s := self.share.findall(link)) >= 1:
        #     s = [self.get_id("room_id", i, True) for i in s]
        #     s = [i for i in s if i]
        #     return s or []
        return []

    def return_live_ids(self, text, solo=False) -> bool | list:
        id_ = self.get_live_id(text)
        if not id_:
            self.log.warning(f"直播链接格式错误: {text}")
            return False
        return id_[:1] if solo else id_

    @check_cookie
    def get_live_data(self, id_: str):
        params = {
            "aid": "6383",
            "app_name": "douyin_web",
            "device_platform": "web",
            "cookie_enabled": "true",
            "web_rid": id_,
        }
        self.deal_url_params(params)
        try:
            response = requests.get(
                self.live_api,
                headers=self.headers,
                params=params,
                timeout=10,
                proxies=self.proxies)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.warning("获取直播数据超时")
            return False
        except requests.exceptions.JSONDecodeError:
            self.log.warning("直播数据内容格式错误")
            return False
        if response.content == b"":
            self.log.warning("直播数据响应内容为空")
            return False
        return response.json()

    def deal_live_data(self, data):
        try:
            if data["data"]["data"][0]["status"] == 4:
                self.log.info("当前直播已结束")
                return None
            nickname = self.clean.filter(
                data["data"]["data"][0]["owner"]["nickname"])
            title = self.clean.filter(data["data"]["data"][0]["title"])
            url = data["data"]["data"][0]["stream_url"]["flv_pull_url"]
            cover = data["data"]["data"][0]["cover"]["url_list"][0]
            return nickname, title, url, cover
        except KeyError as e:
            self.log.error(f"发生错误: {e}, 数据: {data}")
            return None

    @reset
    @check_cookie
    def run_comment(self, id_: str, data):
        self.data = data
        self.log.info("开始获取评论数据")
        while not self.finish:
            self.get_comment(id_=id_, api=self.comment_api)
            self.deal_comment()
        for item in self.reply:
            self.finish = False
            self.cursor = 0
            while not self.finish:
                self.get_comment(id_=id_, api=self.reply_api, reply=item)
                self.deal_comment()
        self.log.info("评论数据获取结束")

    @retry(finish=True)
    def get_comment(self, id_: str, api: str, reply=""):
        """获取评论数据"""
        if reply:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "item_id": id_,
                "comment_id": reply,
                "cursor": self.cursor,
                "count": "3",  # 每次返回数据的数量
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
                "webid": self.__web,
            }
        else:
            params = {
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "aweme_id": id_,
                "cursor": self.cursor,
                "count": "20",
                "cookie_enabled": "true",
                "platform": "PC",
                "downlink": "10",
                "webid": self.__web,
            }
        self.deal_url_params(params)
        self.comment = []
        try:
            response = requests.get(
                api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取评论数据超时")
            return False
        if response.content == b"":
            self.log.warning("账号作品数据响应内容为空")
            return False
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            self.log.error("评论数据返回内容异常！疑似接口失效", False)
            return False
        try:
            self.comment = data["comments"]
            self.cursor = data["cursor"]
            self.finish = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"评论数据内容异常: {data}", False)
            return False

    @staticmethod
    def get_author_data(data):
        """部分数据需要已登录的 Cookie 才可获取"""
        data = data["user"]
        uid = data["uid"]
        sec_uid = data["sec_uid"]
        short_id = data.get("short_id") or ""
        unique_id = data.get("unique_id") or ""
        user_age = data.get("user_age") or "-1"
        signature = data.get("signature") or ""
        nickname = data.get("nickname") or "已注销账号"
        return uid, sec_uid, short_id, unique_id, user_age, signature, nickname

    def deal_comment(self):
        if not self.comment:
            return
        for item in self.comment:
            """数据格式: 采集时间, 评论ID, 评论时间, UID, 用户昵称, IP归属地, 评论内容, 评论图片, 点赞数量, 回复数量, 回复ID"""
            collection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            create_time = time.strftime(
                self.time,
                time.localtime(
                    item["create_time"]))
            ip_label = item.get("ip_label") or "未知"
            text = item["text"][:self.max_comment]
            if images := item.get("image_list"):
                images = images[0]["origin_url"]["url_list"][-1]  # 图片链接
            else:
                images = ""
            if sticker := item.get("sticker"):
                sticker = sticker["static_url"]["url_list"][-1]  # 表情链接
            else:
                sticker = ""
            uid, sec_uid, short_id, unique_id, user_age, signature, nickname = self.get_author_data(
                item)
            digg_count = str(item["digg_count"])
            cid = item["cid"]
            reply_comment_total = item.get("reply_comment_total") or -1
            if reply_comment_total > 0:
                self.reply.append(cid)
            reply_id = item["reply_id"]
            result = [
                collection_time,
                cid,
                create_time,
                uid,
                sec_uid,
                short_id,
                unique_id,
                nickname,
                signature,
                str(user_age),
                ip_label,
                text,
                sticker,
                images,
                digg_count,
                str(reply_comment_total),
                reply_id]
            self.log.info("评论: " + ", ".join(result), False)
            self.data.save(result)

    @reset
    @check_cookie
    def run_mix(self, data: dict | str):
        info = self.get_mix_id(data) if isinstance(data, dict) else (data,)
        if not isinstance(info, tuple):
            return False
        while not self.finish:
            self.get_mix_data(info[0])
            self.deal_mix_data()
        if len(info) != 3:
            info = self.get_mix_id(self.mix_total[0])
        self.log.info("合集作品数据提取结束")
        # 如果合集名称去除非法字符后为空字符串，则使用当前时间戳作为合集标识
        return [
            info[0],
            self.clean.filter(
                info[1]) or str(
                time.time())[
                            :10],
            info[2]]

    @reset
    @check_cookie
    def run_mix_id(self, id_):
        pass

    def get_mix_id(self, data):
        nickname = self.clean.filter(data["author"]["nickname"])
        data = data.get("mix_info", False)
        return (data["mix_id"], data["mix_name"], nickname) if data else None

    @retry(finish=True)
    def get_mix_data(self, id_):
        """获取合集作品数据"""
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "mix_id": id_,
            "cursor": self.cursor,
            "count": "20",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
            "webid": self.__web,
        }
        self.deal_url_params(params)
        self.mix_data = []
        try:
            response = requests.get(
                self.mix_api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取合集作品数据超时")
            return False
        if response.content == b"":
            self.log.warning("合集作品数据响应内容为空")
            return False
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            self.log.error("合集作品数据返回内容异常！疑似接口失效", False)
            return False
        try:
            self.cursor = data['cursor']
            self.mix_data = data["aweme_list"]
            self.finish = not data["has_more"]
            return True
        except KeyError:
            self.log.error(f"合集作品数据内容异常: {data}", False)
            return False

    def deal_mix_data(self):
        for item in self.mix_data:
            self.mix_total.append(item)

    @reset
    @check_cookie
    def run_user(self):
        if not self.get_user_id():
            return False
        return self.deal_user(data) if (
            data := self.get_user_info()) else False

    @retry(finish=False)
    def get_user_info(self):
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "source": "channel_pc_web",
            "sec_user_id": self.id_,
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
            "webid": self.__web,
        }
        self.deal_url_params(params)
        try:
            response = requests.get(
                self.user_api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取账号数据超时")
            return False
        if response.content == b"":
            self.log.warning("账号数据响应内容为空")
            return False
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            self.log.error("账号数据内容异常！疑似接口失效", False)
            return False

    @staticmethod
    def deal_user(data):
        data = data["user"]
        collection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 采集时间
        avatar = data["avatar_larger"]["url_list"][0] or ""  # 头像链接
        cover = c[0]["url_list"][0] if (
            c := data.get("cover_url")) else ""  # 背景图片链接
        favoriting_count = data["favoriting_count"]  # 喜欢作品数量
        follower_count = data["follower_count"]  # 粉丝数量
        following_count = data["following_count"]  # 关注数量
        max_follower_count = data["max_follower_count"]  # 粉丝数量最大值
        city = data.get("city") or ""
        country = data.get("country") or ""
        # district = data.get("district") or ""
        # ip_location = data.get("ip_location") or ""
        signature = data.get("signature") or ""  # 简介
        total_favorited = data["total_favorited"]  # 获赞数量
        nickname = data.get("nickname") or "已注销账号"  # 账号昵称
        sec_uid = data["sec_uid"]
        unique_id = data["unique_id"]  # 抖音号
        short_id = data["short_id"]
        user_age = data["user_age"]  # 年龄
        aweme_count = data["aweme_count"]  # 作品数量
        # room_data = data.get("room_data")  # 直播数据
        custom_verify = data.get("custom_verify") or ""  # 标签认证
        uid = data["uid"]
        enterprise = data.get("enterprise_verify_reason") or ""  # 企业认证
        return [
            collection_time,
            nickname,
            signature,
            unique_id,
            str(user_age),
            country,
            city,
            # district,
            # ip_location,
            custom_verify,
            enterprise,
            sec_uid,
            uid,
            short_id,
            avatar,
            cover,
            str(aweme_count),
            str(total_favorited),
            str(favoriting_count),
            str(follower_count),
            str(following_count),
            str(max_follower_count), ]

    def save_user(self, file, data, batch=False):
        self.data = file
        if not batch:
            data = [data]
        for i in data:
            self.log.info("账号数据: " + ", ".join(i), False)
            self.data.save(i)
        self.log.info("账号数据已保存")

    @reset
    @check_cookie
    def run_search(
            self,
            keyword: str,
            type_: int,
            page: int,
            sort_type: int,
            publish_time: str):
        deal = {
            0: self.add_search_general,
            1: self.add_search_general,
            2: self.add_search_user,
        }
        self.log.info("开始获取搜索数据")
        api, first, channel, type_text = self.search_api[type_]
        self.headers["Referer"] = f"https://www.douyin.com/search/{quote(keyword)}?type={type_text}"
        for _ in range(page):
            if not self.get_search_data(
                    type_,
                    api,
                    first,
                    channel,
                    keyword,
                    sort_type,
                    publish_time):
                break
            deal[type_]()
        self.log.info("搜索数据获取结束")

    @retry(finish=False)
    def get_search_data(
            self,
            type_: int,
            api: str,
            first: int,
            channel: str,
            keyword: str,
            sort_type: int,
            publish_time: str):
        def user_params(metadata: dict):
            del metadata["sort_type"]
            del metadata["publish_time"]
            metadata["is_filter_search"] = 0

        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "search_channel": channel,
            "sort_type": sort_type,
            "publish_time": publish_time,
            "keyword": keyword,
            "search_source": "switch_tab",
            "is_filter_search": 0 if sort_type == 0 and publish_time == "0" else 1,
            "offset": self.cursor,
            "count": first if self.cursor == 0 else 10,
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
            "webid": self.__web,
        }
        if type_ == 2:
            user_params(params)
        self.deal_url_params(params)
        self.list = []
        try:
            response = requests.get(
                api,
                params=params,
                headers=self.headers,
                proxies=self.proxies,
                timeout=10)
            sleep()
        except requests.exceptions.ReadTimeout:
            self.log.error("获取搜索结果超时")
            return False
        except requests.exceptions.ConnectionError:
            self.log.error("获取搜索结果时网络异常")
            return False
        if response.content == b"":
            self.log.warning("搜索结果响应内容为空")
            return False
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            self.log.error("搜索结果返回内容异常！疑似接口失效", False)
            return False
        try:
            self.list = data["user_list"] if type_ == 2 else data["data"]
            self.cursor += params["count"]
            return True
        except KeyError:
            self.log.error(f"搜索结果响应内容异常: {data}", False)
            return False

    def add_search_general(self):
        for item in self.list:
            if data := item.get("aweme_info"):
                self.search_data.append(data)
            elif data := item.get("aweme_mix_info"):
                self.search_data.append(data["mix_items"][0])
            elif data := item.get("user_list"):
                for i in data[0]["items"]:
                    self.search_data.append(i)
            else:
                self.log.warning("搜索结果包含未知的JSON数据，请开启日志记录并告知作者处理")
                self.log.warning(f"不受支持的数据: {item}", False)

    def add_search_user(self):
        for item in self.list:
            self.search_data.append(item["user_info"])

    def deal_search_user(self) -> list[list]:
        result = []
        for item in self.search_data:
            collection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 采集时间
            uid = item.get('uid')
            short_id = item.get('short_id')
            nickname = item.get('nickname')
            signature = item.get('signature')
            avatar = item["avatar_thumb"]["url_list"][0]  # 搜索模式只能获取头像缩略图
            follower_count = item.get("follower_count") or 0
            total_favorited = item.get("total_favorited") or 0
            custom_verify = item.get("custom_verify")
            unique_id = item.get("unique_id")
            enterprise = item.get("enterprise_verify_reason")
            sec_uid = item.get("sec_uid")
            result.append([
                collection_time,
                uid,
                sec_uid,
                nickname,
                unique_id,
                short_id,
                avatar,
                signature,
                custom_verify,
                enterprise,
                str(follower_count),
                str(total_favorited),
            ])
        return result
