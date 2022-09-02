

def same_schema(sch1: dict, sch2: dict) -> bool:
    """Compare two schemas and return True if they are EQUIVALENT"""

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

            if not same_schema(value, properties_2[key]):
                return False

    elif sch1['type'] == 'array':
        items_1 = sch1.get('items', {})
        items_2 = sch2.get('items', {})

        if not same_schema(items_1, items_2):
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
