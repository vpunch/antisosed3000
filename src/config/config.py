from dataclasses import dataclass, field


@dataclass(slots=True)
class Config:
    TG_HOOK: str
    TG_TOKEN: str
    DEBUG: bool
    TESTING: bool = False
    FLASK_HOST: str = 'localhost'
    FLASK_PORT: int = 5000
    TG_THREADED: bool = field(init=False)

    def __post_init__(self):
        self.TG_THREADED = not self.DEBUG
