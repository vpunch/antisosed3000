from .config import Config

config = Config(
    CACHE_PAGE=1,
    TG_HOOK='foob',
    TG_TOKEN='foob',
    PAGE_SIZE=6,
    DB_NAME='data.db',
    CELERY_PAGE=2,
    CELERY_SCHEDULE=[60 * 15, 60 * 60 * 2],
    DEBUG=False
)
