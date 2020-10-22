column_settings = {
    'Account': [
        {'id': 'id', 'title': 'ID', 'width': 35},
        {'id': 'name', 'title': 'NAME', 'width': -1},
    ],
    'CloudRegion': [
        {'id': 'id', 'title': 'ID', 'width': 25},
        {'id': 'provider', 'title': 'PROVIDER', 'width': 20},
        {'id': 'display_name', 'title': 'DISPLAY_NAME', 'width': 40},
        {'id': 'geo_coordinates', 'title': 'GEO-COORDINATES', 'width': -1, 'serialize': True}
    ],
    'CloudService': [
        {'id': 'id', 'title': 'ID', 'width': 35},
        {'id': 'provider', 'title': 'PROVIDER', 'width': 15},
        {'id': 'service', 'title': 'SERVICE', 'width': 20},
        {'id': 'deactivated', 'title': 'DEACTIVATED', 'width': -1, 'json': True}
    ],
    'Facility': [
        {'id': 'id', 'title': 'ID', 'width': 56},
        {'id': 'name', 'title': 'NAME', 'width': 55},
        {'id': 'state', 'title': 'STATE', 'width': -1},
    ],
    'Location': [
        {'id': 'id', 'title': 'ID', 'width': 15},
        {'id': 'name', 'title': 'NAME', 'width': 20},
        {'id': 'href', 'title': 'HREF', 'width': 25},
        {'id': 'geo_coordinates', 'title': 'GEO-COORDINATES', 'width': -1, 'serialize': True}
    ],
    'Network': [
        {'id': 'id', 'title': 'ID', 'width': 35},
        {'id': 'name', 'title': 'NAME', 'width': 25},
        {'id': 'state', 'title': 'STATE', 'width': 25},
        {'id': 'tags', 'title': 'TAGS', 'width': -1, 'json': True}
    ]
}
