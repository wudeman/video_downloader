from time import time

from src.Configuration import Settings
from src.DataAcquirer import UserData
from src.DataDownloader import Download
from src.FileManager import Cache
from src.Parameter import XBogus
from src.Recorder import BaseLogger
from src.Recorder import LoggerManager
from src.Recorder import RecordManager
from src.StringCleaner import colored_text


def prompt(tip: str, choose: tuple | list, start=1) -> str:
    screen = colored_text(f"{tip}:\n", 96)
    for i, j in enumerate(choose):
        screen += colored_text(f"{i + start}. {j}\n", 92)
    return input(screen)


class TikTok:

    def __init__(self):
        self.logger = BaseLogger()
        self.xb = XBogus()
        self.request = UserData(self.logger, self.xb)

    def account_download(
            self,
            num: int,
            mark: str,
            url: str,
            mode: str,
            earliest: str,
            latest: str, save, root: str, params: dict):
        self.request.mark = mark
        self.request.url = url
        self.request.api = mode
        self.request.earliest = earliest
        self.request.latest = latest
        if not self.request.run(f"第 {num} 个"):
            return False
        old_mark = m["mark"] if (
            m := self.manager.cache.get(
                self.request.uid.lstrip("UID"))) else None
        self.manager.update_cache(
            self.request.uid.lstrip("UID"),
            self.request.mark,
            self.request.name)
        self.download.nickname = self.request.name
        self.download.uid = self.request.uid
        self.download.mark = self.request.mark
        self.download.favorite = self.request.favorite
        with save(root, name=f"{self.download.uid}_{self.download.mark}", old=old_mark, **params) as data:
            self.download.data = data
            self.download.run(f"第 {num} 个",
                              self.request.video_data,
                              self.request.image_data)
        return True
