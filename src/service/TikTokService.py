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
        self.request = None;

    def account_download(self, cookie, proxies, mark, url, mode, earliest, latest):
        # 初始化请求模块
        self.init_request(cookie, proxies, mark, url, mode, earliest, latest)

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

        response = requests.get(
            self.request.api,
            params=params,
            headers=self.request.headers,
            proxies=self.request.proxies,
            timeout=10)

        self.log.info(response)

        return True

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


if __name__ == '__main__':
    cookie = Cookie().get_cookie(
        cookie="ttwid=1%7C9zOlSUdlF30Sm3KyM15DgzXP0m3EJadZooiwCsyID54%7C1689741772%7Ce8940ba9833495b05a770c5baddb2982f4bb4bcba0c886ef08fc60873b53eed5; __bd_ticket_guard_local_probe=1689903032407; passport_csrf_token=87bdac3f4a275312c839cd9818982438; passport_csrf_token_default=87bdac3f4a275312c839cd9818982438; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtY2xpZW50LWNzciI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbk1JSUJEekNCdFFJQkFEQW5NUXN3Q1FZRFZRUUdFd0pEVGpFWU1CWUdBMVVFQXd3UFltUmZkR2xqYTJWMFgyZDFcclxuWVhKa01Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRTFZMTJnQ2NyK2l3d0gwTWNXeFlIaWNYV1xyXG5FZjZlRldvSzlqMWxXUmNGK1V4S0Y1Rk1MemNzR3VYVjFpTE5JODFuTjRiOGRRMGxIM0Z4MXBwd3YyaXVsNkFzXHJcbk1Db0dDU3FHU0liM0RRRUpEakVkTUJzd0dRWURWUjBSQkJJd0VJSU9kM2QzTG1SdmRYbHBiaTVqYjIwd0NnWUlcclxuS29aSXpqMEVBd0lEU1FBd1JnSWhBTmZqc1pkVENOZ0hQa0E1MEJkVzBhaVlCZEF3OGxZK1pNUG5hSmcxQ2tqMVxyXG5BaUVBNFdyTEh6U29ldHJiM1dhTG1aOHRqczUwQmJKWWxzb1UydVI0aWEzOTNkWT1cclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; ttcid=69f12d4093a44289af9107d5593e65a412; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; webcast_local_quality=null; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1690778867278%2C%22type%22%3Anull%7D; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; s_v_web_id=verify_lkge04x6_Guimx02A_QVus_4kbc_99sF_UkAQSgCYghyz; csrf_session_id=63d53a897d8aa9dc3f644e676daf51d0; download_guide=%223%2F20230724%2F0%22; pwa2=%220%7C0%7C3%7C0%22; __ac_nonce=064c243dd00e5e2e16377; __ac_signature=_02B4Z6wo00f01qae1jQAAIDDxZQWXUQ1.cqmvtKAAM1y7kwjf8UEOK9Ox7Dm6HnCtxJoqFQiYRYQc4BAcQIhNe-hsWR3zuC6OD2bOJAiESNlIQYZdHKMBxJAeH1k9Y3PgotsDwnICR.QzivWd8; strategyABtestKey=%221690452963.29%22; n_mh=yH2oFGdcjLiDdSrnzgmngTOPSEHwuPSkHB6Prf5Jj64; sso_uid_tt=28f9491c4994a3ed451ce6560ca1a5ba; sso_uid_tt_ss=28f9491c4994a3ed451ce6560ca1a5ba; toutiao_sso_user=ffc830df148fe8fffa74ca9056900aa0; toutiao_sso_user_ss=ffc830df148fe8fffa74ca9056900aa0; passport_auth_status=6fc73e27111e4aa06d93cef9aa526116%2C; passport_auth_status_ss=6fc73e27111e4aa06d93cef9aa526116%2C; uid_tt=602f5f0080515e6aaea150cad5f56584; uid_tt_ss=602f5f0080515e6aaea150cad5f56584; sid_tt=43a47f5834173b90d2e608a7ba7d5728; sessionid=43a47f5834173b90d2e608a7ba7d5728; sessionid_ss=43a47f5834173b90d2e608a7ba7d5728; odin_tt=53062daa5d93eda3e845282131d515bf89b16956c0e8c25a844f155b7641bb3ddddea2fc9d286345ed967d9f0b507d0d3035f163313024db9c14bcebccc6559f; passport_assist_user=CkFMK8b3saXFcDH5wPIELtAzVIC11lpsWwJe0UamGoIfXGQCRJsQOF8bWP9k1YGXh8K7nGIFAAhkZH3ZlIbHgC5UtBpICjzuiCWtaqhsWxC2w9kLcmPXxzDENfDce6bgnCW1PSeL7M2X_yZtajbMkBlPgBeT4rv_iWVo2g9sqTvLwNEQqM63DRiJr9ZUIgEDWHVBFA%3D%3D; sid_ucp_sso_v1=1.0.0-KDNjMGFjOWI4NWJiYjFkNmZlNDE4NTM4MWRiM2ViZjdlMDNhOGU1NDQKHwjd-eD_qo3GAxCXiImmBhjvMSAMMP7_q40GOAZA9AcaAmxxIiBmZmM4MzBkZjE0OGZlOGZmZmE3NGNhOTA1NjkwMGFhMA; ssid_ucp_sso_v1=1.0.0-KDNjMGFjOWI4NWJiYjFkNmZlNDE4NTM4MWRiM2ViZjdlMDNhOGU1NDQKHwjd-eD_qo3GAxCXiImmBhjvMSAMMP7_q40GOAZA9AcaAmxxIiBmZmM4MzBkZjE0OGZlOGZmZmE3NGNhOTA1NjkwMGFhMA; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAATV40uPeRacdIHwI-ecJ3AnN5JlGkWpmPQiYyyk-d72-ilxkCZ2Hv9QHxsV--MqOr%2F1690473600000%2F0%2F1690453018323%2F0%22; LOGIN_STATUS=1; passport_fe_beating_status=true; store-region=cn-gd; store-region-src=uid; sid_guard=43a47f5834173b90d2e608a7ba7d5728%7C1690453020%7C5183995%7CMon%2C+25-Sep-2023+10%3A16%3A55+GMT; sid_ucp_v1=1.0.0-KGM1MjM4YWMxODA4OWMzNmVkZTc1MDllMTEwNWRhZTQzOWVmOTc2OGQKGwjd-eD_qo3GAxCciImmBhjvMSAMOAZA9AdIBBoCbGYiIDQzYTQ3ZjU4MzQxNzNiOTBkMmU2MDhhN2JhN2Q1NzI4; ssid_ucp_v1=1.0.0-KGM1MjM4YWMxODA4OWMzNmVkZTc1MDllMTEwNWRhZTQzOWVmOTc2OGQKGwjd-eD_qo3GAxCciImmBhjvMSAMOAZA9AdIBBoCbGYiIDQzYTQ3ZjU4MzQxNzNiOTBkMmU2MDhhN2JhN2Q1NzI4; _bd_ticket_crypt_cookie=19ea42c82369245ebd6e33bdbffb430a; __security_server_data_status=1; tt_scid=WVbqqZFUE9lJV6QoXNfopgT0lJi9UzzZzPZSsZV0GEPsr7BqcG7gMaTSvxzfI5MN88dc; msToken=cT2-cwW2YPfS_J6UJuNANL9Fq3zTQroepv7HX9_4hFQgchEe4ol9BldcNT_pcDXlXcYBtjj-l8W9BYqxko_HUcCwjt-Yp1EhhKSg6DBTkRnWzpjSGh2--ImniUbFTFA=; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.55%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A400%7D%22; msToken=B2cbBVY6ZfQU5V3ejYv6QFldQ74kmkIdkhep-shQli3GdMov0hgVT-TRLCqFnhk3lYGUOrqDQr9ZI26k_x7APgcDkfevxlDvCJMSFK00BQ4lu7a7UST45PoY7xHvDw==; home_can_add_dy_2_desktop=%221%22; publish_badge_show_info=%220%2C0%2C0%2C1690453048374%22")

    TikTok().account_download(cookie, "127.0.0.1:15732", "",
                              "https://www.douyin.com/user/MS4wLjABAAAA3xgdieikm--yugm6aHJ9BcFfYoSqgWZVkL9KzzRRoRs?vid=7259390496286461240",
                              "post", "2023/7/25", "2023/7/27")
