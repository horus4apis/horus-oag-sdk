from horus_oag_sdk.openapi_v3 import drop_orphans_schemas
from deepdiff import DeepDiff


def test_drop_orphans_schemas_no_orphans():
    base_oas = {
        'paths': {
            '/a': {
                'get': {
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/MySchema'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'components': {
            'schemas': {
                'a': {
                    'type': 'object',
                    'properties': {
                        'b': {
                            'type': 'string'
                        }
                    }
                }
            }
        }
    }

    expected_oas = base_oas.copy()

    drop_orphans_schemas(base_oas)

    changes_diff = DeepDiff(expected_oas, base_oas, ignore_order=True)
    assert not changes_diff, f"difference in changes: {changes_diff}"


def test_drop_orphans_schemas_orphans():
    base_oas = {
        'paths': {
            '/a': {
                'get': {
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/MySchema1'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'components': {
            'schemas': {
                'a': {
                    'type': 'object',
                    'properties': {
                        'b': {
                            'type': 'string'
                        }
                    }
                }
            }
        }
    }

    expected_oas = {
        'paths': {
            '/a': {
                'get': {
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/MySchema1'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'components': {}
    }

    drop_orphans_schemas(base_oas)
    changes_diff = DeepDiff(expected_oas, base_oas, ignore_order=True)
    assert not changes_diff, f"difference in changes: {changes_diff}"
