import json

from pages.audience import Audience
from utils.audience import AudienceUtils


def test_create_update_and_delete_audience_by_dmp_ids_with_mandatory_and_optional_params(setup):
    config, access_token = setup

    with open('assets/audience/audience_creation_by_dmp_ids.json') as json_file:
        audience_creation_by_dmp_ids = json.load(json_file)
    audience_creation_by_dmp_ids['name'] = audience_creation_by_dmp_ids['name'] + Audience.get_random_string(5)

    # CREATE AUDIENCE
    response = Audience.create_audience_by_dmp_ids(config, access_token=access_token,
                                                   audience_data=audience_creation_by_dmp_ids)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == audience_creation_by_dmp_ids['name']
    assert user_id == audience_creation_by_dmp_ids['userId']
    assert user_validity_minutes == audience_creation_by_dmp_ids['userValidityMinutes']
    assert description == audience_creation_by_dmp_ids['description']
    assert au_type == 3
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == ''
    assert country == ''
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'
    assert updated_at is None
    assert response.status_code == 200

    # UPDATE AUDIENCE
    with open('assets/audience/audience_update_by_dmp_ids.json') as json_file:
        audience_update_by_dmp_ids = json.load(json_file)
    audience_update_by_dmp_ids['name'] = audience_update_by_dmp_ids[
                                             'name'] + Audience.get_random_string(5)
    update_response = Audience.update_dmp_audience(config, access_token=access_token,
                                                   audience_data=audience_update_by_dmp_ids,
                                                   audience_id=(response.json())['id'])

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == audience_update_by_dmp_ids['name']
    assert user_id == audience_creation_by_dmp_ids['userId']
    assert user_validity_minutes == audience_update_by_dmp_ids['userValidityMinutes']
    assert description == audience_update_by_dmp_ids['description']
    assert au_type == 3
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == ''
    assert country == ''
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'

    # DELETE AUDIENCE
    delete_response = Audience.delete_dmp_audience(config, access_token=access_token,
                                                   audience_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'])

    assert created_at is None
    assert updated_at is None
    assert created_date is None
    assert name is None
    assert user_id is None
    assert user_validity_minutes is None
    assert description is None
    assert au_type is None
    assert status is None
    assert api_version is None
    assert member_count is None
    assert verticals is None
    assert country is None
    assert rule is None
    assert date_to is None
    assert date_from is None


def test_create_update_and_delete_audience_by_dmp_ids_with_mandatory_params(setup):
    config, access_token = setup

    with open('assets/audience/audience_creation_by_dmp_ids.json') as json_file:
        audience_creation_by_dmp_ids = json.load(json_file)
        del (audience_creation_by_dmp_ids['description'])
    audience_creation_by_dmp_ids['name'] = audience_creation_by_dmp_ids['name'] + Audience.get_random_string(5)

    # CREATE AUDIENCE
    response = Audience.create_audience_by_dmp_ids(config, access_token=access_token,
                                                   audience_data=audience_creation_by_dmp_ids)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == audience_creation_by_dmp_ids['name']
    assert user_id == audience_creation_by_dmp_ids['userId']
    assert user_validity_minutes == audience_creation_by_dmp_ids['userValidityMinutes']
    assert description is ''
    assert au_type == 3
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == ''
    assert country == ''
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'
    assert updated_at is None
    assert response.status_code == 200

    # UPDATE AUDIENCE
    with open('assets/audience/audience_update_by_dmp_ids.json') as json_file:
        audience_update_by_dmp_ids = json.load(json_file)
    audience_update_by_dmp_ids['name'] = audience_update_by_dmp_ids[
                                             'name'] + Audience.get_random_string(5)
    del (audience_update_by_dmp_ids['description'])
    update_response = Audience.update_dmp_audience(config, access_token=access_token,
                                                   audience_data=audience_update_by_dmp_ids,
                                                   audience_id=(response.json())['id'])

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == audience_update_by_dmp_ids['name']
    assert user_id == audience_creation_by_dmp_ids['userId']
    assert user_validity_minutes == audience_update_by_dmp_ids['userValidityMinutes']
    assert description is ''
    assert au_type == 3
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == ''
    assert country == ''
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'

    # DELETE AUDIENCE
    delete_response = Audience.delete_dmp_audience(config, access_token=access_token,
                                                   audience_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'])

    assert created_at is None
    assert updated_at is None
    assert created_date is None
    assert name is None
    assert user_id is None
    assert user_validity_minutes is None
    assert description is None
    assert au_type is None
    assert status is None
    assert api_version is None
    assert member_count is None
    assert verticals is None
    assert country is None
    assert rule is None
    assert date_to is None
    assert date_from is None


def test_audience_with_dmp_ids_invalid_response(setup):
    config, access_token = setup

    with open('assets/audience/audience_creation_by_dmp_ids.json') as json_file:
        audience_creation_by_dmp_ids = json.load(json_file)
    with open('assets/audience/audience_update_by_dmp_ids.json') as json_file:
        audience_update_by_dmp_ids = json.load(json_file)

    # ERROR RESPONSE
    response = Audience.create_audience_by_dmp_ids(config, access_token=access_token,
                                                   audience_data=audience_creation_by_dmp_ids,
                                                   error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"

    response = Audience.create_audience_by_dmp_ids(config, access_token=access_token,
                                                   audience_data=audience_creation_by_dmp_ids)
    update_response = Audience.update_dmp_audience(config, access_token=access_token,
                                                   audience_data=audience_update_by_dmp_ids,
                                                   audience_id=(response.json())['id'], error_response_check=True)
    assert update_response.status_code == 400
    assert (update_response.json())['error'] == "Bad request"

    delete_response = Audience.delete_dmp_audience(config, access_token=access_token,
                                                   audience_id=(response.json())['id'], error_response_check=True)
    assert delete_response.status_code == 400

    # INVALID RESPONSE
    audience_creation_by_dmp_ids["userId"] = 1276761267678098908
    audience_creation_by_dmp_ids["dmpIds"] = ["1276761267678098908-testing-purpose"]
    audience_creation_by_dmp_ids["userValidityMinutes"] = "testing-purpose"
    invalid_response = Audience.create_audience_by_dmp_ids(config, access_token=access_token,
                                                           audience_data=audience_creation_by_dmp_ids)
    assert invalid_response.status_code == 400
    assert (invalid_response.json())[
               'error'] == "The given data was invalid.  Invalid user ID. Invalid Dmp ID. The user " \
                           "validity minutes must be an integer.."

    # TODO: NEED TO INCLUDE INVALID RESPONSE FOR UPDATE AUDIENCE WITH DMP IDs


def test_create_update_and_delete_behavioural_audience_with_mandatory_and_optional_params(setup):
    config, access_token = setup

    with open('assets/audience/behavioural_audience_creation_data.json') as json_file:
        behavioural_audience_creation_data = json.load(json_file)
    behavioural_audience_creation_data['name'] = behavioural_audience_creation_data[
                                                     'name'] + Audience.get_random_string(5)

    # CREATE AUDIENCE
    response = Audience.create_behavioural_audience(config, access_token=access_token,
                                                    audience_data=behavioural_audience_creation_data)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == behavioural_audience_creation_data['name']
    assert user_id == behavioural_audience_creation_data['userId']
    assert user_validity_minutes == 0
    assert description == behavioural_audience_creation_data['description']
    assert au_type == 1
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == '3,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,386,387,388,389,390,391,392,393,' \
                        '394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416' \
                        ',417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,' \
                        '439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,1124,1125,' \
                        '1126,1127'
    assert country == 'bd'
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'
    assert updated_at is None
    assert response.status_code == 200

    # UPDATE AUDIENCE
    with open('assets/audience/behavioural_audience_update_data.json') as json_file:
        behavioural_audience_update_data = json.load(json_file)
    behavioural_audience_update_data['name'] = behavioural_audience_update_data[
                                                   'name'] + Audience.get_random_string(5)
    update_response = Audience.update_behavioural_audience(config, access_token=access_token,
                                                           audience_data=behavioural_audience_update_data,
                                                           audience_id=(response.json())['id'])

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == behavioural_audience_update_data['name']
    assert user_id == behavioural_audience_creation_data['userId']
    assert user_validity_minutes == 0
    assert description == behavioural_audience_update_data['description']
    assert au_type == 1
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == '5'
    assert country == 'bd'
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'
    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    # DELETE AUDIENCE
    delete_response = Audience.delete_behavioural_audience(config, access_token=access_token,
                                                           audience_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    assert created_at is None
    assert updated_at is None
    assert created_date is None
    assert name is None
    assert user_id is None
    assert user_validity_minutes is None
    assert description is None
    assert au_type is None
    assert status is None
    assert api_version is None
    assert member_count is None
    assert verticals is None
    assert country is None
    assert rule is None
    assert date_to is None
    assert date_from is None

    # ERROR RESPONSE
    response = Audience.create_behavioural_audience(config, access_token=access_token,
                                                    audience_data=behavioural_audience_creation_data,
                                                    error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"

    response = Audience.create_behavioural_audience(config, access_token=access_token,
                                                    audience_data=behavioural_audience_creation_data)
    update_response = Audience.update_behavioural_audience(config, access_token=access_token,
                                                           audience_data=behavioural_audience_update_data,
                                                           audience_id=(response.json())['id'],
                                                           error_response_check=True)
    assert update_response.status_code == 400
    assert (update_response.json())['error'] == "Bad request"

    delete_response = Audience.delete_behavioural_audience(config, access_token=access_token,
                                                           audience_id=(response.json())['id'],
                                                           error_response_check=True)
    assert delete_response.status_code == 400


def test_create_update_and_delete_behavioural_audience_with_mandatory_params(setup):
    config, access_token = setup

    with open('assets/audience/behavioural_audience_creation_data.json') as json_file:
        behavioural_audience_creation_data = json.load(json_file)
    del (behavioural_audience_creation_data['description'])
    del (behavioural_audience_creation_data['country'])
    behavioural_audience_creation_data['name'] = behavioural_audience_creation_data[
                                                     'name'] + Audience.get_random_string(5)

    # CREATE AUDIENCE
    response = Audience.create_behavioural_audience(config, access_token=access_token,
                                                    audience_data=behavioural_audience_creation_data)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == behavioural_audience_creation_data['name']
    assert user_id == behavioural_audience_creation_data['userId']
    assert user_validity_minutes == 0
    assert description == ''
    assert au_type == 1
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == '3,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,386,387,388,389,390,391,392,393,' \
                        '394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416' \
                        ',417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,' \
                        '439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,1124,1125,' \
                        '1126,1127'
    assert country == ''
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'
    assert updated_at is None
    assert response.status_code == 200

    # UPDATE AUDIENCE
    with open('assets/audience/behavioural_audience_update_data.json') as json_file:
        behavioural_audience_update_data = json.load(json_file)
    behavioural_audience_update_data['name'] = behavioural_audience_update_data[
                                                   'name'] + Audience.get_random_string(5)
    update_response = Audience.update_behavioural_audience(config, access_token=access_token,
                                                           audience_data=behavioural_audience_update_data,
                                                           audience_id=(response.json())['id'])

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert Audience.get_specific_date_with_specific_format('%Y-%m-%d') == str(created_date)

    assert name == behavioural_audience_update_data['name']
    assert user_id == behavioural_audience_creation_data['userId']
    assert user_validity_minutes == 0
    assert description == behavioural_audience_update_data['description']
    assert au_type == 1
    assert status == 1
    assert api_version == 1
    assert member_count == 0
    assert verticals == '5'
    assert country == ''
    assert rule == 0
    assert date_to == '0000-00-00'
    assert date_from == '0000-00-00'
    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    # DELETE AUDIENCE
    delete_response = Audience.delete_behavioural_audience(config, access_token=access_token,
                                                           audience_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    name, user_id, user_validity_minutes, au_type, status, description, date_from, \
        date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
        updated_at = AudienceUtils.pull_audience_data_from_db((response.json())['id'], db_close=False)

    assert created_at is None
    assert updated_at is None
    assert created_date is None
    assert name is None
    assert user_id is None
    assert user_validity_minutes is None
    assert description is None
    assert au_type is None
    assert status is None
    assert api_version is None
    assert member_count is None
    assert verticals is None
    assert country is None
    assert rule is None
    assert date_to is None
    assert date_from is None


def test_behavioural_audience_invalid_response(setup):
    config, access_token = setup

    with open('assets/audience/behavioural_audience_creation_data.json') as json_file:
        behavioural_audience_creation_data = json.load(json_file)
    with open('assets/audience/behavioural_audience_update_data.json') as json_file:
        behavioural_audience_update_data = json.load(json_file)

    # ERROR RESPONSE
    response = Audience.create_behavioural_audience(config, access_token=access_token,
                                                    audience_data=behavioural_audience_creation_data,
                                                    error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"

    response = Audience.create_behavioural_audience(config, access_token=access_token,
                                                    audience_data=behavioural_audience_creation_data)
    update_response = Audience.update_behavioural_audience(config, access_token=access_token,
                                                           audience_data=behavioural_audience_update_data,
                                                           audience_id=(response.json())['id'],
                                                           error_response_check=True)
    assert update_response.status_code == 400
    assert (update_response.json())['error'] == "Bad request"

    delete_response = Audience.delete_behavioural_audience(config, access_token=access_token,
                                                           audience_id=(response.json())['id'],
                                                           error_response_check=True)
    assert delete_response.status_code == 400

    # INVALID RESPONSE
    behavioural_audience_creation_data["userId"] = 1276761267678098908
    behavioural_audience_creation_data["interestIds"] = [323242344434]
    behavioural_audience_creation_data["country"] = "bd-testing"
    invalid_response = Audience.create_behavioural_audience(config, access_token=access_token,
                                                            audience_data=behavioural_audience_creation_data)
    assert invalid_response.status_code == 400
    assert (invalid_response.json())[
               'error'] == "The given data was invalid.  Invalid user ID. Invalid country code. " \
                           "Invalid interest provided."

    # TODO: NEED TO INCLUDE INVALID RESPONSE FOR UPDATE AUDIENCE


def test_audience_interest(setup):
    config, access_token = setup

    with open('assets/audience/audience_interest.json') as json_file:
        audience_interest = json.load(json_file)

    response = Audience.get_audience_interest(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    assert response.json() == audience_interest

    # ERROR RESPONSE
    response = Audience.get_audience_interest(config, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
