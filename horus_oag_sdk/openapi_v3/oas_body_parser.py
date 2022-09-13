from urllib.parse import parse_qsl

from powerful_pipes import read_json, write_to_stderr

class OasParserException(Exception):
    ...


def parse_body(raw, request_type: str = 'undefined') -> dict:
    """ create a new schema """
    schema = {}
    if request_type == 'application/json':
        raw = read_json(raw)
        schema = parse_json_body(raw)
    elif request_type == 'application/x-www-form-urlencoded':
        parsed_urlencoded = parse_qsl(raw)
        json_schema = {}
        for key, value in parsed_urlencoded:
            json_schema[key] = value
        schema = parse_json_body(json_schema)
    elif request_type == 'multipart/form-data':
        ...  # TODO https://julien.danjou.info/handling-multipart-form-data-python/
    elif request_type == 'text/plain':
        schema['type'] = 'string'
    else:
        schema['type'] = parse_base_body(raw)
    return schema


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
            schema['items'] = {}
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


def guess_body_type(raw_boyd: str, headers: dict) -> str or None:
    content_type = headers.get('content-type', '')

    if content_type:
        if 'application/json' in content_type:
            try:
                read_json(raw_boyd)
            except Exception as e:
                write_to_stderr(f"Error parsing json body: {raw_boyd}")
            else:
                return 'application/json'
        elif 'application/x-www-form-urlencoded' in content_type:
            parsed_urlencoded = parse_qsl(raw_boyd)
            if not parsed_urlencoded:
                write_to_stderr(f"Error parsing urlencoded body: {raw_boyd}")
            else:
                return 'application/x-www-form-urlencoded'
        elif content_type.startswith('multipart/form-data'):
            # TODO: validate first to ensure correct type
            return 'multipart/form-data'
        elif 'text/plain' in content_type:
            return 'text/plain'
        else:
            write_to_stderr("Unsupported content-type: {}".format(content_type))
    else:
        # two alternatives, json or text/plain
        try:
            read_json(raw_boyd)
        except Exception as e:
            return 'text/plain'
        else:
            return 'application/json'
        # TODO add urlencoded here
