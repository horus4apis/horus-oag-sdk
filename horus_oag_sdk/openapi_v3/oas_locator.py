from powerful_pipes import read_json

from .oas_schema_searcher import search_reference_content
from .. import HorusOagSDKException

dict_operator = '~DICT~'  # followed by dict key
list_operator = '~LIST~'  # followed by index
parameter_operator = '~PARAM~'  # followed by dict with name and in


def locate_openapi_position(obj: dict | list, location: str, oas: dict) -> dict | list:
    if location.startswith(dict_operator):

        if "$ref" in obj:
            obj = search_reference_content(oas, obj.get("$ref"))

        location = location[len(dict_operator):]
        dict_key = location.split('~')[0]

        if not dict_key in obj:
            raise HorusOagSDKException(f"Key {dict_key} not found in dict")

        return locate_openapi_position(obj[dict_key], location[len(dict_key):], oas)
    elif location.startswith(list_operator):
        location = location[len(list_operator):]
        list_index = location.split('~')[0]

        if not list_index.isdigit():
            raise HorusOagSDKException(f"Index {list_index} is not an integer")

        if not int(list_index) < len(obj):
            raise HorusOagSDKException(f"Index {list_index} is out of bounds")

        return locate_openapi_position(obj[int(list_index)], location[len(list_index):], oas)
    elif location.startswith(parameter_operator):
        location = location[len(parameter_operator):]
        dict_key = location.split('~')[0]
        dict_key_json = read_json(dict_key)
        name = dict_key_json.get('name')
        parameter_in = dict_key_json.get('in')
        parameter = locate_parameter(obj, name, parameter_in)
        return locate_openapi_position(parameter, location[len(dict_key):], oas)
    else:
        return obj


def locate_parameter(parameters: list, parameter_name: str, parameter_in: str) -> dict:
    for parameter in parameters:
        if parameter.get('name') == parameter_name and parameter.get('in') == parameter_in:
            return parameter

    raise HorusOagSDKException(f"Parameter {parameter_name} of type {parameter_in} not found")
