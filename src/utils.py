from typing import Callable, Sequence, overload
import logging
from functools import wraps

from pydantic import BaseModel


GetModLogger = Callable[..., logging.Logger]


class ObsData(BaseModel):
    id: int
    usr_id: int
    with_medic: bool




def get_logger(module: str | None = None) -> GetModLogger:
    def get_mod_logger(*entities: str) -> logging.Logger:
        return logging.getLogger(
                '.'.join(filter(None, ('main', module) + entities)))

    return get_mod_logger


def with_logger(get_mod_logger: GetModLogger):
    def decorator(func: Callable):
        logger = get_mod_logger(func.__name__)

        @wraps(func)
        def func_(*args, **kwargs):
            return func(logger, *args, **kwargs)

        return func_

    return decorator
