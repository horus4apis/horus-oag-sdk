from __future__ import annotations

import sys
import hashlib

from collections import OrderedDict
from abc import ABCMeta, abstractmethod

from dataclasses import dataclass, field
from typing import List, Dict, Union, Set, Iterable

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
    description: str = ""

    _meta: dict = field(default_factory=dict)

@dataclass
class ParamInt(Param):
    minimum: int = -sys.maxsize
    maximum: int = sys.maxsize

@dataclass
class ParamFloat(Param):
    minimum: int = -float(sys.maxsize)
    maximum: int = float(sys.maxsize)

@dataclass
class ParamBoolean(Param):
    ...


@dataclass
class ParamString(Param):
    pattern: str = '*'
    min_length: int = 0
    max_length: int = sys.maxsize

InputType: ParamInt | ParamBoolean | ParamString | ParamFloat

Schema: Union[
    Dict[str, Schema],
    List[Schema],
    Schema,
    InputType
]

@dataclass
class BodyTypes:
    JSON = "ASDF"

@dataclass
class Body(Hashable):
    params: Schema
    content_type: str # extract from bodyTypes

    _meta: dict = field(default_factory=dict)

    def hash(self) -> str:
        return "body hash"


@dataclass
class Parameter:
    name: str
    description: str = ""

    param_type: str = None
    param_constrains: InputType = None

    _meta: dict = field(default_factory=dict)

@dataclass
class Response(Hashable):
    status_code: int
    body: Body = None
    headers: List[Dict[str, Parameter]] = field(default_factory=list)

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
    body: Body = None

    headers: Dict[str, Parameter] = field(default_factory=OrderedDict)
    query_params: Dict[str, Parameter] = field(default_factory=OrderedDict)

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

    def hash(self) -> str:
        return do_hash(f"{self.hosts}#{self.paths}")

current_api = API()

__all__ = ("API", "Path", "Request", "Response", "Body", "Param",
           "ParamInt", "ParamFloat", "ParamBoolean", "ParamString",
           "current_api")
