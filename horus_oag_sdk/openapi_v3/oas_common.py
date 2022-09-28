from .oas_schema_searcher import search_reference_content


def get_path(oas: dict, path: str) -> dict:
    return oas.get('paths', {}).get(path, {})


def get_method(oas: dict, path: str, method: str) -> dict:
    return oas.get('paths', {}).get(path, {}).get(method, {})


def get_responses(oas: dict, path: str, method: str) -> dict:
    return oas.get('paths', {}).get(path, {}).get(method, {}).get('responses', {})


def get_oas_parameters(oas: dict, path: str, method: str) -> list:
    return oas.get('paths', {}).get(path, {}).get(method, {}).get('parameters', [])


def get_request_schema(request: dict, request_type: str) -> dict:
    return request.get('content', {}).get(request_type, {}).get('schema', {})


def get_response(oas: dict, path: str, method: str, rc: str) -> (dict, str): # return response, reference
    response = oas.get('paths', {}).get(path, {}).get(method, {}).get('responses', {}).get(rc, {})
    if '$ref' in response:
        return search_reference_content(oas, response['$ref']), response['$ref']
    return response, None


def get_request(oas: dict, path: str, method: str) -> (dict, str):
    request_body = oas.get('paths', {}).get(path, {}).get(method, {}).get('requestBody', {})
    if '$ref' in request_body:
        return search_reference_content(oas, request_body['$ref']), request_body['$ref']
    return request_body, None


def get_response_schema(response: dict, response_type: str) -> dict:
    return response.get('content', {}).get(response_type, {}).get('schema', {})


def get_components(oas: dict) -> dict:
    return oas.get('components', {})


def get_schemas(oas: dict) -> dict:
    return oas.get('components', {}).get('schemas', {})


def set_empty_components(oas: dict):
    if not 'components' in oas:
        oas['components'] = {}


def set_empty_schemas(oas: dict):
    set_empty_components(oas)
    if not 'schemas' in oas['components']:
        oas['components']['schemas'] = {}


def set_empty_security_schemes(oas: dict):
    set_empty_components(oas)
    if not 'securitySchemes' in oas['components']:
        oas['components']['securitySchemes'] = {}


def set_empty_request_body(oas: dict, path: str, method: str):
    if not 'requestBody' in oas['paths'][path][method]:
        oas['paths'][path][method]['requestBody'] = {}


def get_security_schemes(oas: dict) -> dict:
    return oas.get('components', {}).get('securitySchemes', {})
