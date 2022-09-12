

def get_path(oas: dict, path: str) -> dict:
    return oas.get('paths', {}).get(path, {})


def get_method(oas: dict, path: str, method: str) -> dict:
    return oas.get('paths', {}).get(path, {}).get(method, {})


def get_responses(oas: dict, path: str, method: str) -> dict:
    return oas.get('paths', {}).get(path, {}).get(method, {}).get('responses', {})


def get_oas_parameters(oas: dict, path: str, method: str) -> list:
    return oas.get('paths', {}).get(path, {}).get(method, {}).get('parameters', [])


def get_request_schema(oas: dict, path: str, method: str, request_type: str) -> dict:
    return oas.get('paths', {}).get(path, {}).get(method, {}).get('requestBody', {}).get('content', {}).get(request_type, {}).get('schema', {})


def get_response_schema(oas: dict, path: str, method: str, rc: str, response_type: str) -> dict:
    return oas.get('paths', {}).get(path, {}).get(method, {}).get('responses', {}).get(rc, {}).get('content', {}).get(response_type, {}).get('schema', {})

