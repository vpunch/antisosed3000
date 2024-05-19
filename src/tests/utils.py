def get_tg_mes(text: str):
    return {
        'update_id': 94721241,
        'message': {
            'message_id': 1121,
            'from': {
                'id': 228290426,
                'is_bot': False,
                'first_name': 'Ivan',
                'username': 'rot1t',
                'language_code': 'en'
            },
            'chat': {
                'id': 228290426,
                'first_name': 'Ivan',
                'username': 'rot1t',
                'type': 'private'
            },
            'date': 1682707096,
            'text': text,
        }
    }


def get_tg_cmd(name: str):
    message = get_tg_mes(f'/{name}')

    message['message']['entities'] = [
        {'offset': 0, 'length': len(name), 'type': 'bot_command'}
    ]

    return message
