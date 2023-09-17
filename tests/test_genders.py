from pages.gender import Gender
from utils.genders import GenderUtils


def test_genders(setup):
    config, access_token = setup

    response = Gender.get_genders(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.status_code == 200

    gender_list_from_db = GenderUtils.pull_genders_list_from_db()
    json_data = Gender.ordered((response.json()))
    gender_list_from_db = Gender.ordered(gender_list_from_db)
    assert json_data == gender_list_from_db

    # ERROR RESPONSE
    response = Gender.get_genders(config, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
