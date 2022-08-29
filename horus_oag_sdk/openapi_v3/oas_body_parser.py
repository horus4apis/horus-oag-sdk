
class OasParserException(Exception):
    ...


def parse_body(raw, request_type: str = 'undefined') -> dict:
    """ create a new schema """
    schema = {}

    if request_type == 'application/json':
        schema = parse_json_body(raw)
    elif request_type == 'application/x-www-form-urlencoded':
        ...  # TODO https://docs.python.org/3/library/urllib.parse.html#urllib.parse.parse_qsl
    elif request_type == 'multipart/form-data':
        ...  # TODO https://julien.danjou.info/handling-multipart-form-data-python/
    elif request_type == 'text/plain':
        schema['type'] = 'string'
    else:
        schema['type'] = parse_base_body(raw)

    return {'schema': schema}


def parse_json_body(raw) -> dict:
    """ create a new json schema"""
    schema = {}

    raw_type = type(raw)
    if raw_type is dict:
        schema['type'] = 'object'
        schema['additionalProperties'] = False

        if raw:
            schema['properties'] = {}
            schema['required'] = []
            for key, value in raw.items():
                schema['properties'][key] = parse_json_body(value)
                schema['required'].append(key)

    elif raw_type in (list, tuple, set):
        schema['type'] = 'array'
        if raw:
            # TODO: provisional, an array can have different schemas in different positions
            schema['items'] = parse_json_body(raw[0])
    else:
        schema['type'] = parse_base_body(raw)

    return schema


def parse_base_body(value) -> str:
    return_types = {
        "str": "string",
        "int": "integer",
        "float": "number",
        "bool": "boolean",
    }

    try:
        return return_types[type(value).__name__]
    except KeyError:
        raise OasParserException('Unsupported type')
