from pages.sites import Sites
from utils.sites import SitesUtils


def test_site_platforms(setup):
    config, access_token = setup

    response = Sites.get_platforms(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    sites_platforms_data_from_db = SitesUtils.pull_sites_platforms_data_from_db()
    assert response.json() == sites_platforms_data_from_db

    # Error check response
    response = Sites.get_platforms(config, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_site_types(setup):
    config, access_token = setup

    response = Sites.get_types(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    sites_types_data_from_db = SitesUtils.pull_sites_types_data_from_db()
    assert response.json() == sites_types_data_from_db

    # Error check response
    response = Sites.get_types(config, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_sites(setup):
    config, access_token = setup

    response = Sites.get_sites(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    sites_data_from_db = SitesUtils.pull_sites_data_from_db()
    json_data = Sites.ordered(response.json())
    assert json_data == sites_data_from_db

    # Error check response
    response = Sites.get_sites(config, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"

