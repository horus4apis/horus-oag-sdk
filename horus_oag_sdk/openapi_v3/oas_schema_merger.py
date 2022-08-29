
class OasMergerException(Exception):
    ...


def merge_schemas(sch1: dict, sch2: dict) -> dict: # the merge will be in sch1
    ## TODO add cmp for null types

    not_null = True
    if not 'type' in sch1 and not 'type' in sch2:
        not_null = False
    elif not 'type' in sch1:
        sch1['type'] = sch2['type']
    elif not 'type' in sch2:
        sch2['type'] = sch1['type']

    if sch1['type'] != sch2['type']:
        raise OasMergerException('Cannot merge schemas with different types')

    if not_null:
        if sch1['type'] == 'object':

            # create properties object if not exists
            if 'properties' not in sch1:
                sch1['properties'] = {}
            if 'properties' not in sch2:
                sch2['properties'] = {}

            for key, value in sch2['properties'].items():
                if key not in sch1['properties']:
                    sch1['properties'][key] = value
                else:
                    merge_schemas(sch1['properties'][key], sch2['properties'][key])


        elif sch1['type'] == 'array':
            ...
        elif sch1['type'] == 'string':
            # this will cause a merge in the db sample lists
            ...


    # merge nullable property
    if 'nullable' in sch2:
        sch1['nullable'] = True

    return sch1

#TODO: merge required object list
