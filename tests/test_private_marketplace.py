from pages.private_marketplace import PrivateMarketplace
from utils.private_marketplace import PrivateMarketplaceUtils


def test_get_list_of_private_marketplaces(setup):
    config, access_token = setup

    response = PrivateMarketplace.get_list_of_private_marketplaces(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    private_marketplace_list_from_db = PrivateMarketplaceUtils.pull_private_marketplace_data_from_db()
    json_data = PrivateMarketplace.ordered(response.json())
    private_marketplace_list_from_db = PrivateMarketplace.ordered(private_marketplace_list_from_db)
    assert json_data == private_marketplace_list_from_db

    # ERROR RESPONSE
    response = PrivateMarketplace.get_list_of_private_marketplaces(config, access_token=access_token,
                                                                   error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
