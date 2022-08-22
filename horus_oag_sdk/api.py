from __future__ import annotations

from typing import List, Dict, Union
from dataclasses import dataclass, field


@dataclass
class Param:
    type: str
    format: str
    description: str = ""

    _meta: dict = field(default_factory=dict)


@dataclass
class ParamInt(Param):
    minimum: int = -65535
    maximum: int = 65535
    ...


@dataclass
class ParamFloat(Param):
    ...


@dataclass
class ParamBoolean(Param):
    ...


@dataclass
class ParamString(Param):
    ...


InputType: ParamInt | ParamBoolean | ParamString | ParamFloat

Schema: Union[
    Dict[str, InputType | Param],
    List[InputType | Param],
    InputType | Param
]


@dataclass
class Body:
    params: Union[
        Dict[str, InputType | Param],
        List[InputType | Param],
        InputType | Param
    ]

    _meta: dict = field(default_factory=dict)


@dataclass
class Response:
    status_code: int
    body: Schema = None
    headers: List[Dict[str, InputType]] = field(default_factory=list)

    _meta: dict = field(default_factory=dict)


@dataclass
class Request:
    response: Response
    body: Schema = None

    headers: Dict[str, InputType] = field(default_factory=dict)
    query_params: Dict[str, InputType] = field(default_factory=dict)

    _meta: dict = field(default_factory=dict)


@dataclass
class Path:
    path: str
    method: str
    request: List[Request]

    _meta: dict = field(default_factory=dict)


@dataclass
class API:
    host: str
    paths: list[Path] = field(default_factory=list)
    extensions: dict = field(default_factory=dict)

    _meta: dict = field(default_factory=dict)


"""
API EXAMPLE:

/api/v1/users/{userId}/books/{bookId} GET [1]
    /api/v1/users/{userId}/books/{bookId}?q=juan
        R1
    /api/v1/users/{userId}/books/{bookId}?q=bolsos
        R2
    /api/v1/users/{userId}/books/{bookId}?q=zapatos
        R3

/api/v1/users/{userId}/books/{bookId} POST [2]
"""

"""
INPUT (STEP 1):
   input:
   - oas v3 (seed or baseline) 
   - n http calls (n>0)
   - metadata stored in the db used by the plugins (optional)

   methods:
    - from http to api (transform response, request body to schema)
    - from oas_v3_0 to api (transform all but schemas)

 WORK (STEP 2):
    ...

 OUTPUT (STEP 3):
  output:
  - from api to oasV3 + metadata  
"""

"""
    (step 2.1):
    for path in API:
        for method in path:
            p: Tuple[str, Request]

            similares = get_similares(p) # obtener todas las request que son iguales


    methods (step 2.2):
     add examples
     add regex

    methods (step 3):
    - from api to oasV3 + metadata
            for similar in similares:
                new_p = merge(similar) # mergea todas las request iguales
"""

__all__ = ("API", "Path", "Request", "Response", "Body", "Schema", "Param",
           "ParamInt", "ParamFloat", "ParamBoolean", "ParamString")
