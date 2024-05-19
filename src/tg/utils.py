from typing import Final
from math import ceil
from datetime import timedelta
from hashlib import blake2b

from flask import current_app
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from entity import SpecEntities, EntityId, Medics, Specials
import text as text_

SEND_PAGE_CODE: Final = text_.COMMANDS[2][0]
REG_OBS_CODE: Final = 'ro'
DEL_OBS_CODE: Final = 'do'
_EID_PREFIX: Final = 'eid'


def encode_id(id_: EntityId) -> str:
    return ':'.join(id_)


def decode_id(id_: str) -> EntityId:
    if not id_:
        return ()

    return tuple(id_.split(':'))


def hide_id(id_: EntityId) -> str:
    eid = encode_id(id_)
    hid = blake2b(eid.encode(), digest_size=8).hexdigest()
    current_app.extensions['cache'].set(
            f'{_EID_PREFIX}:{hid}', eid, timedelta(days=7))
    return hid


def decode_hid(id_: str) -> EntityId | None:
    if id_:
        value = current_app.extensions['cache'].get(f'{_EID_PREFIX}:{id_}')

        if value is None:
            return value

        id_ = value

    return decode_id(id_)


def get_page_text(cls: SpecEntities,
                  entities_id: EntityId,
                  num: int) -> tuple[str, bool | None]:
    entities = cls(*entities_id).get_list()

    if not entities:
        return text_.ERROR, None

    size = current_app.config['PAGE_SIZE']
    start = size * num
    end = start + size
    num_last = ceil(len(entities) / size) - 1

    header = f'<b>{cls.header}</b>'

    if num_last:
        header += ' ' + text_.PAGE_POS.format(num + 1, num_last + 1)

    text_items = [header]

    for entity in entities[start:end]:
        hid = hide_id(entity.id)
        items = [entity.name]

        if cls != Medics:
            items.append(
                    f'<i>{text_.ENTITY_OPEN}</i>: /{SEND_PAGE_CODE}_{hid}')

        if cls in [Specials, Medics]:
            items.append(
                    f'<i>{text_.ENTITY_OBS}</i>: /{REG_OBS_CODE}_{hid}')

        text_items.append('\n'.join(items))

    return '\n\n'.join(text_items), num_last == num


def get_page_markup(cls: SpecEntities,
                    entities_id: str,
                    page_num: int,
                    is_last: bool | None) -> InlineKeyboardMarkup:
    if is_last is None:
        return None

    buttons: list[InlineKeyboardButton] = []

    def add_button(name: str, page_num: int) -> None:
        buttons.append(InlineKeyboardButton(
            name,
            # Лучше использовать хэшированный ID, чтобы не было
            # переполнения
            callback_data=f'cp{cls.char}{page_num}:{entities_id}'
        ))

    if page_num:
        add_button('<', page_num - 1)

    if not is_last:
        add_button('>', page_num + 1)

    return InlineKeyboardMarkup([buttons])
