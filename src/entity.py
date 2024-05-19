from pydantic import BaseModel, ValidationError
import requests
from requests.exceptions import JSONDecodeError

import text
import utils

EntityId = tuple[str, ...]


class Entity(BaseModel):
    id: EntityId
    name: str


class ExtdEntity(Entity):
    ticket_count: int


EntityMap = dict[EntityId, Entity]


class Entities:
    id: EntityId
    _path: str

    __slots__ = ('_logger', 'id', '_path')

    _cache: dict[EntityId, EntityMap | None] = {}

    def __init__(self) -> None:
        self._logger = utils.get_logger(__name__)(self.__class__.__name__)

    def _fetch(self) -> dict | None:
        self._logger.debug('Updating entities data') 

        response = requests.get(
                f'https://gorzdrav.spb.ru/_api/api/v2{self._path}')

        if response.status_code != 200:
            self._logger.error('API response is not ok')
            return None

        try:
            return response.json()
        except JSONDecodeError:
            self._logger.error('API uses invalid return type')
            return None

    def _convert_item(self, item: dict) -> Entity:
        raise NotImplementedError

    def _convert(self, response: dict) -> EntityMap:
        result = {}

        for item in response['result']:
            item = self._convert_item(item)
            result[item.id] = item

        return result

    def get(self, check_cache: bool = True) -> EntityMap | None:
        if check_cache:
            cache = self._cache.get(self.id)
        else:
            cache = None

        if cache is None:
            response = self._fetch()

            try:
                entities = self._convert(response)  # type: ignore[arg-type]
            except (KeyError, ValidationError, TypeError):
                self._logger.exception('Invalid response structure')
                entities = None

            self._cache[self.id] = entities

        return self._cache[self.id]

    def get_list(self) -> list[Entity] | None:
        if result := self.get():
            return list(result.values())

        return None


class Districts(Entities):
    __slots__ = ()

    char = 'd'
    header = text.DISTR_HEADER

    def __init__(self):
        super().__init__()
        self.id = ('districts',)
        self._path = '/shared/districts'

    def _convert_item(self, item: dict) -> Entity:
        return Entity(id=(item['id'],), name=item['name'])


class Hospitals(Entities):
    __slots__ = ()

    char = 'h'
    header = text.HOSP_HEADER

    def __init__(self, distr_id: str):
        super().__init__()
        self.id = (distr_id,)
        self._path = f'/shared/district/{distr_id}/lpus'

    def _convert_item(self, item: dict) -> Entity:
        return Entity(
                id=self.id + (str(item['id']),), name=item['lpuFullName'])


class Specials(Entities):
    __slots__ = ()

    char = 's'
    header = text.SPECIAL_HEADER

    def __init__(self, distr_id: str, hosp_id: str):
        super().__init__()
        self.id = (distr_id, hosp_id)
        self._path = f'/schedule/lpu/{hosp_id}/specialties'

    def _convert_item(self, item: dict) -> ExtdEntity:
        return ExtdEntity(
            id=self.id + (item['id'],),
            name=item['name'],
            ticket_count=item['countFreeTicket']
        )


class Medics(Entities):
    __slots__ = ()

    char = 'm'
    header = text.MEDIC_HEADER

    def __init__(self, distr_id: str, hosp_id: str, special_id: str) -> None:
        super().__init__()
        self.id = (distr_id, hosp_id, special_id)
        self._path = f'/schedule/lpu/{hosp_id}/speciality/{special_id}/doctors'

    def _convert_item(self, item: dict) -> ExtdEntity:
        return ExtdEntity(
            id=self.id + (item['id'],),
            name=item['name'],
            ticket_count=item['freeParticipantCount']
        )


SpecEntities = type[Districts | Hospitals | Specials | Medics]
