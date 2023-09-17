import json

from pages.ad_placement_types_page import AdPlacementType


def test_ad_placement_position(setup):
    config, access_token = setup

    with open('assets/ad_placement_types.json') as json_file:
        ad_placement_types = json.load(json_file)

    response = AdPlacementType.get_ad_placement_types(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    assert response.json() == ad_placement_types

    # ERROR RESPONSE
    response = AdPlacementType.get_ad_placement_types(config, access_token=access_token,
                                                      error_response_check=True)
    assert response.status_code == 400
