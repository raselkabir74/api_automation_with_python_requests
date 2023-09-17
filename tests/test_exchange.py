from pages.exchange import Exchanges
from utils.exchanges import ExchangeUtils


def test_exchanges_list(setup):
    config, access_token = setup

    response = Exchanges.get_exchange_list(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    exchange_data_from_db = ExchangeUtils.pull_exchange_data_from_db()
    assert response.json() == exchange_data_from_db

    # Error check response
    response = Exchanges.get_exchange_list(config, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
