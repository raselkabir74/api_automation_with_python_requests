from pages.age_groups_page import AgeGroups
from utils.age_group import AgeGroupUtils


def test_age_groups(setup):
    config, access_token = setup

    response = AgeGroups.get_age_groups(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    age_group_list_from_db = AgeGroupUtils.pull_age_group_list_from_db()
    json_data = AgeGroups.ordered(response.json())
    age_group_list_from_db = AgeGroups.ordered(age_group_list_from_db)
    assert json_data == age_group_list_from_db

    # ERROR RESPONSE
    response = AgeGroups.get_age_groups(config, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
