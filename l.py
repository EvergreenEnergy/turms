import strawberry
from enum import Enum
from typing import List, Any, Optional, Union
from strawberry.schema_directive import Location

@strawberry.schema_directive(locations=[Location.OBJECT, Location.INTERFACE])
class key:
    fields: str

@strawberry.schema_directive(locations=[Location.OBJECT, Location.INTERFACE])
class extends:
    pass

@strawberry.schema_directive(locations=[Location.OBJECT, Location.FIELD_DEFINITION])
class external:
    pass

@strawberry.schema_directive(locations=[Location.FIELD_DEFINITION])
class requires:
    fields: str

@strawberry.schema_directive(locations=[Location.FIELD_DEFINITION])
class provides:
    fields: str

@strawberry.input
class StringQueryOperatorInput:
    eq: Optional[str]
    ne: Optional[str]
    in_: Optional[List[Optional[str]]]
    nin: Optional[List[Optional[str]]]
    regex: Optional[str]
    glob: Optional[str]

@strawberry.input
class CountryFilterInput:
    code: Optional[StringQueryOperatorInput]
    currency: Optional[StringQueryOperatorInput]
    continent: Optional[StringQueryOperatorInput]

@strawberry.input
class ContinentFilterInput:
    code: Optional[StringQueryOperatorInput]

@strawberry.input
class LanguageFilterInput:
    code: Optional[StringQueryOperatorInput]

@strawberry.type
class Country:
    code: str
    name: str
    native: str
    phone: str
    continent: 'Continent'
    capital: Optional[str]
    currency: Optional[str]
    languages: List['Language']
    emoji: str
    emoji_u: str
    states: List['State']

@strawberry.type
class Continent:
    code: str
    name: str
    countries: List[Country]

@strawberry.type
class Language:
    code: str
    name: Optional[str]
    native: Optional[str]
    rtl: bool

@strawberry.type
class State:
    code: Optional[str]
    name: str
    country: Country

@strawberry.type
class Query:

    @strawberry.field()
    def _entities(self, representations: List[Any]) -> List[Optional[Union[Country, Continent, Language]]]:
        return None

    @strawberry.field()
    def _service(self) -> '_Service':
        return None

    @strawberry.field()
    def countries(self, filter: Optional[CountryFilterInput]) -> List[Country]:
        return None

    @strawberry.field()
    def country(self, code: str) -> Optional[Country]:
        return None

    @strawberry.field()
    def continents(self, filter: Optional[ContinentFilterInput]) -> List[Continent]:
        return None

    @strawberry.field()
    def continent(self, code: str) -> Optional[Continent]:
        return None

    @strawberry.field()
    def languages(self, filter: Optional[LanguageFilterInput]) -> List[Language]:
        return None

    @strawberry.field()
    def language(self, code: str) -> Optional[Language]:
        return None

@strawberry.type
class _Service:
    sdl: Optional[str] = strawberry.field(description='The sdl representing the federated service capabilities. Includes federation directives, removes federation types, and includes rest of full schema after schema directives have been applied')