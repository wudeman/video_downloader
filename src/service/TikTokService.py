from src.DataAcquirer import UserData
from src.Parameter import XBogus
from src.Recorder import BaseLogger
from src.StringCleaner import colored_text
import requests
from src.CookieTool import Cookie


class TikTok:

    def __init__(self):
        self.id_ = None  # sec_uid or item_ids

        self.log = BaseLogger()
        self.xb = XBogus()
        self.request = None
        self.list = []  # 未处理的数据，循环时重置

    def account_download(self, cookie, proxies, mark, url, mode, earliest, latest):
        # 初始化请求模块
        self.init_request(cookie, proxies, mark, url, mode, earliest, latest)
        params = self.build_account_param()

        try:
            response = requests.get(
                self.request.api,
                params=params,
                headers=self.request.headers,
                proxies=self.request.proxies,
                timeout=10)
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
            else:
                self.list = list_

                self.log.info(list_)
            return True
        except KeyError:
            self.log.error(f"账号作品数据响应内容异常: {data}", False)
            return False

    def init_request(self, cookie, proxies, mark, url, mode, earliest, latest):
        self.request = UserData(self.log, self.xb)
        self.request.set_web_id()

        self.request.proxies = proxies
        self.request.cookie = cookie
        self.request.mark = mark
        self.request.url = url
        self.request.api = mode
        self.request.earliest = earliest
        self.request.latest = latest
        return True

    def build_account_param(self):
        """获取账号作品数据"""
        params = {
            "device_platform": "webapp",
            "aid": "6383",
            "channel": "channel_pc_web",
            "sec_user_id": self.request.get_user_id(True),
            "max_cursor": self.request.cursor,
            "count": "18",
            "cookie_enabled": "true",
            "platform": "PC",
            "downlink": "10",
            "webid": self.request.get_web_id(),
        }
        return params


if __name__ == '__main__':
    cookie = Cookie().get_cookie(
        cookie="ttwid=1%7C9zOlSUdlF30Sm3KyM15DgzXP0m3EJadZooiwCsyID54%7C1689741772%7Ce8940ba9833495b05a770c5baddb2982f4bb4bcba0c886ef08fc60873b53eed5; __bd_ticket_guard_local_probe=1689903032407; passport_csrf_token=87bdac3f4a275312c839cd9818982438; passport_csrf_token_default=87bdac3f4a275312c839cd9818982438; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEekNCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRTFZMTJnQ2NyK2l3d0gwTWNXeFlIaWNYV1xyXG5FZjZlRldvSzlqMWxXUmNGK1V4S0Y1Rk1MemNzR3VYVjFpTE5JODFuTjRiOGRRMGxIM0Z4MXBwd3YyaXVsNkFzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEU1FBd1JnSWhBTmZqc1pkVENOZ0hQa0E1MEJkVzBhaVlCZEF3OGxZK1pNUG5hSmcxQ2tqMVxyXG5BaUVBNFdyTEh6U29ldHJiM1dhTG1aOHRqczUwQmJKWWxzb1UydVI0aWEzOTNkWT1cclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; webcast_local_quality=null; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1690778867278%2C%22type%22%3Anull%7D; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; s_v_web_id=verify_lkge04x6_Guimx02A_QVus_4kbc_99sF_UkAQSgCYghyz; csrf_session_id=63d53a897d8aa9dc3f644e676daf51d0; download_guide=%223%2F20230724%2F0%22; pwa2=%220%7C0%7C3%7C0%22; n_mh=yH2oFGdcjLiDdSrnzgmngTOPSEHwuPSkHB6Prf5Jj64; LOGIN_STATUS=1; store-region=cn-gd; store-region-src=uid; __security_server_data_status=1; __ac_nonce=064c3581e005a5bf78502; __ac_signature=_02B4Z6wo00f01meVxxQAAIDDBJ8HfwDL9M5ntcOAAP01se81Nlm5SU9o69YoOz9H982dxFRDXhBt41d2FVn66pDyh0r1yHKsfhGelkgqO00f6oGAXJIRwccUO.elQMKDy8bQePV3nDW0622t6e; strategyABtestKey=%221690523690.447%22; passport_assist_user=CkG-CHkLbQKMb7pxXjfJ5h5yQCljTEbqeckpb-ag9xgYCPJY1cvBi-HQPgp8FnLnX7RQYwUNJNzkGhtD7_HHQCwhdhpICjzSQfFVye8HpXRyoOQXKO-CzfUMAADPRRO5C57ZOSdhfokfuuOaFp9laVoRgdBCTTwG7BsAMGfkJat5v1wQ4Na3DRiJr9ZUIgEDfb25WQ%3D%3D; sso_uid_tt=ca54e0cafbd614a448f4f752434a07d8; sso_uid_tt_ss=ca54e0cafbd614a448f4f752434a07d8; toutiao_sso_user=dbbc96e882d6a42ac8468c260bd42ebd; toutiao_sso_user_ss=dbbc96e882d6a42ac8468c260bd42ebd; sid_ucp_sso_v1=1.0.0-KGIxMGE2NTE3ZjY0ZmRhMDk4N2Q3MzI2Y2E2NDRmODZjMGYwZWQ0ODcKHwjd-eD_qo3GAxDKsI2mBhjvMSAMMP7_q40GOAZA9AcaAmxxIiBkYmJjOTZlODgyZDZhNDJhYzg0NjhjMjYwYmQ0MmViZA; ssid_ucp_sso_v1=1.0.0-KGIxMGE2NTE3ZjY0ZmRhMDk4N2Q3MzI2Y2E2NDRmODZjMGYwZWQ0ODcKHwjd-eD_qo3GAxDKsI2mBhjvMSAMMP7_q40GOAZA9AcaAmxxIiBkYmJjOTZlODgyZDZhNDJhYzg0NjhjMjYwYmQ0MmViZA; odin_tt=49ca00e3dc7c795cd3cddd51aa052e717c8e7b07aa0a8b3c54b7d08a894c59e69719a34eab1d45d104555ff79272e26d190070b2381b6fe4bed2274d60da290a; passport_auth_status=3a2b6b4cca1ecec15781e3664114e135%2C6fc73e27111e4aa06d93cef9aa526116; passport_auth_status_ss=3a2b6b4cca1ecec15781e3664114e135%2C6fc73e27111e4aa06d93cef9aa526116; uid_tt=f15e027b81ff53d305a4e18863bd0e3d; uid_tt_ss=f15e027b81ff53d305a4e18863bd0e3d; sid_tt=4a409bce635a27ed6f4160a5a5a7a5ef; sessionid=4a409bce635a27ed6f4160a5a5a7a5ef; sessionid_ss=4a409bce635a27ed6f4160a5a5a7a5ef; sid_guard=4a409bce635a27ed6f4160a5a5a7a5ef%7C1690523731%7C5183994%7CTue%2C+26-Sep-2023+05%3A55%3A25+GMT; sid_ucp_v1=1.0.0-KGZlNjA5NDQ0MTBjYzMxMDUzOWI4YzUxMjJiYjJkYWNjOTIyYTRlOGMKGwjd-eD_qo3GAxDTsI2mBhjvMSAMOAZA9AdIBBoCaGwiIDRhNDA5YmNlNjM1YTI3ZWQ2ZjQxNjBhNWE1YTdhNWVm; ssid_ucp_v1=1.0.0-KGZlNjA5NDQ0MTBjYzMxMDUzOWI4YzUxMjJiYjJkYWNjOTIyYTRlOGMKGwjd-eD_qo3GAxDTsI2mBhjvMSAMOAZA9AdIBBoCaGwiIDRhNDA5YmNlNjM1YTI3ZWQ2ZjQxNjBhNWE1YTdhNWVm; _bd_ticket_crypt_cookie=07b5722ef65f0da43599fa4cf90b5d60; tt_scid=zrHwwgrN7NJ-MgOcgqFXEvA6bVjZyGKgsBh4Z6c1sOhqNv5S5badhb3kkjcdN6Mk17fd; my_rd=1; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAATV40uPeRacdIHwI-ecJ3AnN5JlGkWpmPQiYyyk-d72-ilxkCZ2Hv9QHxsV--MqOr%2F1690560000000%2F0%2F1690523758742%2F0%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.35%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A450%7D%22; home_can_add_dy_2_desktop=%221%22; msToken=db8VcguHWi5cgx2ZEahNLgQbPUjiAzPJVYcuvYvMqw7xL2n8aM0-DattIHZYvU0Rmsp1dy84PZM-bJwY5gpXFk8_8BxPC1jU-qXGXC_sLKT0tUPkV5awWuUl4gu2WdU=; passport_fe_beating_status=true; msToken=NwwXqKo6mBVP6jWragwwClL6SZi_ZNZX5rSBHDKp-C38N10N6-fWz51Pzb3mwEcbXetTSB0eNqI9-6iZENKZZNfg80AiVr-PE0bpgOQPyFhO3-IMZMmstTJ361oT7ZU=; publish_badge_show_info=%220%2C0%2C0%2C1690523773743%22")

    TikTok().account_download(cookie, "127.0.0.1:15732", "",
                              "https://www.douyin.com/user/MS4wLjABAAAA3xgdieikm--yugm6aHJ9BcFfYoSqgWZVkL9KzzRRoRs?vid=7259390496286461240",
                              "post", "2023/7/25", "2023/7/27")
