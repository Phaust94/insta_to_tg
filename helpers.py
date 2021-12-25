from __future__ import annotations

import os
import typing
from dataclasses import dataclass

from instagrapi import Client
from instagrapi.types import Story
from telegram.ext import Updater
from telegram import Bot

from secrets import API_KEY, TG_TARGET


__all__ = [
    "StoryArchive",
    "Message",
    "MultiMessage"
]


class Botable:
    @property
    def bot(self) -> Bot:
        updater = Updater(API_KEY, workers=1)
        bot = updater.bot
        return bot


@dataclass
class Message(Botable):
    content_path: os.PathLike

    @property
    def path_str(self) -> str:
        return str(self.content_path)

    @property
    def content_type(self) -> str:
        return "photo" if self.path_str.endswith(".jpg") else "video"

    def send(self) -> None:
        bot = self.bot
        # noinspection PyBroadException
        try:
            meth = f"send_{self.content_type}"
            with open(self.content_path, "rb") as item:
                getattr(bot, meth)(TG_TARGET, item)
        except Exception:
            pass


@dataclass
class MultiMessage(Botable):
    user_name: str
    messages: typing.List[Message]

    def send(self) -> None:
        bot = self.bot
        msg = f"New stories from <b>{self.user_name}</b>"
        # noinspection PyBroadException
        try:
            bot.send_message(TG_TARGET, msg, parse_mode="HTML")
        except Exception:
            pass
        for message in self.messages:
            message.send()
        return None


@dataclass
class StoryArchive:
    username: str
    password: str
    targets: typing.Dict[int, str]
    folder: str
    pks: typing.Set[str]

    @classmethod
    def from_folder(
        cls, username: str, password: str,
        targets: typing.Dict[int, str],
        folder: str
    ) -> StoryArchive:

        pks = set()
        for f in os.listdir(folder):
            pk = ".".join(f.split(".")[:-1])
            if pk:
                pks.add(pk)

        inst = cls(username, password, targets, folder, pks)
        return inst

    def authenticate(self) -> Client:
        cl = Client()
        cl.login(self.username, self.password)
        return cl

    @staticmethod
    def filename(user_id: int, story: Story) -> str:
        # ext = "mp4" if story.video_duration > 0 else "jpg"
        res = f"{user_id}_{story.pk}"
        return res

    def update_from_remote(self) -> typing.List[MultiMessage]:
        cl = self.authenticate()
        messages = []
        for user_id, user_name in self.targets.items():
            stories = cl.user_stories(user_id)
            new_stuff = []
            for s in stories:
                fname = self.filename(user_id, s)
                if fname in self.pks:
                    continue
                url = s.thumbnail_url if s.media_type == 1 else s.video_url
                # noinspection PyTypeChecker
                new_path = cl.story_download_by_url(url, fname, self.folder)
                self.pks.add(fname)
                new_message = Message(new_path)
                new_stuff.append(new_message)

            msg = MultiMessage(user_name, new_stuff)
            messages.append(msg)

        return messages
