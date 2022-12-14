import json

components_available_keys = ['schemas', 'responses', 'parameters', 'examples', 'requestBodies', 'headers']


def drop_orphans_schemas(oas: dict):
    oas_str = json.dumps(oas)
    components = oas.get('components', {}) or {}

    for available_key in components_available_keys:
        if available_key in components:
            for key in components[available_key].copy():
                if not key.startswith('x-'):  # exclude x- keys (extensions)
                    ref = f"#/components/{available_key}/{key}"
                    if oas_str.count(ref) == 0:
                        del components[available_key][key]
            if len(components[available_key]) == 0:
                del components[available_key]