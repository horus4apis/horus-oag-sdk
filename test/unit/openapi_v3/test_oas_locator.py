import pytest

from horus_oag_sdk import HorusOagSDKException
from horus_oag_sdk.openapi_v3.oas_locator import locate_openapi_position, locate_parameter


def test_empty_location():
    assert locate_openapi_position({}, '', {}) == {}
    assert locate_openapi_position({'a': 1}, '', {}) == {'a': 1}


def test_dict_location():
    assert locate_openapi_position({'x': 1}, '~DICT~x', {'x': 1}) == 1
    assert locate_openapi_position({'x': {'y': 1}}, '~DICT~x', {'x': {'y': 1}}) == {'y': 1}
    assert locate_openapi_position({'x': {'y': 1}}, '~DICT~x~DICT~y', {'x': {'y': 1}}) == 1

    with pytest.raises(HorusOagSDKException) as e:
        locate_openapi_position({'x': 1}, '~DICT~y', {'x': 1})

    assert str(e.value) == "Key y not found in dict"


def test_list_location_index():
    assert locate_openapi_position({'x': [1, 2]}, '~DICT~x~LIST~0', {'x': [1, 2]}) == 1
    assert locate_openapi_position({'x': [1, 2]}, '~DICT~x~LIST~1', {'x': [1, 2]}) == 2

    with pytest.raises(HorusOagSDKException) as e:
        locate_openapi_position({'x': [1, 2]}, '~DICT~x~LIST~2',{'x': [1, 2]})

    assert str(e.value) == "Index 2 is out of bounds"


def test_list_location_dict_values():
    oas = [
        {'name': 'a', 'in': 'query'},
        {'name': 'b', 'in': 'header'},
        {"foo": "bar", "aux": "baz"},
        {'name': 'c', 'in': 'query'},
        {"foo": "bar", "baz": "qux", "a": "b"},
    ]
    location = '~LIST~{"foo": "bar"}'
    assert locate_openapi_position(oas, location, oas) == {"foo": "bar", "aux": "baz"}

    location = '~LIST~{"foo": "bar", "baz": "qux"}'
    assert locate_openapi_position(oas, location, oas) == {"foo": "bar", "baz": "qux", "a": "b"}


def test_parameter_location():
    assert locate_openapi_position({'parameters': [{'name': 'a', 'in': 'query'}]}, '~DICT~parameters~PARAM~{"name":"a", "in": "query"}', {'parameters': [{'name': 'a', 'in': 'query'}]}) == {'name': 'a', 'in': 'query'}

    with pytest.raises(HorusOagSDKException) as e:
        locate_openapi_position({'parameters': [{'name': 'a', 'in': 'query'}]}, '~DICT~parameters~PARAM~{"name":"b", "in": "query"}', {'parameters': [{'name': 'a', 'in': 'query'}]})

    assert str(e.value) == "Parameter b of type query not found"


def test_locate_parameter():
    parameters = [
        {'name': 'a', 'in': 'query'},
        {'name': 'b', 'in': 'header'},
        {'name': 'c', 'in': 'query'},
    ]

    assert locate_parameter(parameters, 'a', 'query') == {'name': 'a', 'in': 'query'}
    assert locate_parameter(parameters, 'b', 'header') == {'name': 'b', 'in': 'header'}
    assert locate_parameter(parameters, 'c', 'query') == {'name': 'c', 'in': 'query'}

    with pytest.raises(HorusOagSDKException) as e:
        locate_parameter(parameters, 'd', 'query')

    assert str(e.value) == "Parameter d of type query not found"


def test_locate_parameter_complex_no_ref():
    openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": "Test",
            "version": "1.0.0"
        },
        "paths": {
            "/test": {
                "get": {
                    "parameters": [
                        {
                            "name": "a",
                            "in": "query",
                            "schema": {
                                "type": "string"
                            }
                        },
                        {
                            "name": "b",
                            "in": "query",
                            "schema": {
                                "type": "string"
                            }
                        }
                    ]
                }
            }
        }
    }

    assert locate_openapi_position(openapi, '~DICT~paths~DICT~/test~DICT~get~DICT~parameters~PARAM~{"name":"a", "in": "query"}~DICT~schema', openapi) == {"type": "string"}


def test_locate_parameter_complex_ref():
    ...

