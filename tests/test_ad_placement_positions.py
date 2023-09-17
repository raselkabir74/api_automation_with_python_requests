import json

from pages.ad_placement_positions_page import AdPlacementPosition


def test_ad_placement_position(setup):
    config, access_token = setup

    with open('assets/ad_placement_positions.json') as json_file:
        ad_placement_positions_data = json.load(json_file)

    response = AdPlacementPosition.get_ad_placement_positions(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    assert response.json() == ad_placement_positions_data

    # ERROR RESPONSE
    response = AdPlacementPosition.get_ad_placement_positions(config, access_token=access_token,
                                                              error_response_check=True)
    assert response.status_code == 400
