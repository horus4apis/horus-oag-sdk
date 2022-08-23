from __future__ import annotations

import sys
import hashlib

from abc import ABCMeta, abstractmethod

from typing import List, Dict, Union, NewType, Set, Iterable
from dataclasses import dataclass, field

def do_hash(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")

    return hashlib.sha256(data).hexdigest()

class Hashable(metaclass=ABCMeta):

    @abstractmethod
    def hash(self) -> str:
        raise NotImplementedError()

@dataclass
class Param(Hashable):
    type: str
    format: str
    regex: str = "*"
    description: str = ""

    _meta: dict = field(default_factory=dict)

@dataclass
class ParamInt(Param):
    minimum: int = -sys.maxsize
    maximum: int = sys.maxsize


@dataclass
class ParamFloat(Param):
    ...


@dataclass
class ParamBoolean(Param):
    ...


@dataclass
class ParamString(Param):
    ...


# InputType: NewType("InputType", ParamInt | ParamBoolean | ParamString | ParamFloat)
InputType: ParamInt | ParamBoolean | ParamString | ParamFloat

# Schema: NewType("Schema", Union[
#     Dict[str, InputType | Param],
#     List[InputType | Param],
#     InputType | Param
# ])
Schema: Union[
    Dict[str, InputType | Param],
    List[InputType | Param],
    InputType | Param
]


@dataclass
class Body(Hashable):
    params: Union[
        Dict[str, InputType | Param],
        List[InputType | Param],
        InputType | Param
    ]

    _meta: dict = field(default_factory=dict)

    def hash(self) -> str:
        return "body hash"

@dataclass
class Response(Hashable):
    status_code: int
    body: Schema = None
    headers: List[Dict[str, InputType]] = field(default_factory=list)

    _meta: dict = field(default_factory=dict)

    def hash(self) -> str:
        if self.body:
            body_hash = self.body.hash()
        else:
            body_hash = ""

        if self.headers:
            headers_hash = do_hash(str(self.headers))
        else:
            headers_hash = ""

        return do_hash(
            f"{self.status_code}#{body_hash}#{headers_hash}"
        )

@dataclass
class Request(Hashable):
    response: Response
    body: Schema = None

    headers: Dict[str, InputType] = field(default_factory=dict)
    query_params: Dict[str, InputType] = field(default_factory=dict)

    _meta: dict = field(default_factory=dict)

    def hash(self) -> str:
        if self.body:
            body_hash = self.body.hash()
        else:
            body_hash = ""

        if self.headers:
            headers_hash = do_hash(str(self.headers))
        else:
            headers_hash = ""

        if self.query_params:
            query_params_hash = do_hash(str(self.query_params))
        else:
            query_params_hash = ""

        return do_hash(f"{body_hash}#{headers_hash}#{query_params_hash}#{self.response.hash()}")

    def __eq__(self, other):
        return self.hash() == other.hash()

@dataclass
class Path(Hashable):
    path: str
    method: str
    request: List[Request]

    _meta: dict = field(default_factory=dict)

    def find_request(self, request: Request) -> Request:
        for req in self.request:
            if request == req:
                return req

    def hash(self) -> str:
        return do_hash(f"{self.path}_{self.method}")

@dataclass
class API(Hashable):
    hosts: Set[str] = field(default_factory=set)
    paths: list[Path] = field(default_factory=list)

    _meta: dict = field(default_factory=dict)

    def add_host(self, host: str | Iterable[str]):
        if hasattr(host, "__iter__"):
            self.hosts.update(host)
        else:
            self.hosts.add(host)

    def add_path(self, path: Path):
        self.paths.append(path)

    def find_path(self, path: str, method: str) -> Path:
        for p in self.paths:
            if p.path == path and p.method == method:
                return p

        return None

    def hash(self) -> str:
        return do_hash(f"{self.hosts}#{self.paths}")

current_api = API()

__all__ = ("API", "Path", "Request", "Response", "Body", "Param",
           "ParamInt", "ParamFloat", "ParamBoolean", "ParamString",
           "current_api")
