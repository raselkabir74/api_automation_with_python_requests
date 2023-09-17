import json

from pages.country import Country


def test_country_list(setup):
    config, access_token = setup

    with open('assets/country/country_list.json') as json_file:
        country_list = json.load(json_file)

    response = Country.get_county_list(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    assert response.json() == country_list

    # ERROR RESPONSE
    response = Country.get_county_list(config, access_token=access_token,
                                                              error_response_check=True)
    assert response.status_code == 400


def test_state_list(setup):
    config, access_token = setup

    with open('assets/country/states_list.json') as json_file:
        country_list = json.load(json_file)

    response = Country.get_states_list(config, county_code='bd', access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    assert response.json() == country_list
    # ERROR RESPONSE
    response = Country.get_states_list(config, county_code='bd',access_token=access_token,
                                                              error_response_check=True)
    assert response.status_code == 400