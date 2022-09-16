from .oas_schema_searcher import search_reference_content


def same_content(oas: dict, content_1: dict, content_2: dict) -> bool:
    """Compare two contents and return True if they are EQUIVALENT"""

    if len(content_1) != len(content_2):
        return False

    for content_type in content_1:
        if not content_type in content_2:
            return False

        if not same_schema(oas, content_1[content_type], content_2[content_type]):
            return False

    return True


def same_schema(oas: dict, sch1: dict, sch2: dict) -> bool:
    """Compare two schemas and return True if they are EQUIVALENT"""

    if 'schema' in sch1:
        sch1 = sch1['schema']

    if 'schema' in sch2:
        sch2 = sch2['schema']

    if "$ref" in sch1:
        sch1 = search_reference_content(oas, sch1["$ref"])

    if "$ref" in sch2:
        sch2 = search_reference_content(oas, sch2["$ref"])

    if not 'type' in sch1 or not 'type' in sch2:
        return False

    if sch1['type'] != sch2['type']:
        return False

    if sch1['type'] == 'object':
        properties_1 = sch1.get('properties', {})
        properties_2 = sch2.get('properties', {})

        if len(properties_1) != len(properties_2):
            return False

        for key, value in properties_1.items():
            if key not in properties_2:
                return False

            if not same_schema(oas, value, properties_2[key]):
                return False

    elif sch1['type'] == 'array':
        items_1 = sch1.get('items', {})
        items_2 = sch2.get('items', {})

        if not same_schema(oas, items_1, items_2):
            return False

    elif sch1['type'] == 'string':
        pattern_1 = sch1.get('pattern', None)
        pattern_2 = sch2.get('pattern', None)

        if not pattern_1 or not pattern_2:
            return False

        if pattern_1 == pattern_2:
            return True
        else:
            return False

    return True
