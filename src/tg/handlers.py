from typing import Final

from telebot.types import Message
from flask_tghandler import TgHandler

from utils import get_logger

import subprocess

_get_mod_logger = get_logger(__name__)
_LOGGER: Final = _get_mod_logger()

TG: Final = TgHandler()

process = None


@TG.message_handler(commands=["start"])
def send_info(_, message: Message) -> None:
    # kill browser
    # kill telegram
    # volume control mute all
    global process
    process = subprocess.Popen("mpv /home/vanya/Downloads/foobar.mp4", shell=True)

    TG.answer("Ok")


@TG.message_handler(commands="stop")
def send_page(_, message: Message) -> None:
    process.kill()

    TG.answer("Ok")


@TG.message_handler(commands="status")

