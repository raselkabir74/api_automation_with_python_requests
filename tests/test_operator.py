import json

from pages.operator import Operators
from utils.operators import OperatorUtils


def test_operator(setup):
    config, access_token = setup

    with open('assets/operator/operator.json') as json_file:
        operator_data = json.load(json_file)

    country = operator_data['country']
    response = Operators.get_operator(config, access_token=access_token, country=country)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    exchange_data_from_db = OperatorUtils.pull_operator_data_from_db(country)

    assert response.json() == exchange_data_from_db

    # Error check response
    response = Operators.get_operator(config, access_token=access_token, country=country, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
