from typing import Literal, Final
import logging
import sys

from flask import Flask, request
from telebot.types import Update

from tg.handlers import TG
import text
from utils import with_logger, get_logger

_LOGGER: Final = get_logger()()


def _create_logger(app: Flask) -> None:
    formatter = logging.Formatter('%(name)s | %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger = logging.getLogger('main')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if app.config['DEBUG'] else logging.INFO)


def handle_tg(tg_token: str) -> Literal['']:
    body = request.json
    _LOGGER.debug(body)
    update = Update.de_json(body)
    TG.process_new_updates([update])

    return ''





def create_app(conf_name: str) -> Flask:
    app = Flask(__name__)

    app.config.from_object(f'config.{conf_name}.config')
    app.config['TG_COMMANDS'] = text.COMMANDS

    TG.init_app(app)

    app.post('/<tg_token>')(handle_tg)


    return app


if __name__ == '__main__':
    conf_name = sys.argv[1]
    app = create_app(conf_name)

    _create_logger(app)

    app.run(
        host=app.config['FLASK_HOST'],
        port=app.config['FLASK_PORT'],
        use_reloader=False
    )
