from powerful_pipes import write_to_stderr

from .oas_schema_searcher import search_reference_content, replace_all_references


def merge_schemas(base_schema: dict, merged_schema: dict, oas: dict):
    if '$ref' in base_schema:
        base_schema = search_reference_content(oas, base_schema['$ref'])

    if '$ref' in merged_schema:
        merged_schema = search_reference_content(oas, merged_schema['$ref'])

    null = False
    if not 'type' in base_schema and not 'type' in merged_schema:
        null = True
    elif not 'type' in base_schema:
        base_schema['type'] = merged_schema['type']
    elif not 'type' in merged_schema:
        merged_schema['type'] = base_schema['type']

    if not null:
        if base_schema['type'] != merged_schema['type']:
            if base_schema['type'] == 'integer' and merged_schema['type'] == 'number':
                base_schema['type'] = 'number'
            elif base_schema['type'] == 'number' and merged_schema['type'] == 'integer':
                merged_schema['type'] = 'number'
            else:
                write_to_stderr(f"Warning: Cannot merge schemas with different types, base schema of type {base_schema['type']} and new schema of type {merged_schema['type']}")

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

    # merge additional properties property
    if 'additionalProperties' in merged_schema:
        base_schema['additionalProperties'] = merged_schema['additionalProperties']

    # merge required list
    base_required = base_schema.get("required", [])
    merged_required = merged_schema.get("required", [])
    new_required = list(set(base_required).intersection(merged_required)) # get common required properties
    if len(new_required) > 0:
        base_schema['required'] = new_required

    # merge extensions
    for key, value in merged_schema.items():
        if key.startswith("x-"):
            base_schema[key] = value

    return base_schema
