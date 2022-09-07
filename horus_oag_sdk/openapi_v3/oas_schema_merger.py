from powerful_pipes import write_to_stderr

from .oas_schema_searcher import search_reference_content, replace_all_references


class OasMergerException(Exception):
    ...


def merge_schemas(base_schema: dict, merged_schema: dict, oas: dict):
    if '$ref' in base_schema:
        base_schema = search_reference_content(oas, base_schema['$ref'])

    if '$ref' in merged_schema:
        merged_schema = search_reference_content(oas, merged_schema['$ref'])

    not_null = True
    if not 'type' in base_schema and not 'type' in merged_schema:
        not_null = False
    elif not 'type' in base_schema:
        base_schema['type'] = merged_schema['type']
    elif not 'type' in merged_schema:
        merged_schema['type'] = base_schema['type']

    if base_schema['type'] != merged_schema['type']:
        write_to_stderr(f"Warning: Cannot merge schemas with different types, base schema of type {base_schema['type']} and new schema of type {merged_schema['type']}")

    if not_null:
        if base_schema['type'] == 'object':

            # create properties object if not exists
            if 'properties' not in base_schema:
                base_schema['properties'] = {}
            if 'properties' not in merged_schema:
                merged_schema['properties'] = {}

            for key, value in merged_schema['properties'].items():
                if key not in base_schema['properties']:
                    base_schema['properties'][key] = value
                else:
                    merge_schemas(base_schema['properties'][key], merged_schema['properties'][key], oas)


        elif base_schema['type'] == 'array':
            items_1 = base_schema.get('items', {})
            items_2 = merged_schema.get('items', {})
            merge_schemas(items_1, items_2, oas)

    # merge nullable property
    if 'nullable' in merged_schema:
        base_schema['nullable'] = True

    return base_schema

#TODO list:
    # merge required object list
    # preserve non generated schema names
    # merge extensions
