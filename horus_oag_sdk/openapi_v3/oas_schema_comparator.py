

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
            ...

    elif sch1['type'] == 'array':
        ...
    elif sch1['type'] == 'string':
        # use REGEX
        ...

    return True