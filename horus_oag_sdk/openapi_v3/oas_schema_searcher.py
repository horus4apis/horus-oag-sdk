from jsonpath_ng import parse


def search_reference_content(oas_input: dict, ref: str) -> dict or None:
    ref = ref.lstrip('#/')
    ref_array = ref.split('/')

    for key in ref_array:
        if key in oas_input:
            oas_input = oas_input[key]
        else:
            return None

    return oas_input


def replace_all_references(oas_input: dict, base_ref: str, new_ref: str):
    if isinstance(oas_input, dict):
        for key, value in oas_input.items():
            if key == '$ref' and value == base_ref:
                oas_input[key] = new_ref
            else:
                replace_all_references(value, base_ref, new_ref)
    elif isinstance(oas_input, list):
        for item in oas_input:
            replace_all_references(item, base_ref, new_ref)


def convert_ref_to_jsonptr(ref: str) -> str:
    return f"${ref.replace('#', '').replace('/', '.')}"


def insert_with_jsonp(oas_input: dict, jsonp: str, value: dict):
    try:
        json_path_expr = parse(jsonp)
        position = json_path_expr.find(oas_input)

        for sample_key, sample_value in value.items():

            position[0].value[sample_key] = sample_value

    except Exception as e:
        print(f"Error finding json path {jsonp}")
