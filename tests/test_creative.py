import json

from pages.creative import Creative
from utils.creative import CreativeUtils


def test_create_edit_and_delete_banner_type_creative_set_with_mandatory_and_optional_params(setup):
    config, access_token = setup

    index = None
    next_page_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['creative_set_list'], '?page=2')
    prev_page_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['creative_set_list'], '?page=1')
    path = '{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                           config['api']['creative_set_list'])

    with open('assets/creative/creative_set_creation_data.json') as json_file:
        creative_set_creation_data = json.load(json_file)
    creative_set_creation_data['title'] = creative_set_creation_data['title'] + Creative.get_random_string(5)

    # CREATE BANNER TYPE CREATIVE SET WITH MANDATORY + OPTIONAL PARAMS
    response = Creative.create_creative_set(config, access_token=access_token,
                                            creative_set_data=creative_set_creation_data)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    assert response.status_code == 200
    assert response.json()['title'] == creative_set_creation_data['title']
    assert response.json()['creative_type_id'] == creative_set_creation_data['creative_type_id']

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'], db_close=False)

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_creation_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == creative_set_creation_data['creative_type_id']
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 1

    # UPDATE BANNER TYPE CREATIVE SET WITH MANDATORY + OPTIONAL PARAMS
    with open('assets/creative/creative_set_update_data.json') as json_file:
        creative_set_update_data = json.load(json_file)
    creative_set_update_data['title'] = creative_set_update_data[
                                            'title'] + Creative.get_random_string(5)
    update_response = Creative.update_creative_set(config, access_token=access_token,
                                                   creative_set_data=creative_set_update_data,
                                                   creative_set_id=(response.json())['id'])

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'], db_close=False)

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_update_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == creative_set_creation_data['creative_type_id']
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 1

    # GET CREATIVE SET LIST
    with open('assets/creative/get_creative_set_list_data.json') as json_file:
        get_creative_set_list_data = json.load(json_file)
    get_response = Creative.get_creative_set_list(config, access_token=access_token,
                                                  creative_set_data=get_creative_set_list_data)

    for i, item in enumerate(get_response.json()['data']):
        if item["id"] == response.json()['id']:
            index = i
            break
    assert get_response.json()['data'][index]['id'] == response.json()['id']
    assert get_response.json()['data'][index]['title'] == creative_set_update_data['title']
    assert get_response.json()['data'][index]['creative_type_id'] == creative_set_creation_data['creative_type_id']
    assert get_response.json()['data'][index]['creative_count'] == 0
    assert get_response.json()['current_page'] == get_creative_set_list_data['page']
    assert get_response.json()['from'] == 1
    assert get_response.json()['next_page_url'] == next_page_url
    assert get_response.json()['path'] == path
    assert get_response.json()['per_page'] == 15
    assert get_response.json()['to'] == len(get_response.json()['data'])
    assert get_response.json()['prev_page_url'] is None

    get_creative_set_list_data['page'] = 2
    get_response = Creative.get_creative_set_list(config, access_token=access_token,
                                                  creative_set_data=get_creative_set_list_data)
    assert get_response.json()['current_page'] == get_creative_set_list_data['page']
    assert get_response.json()['from'] == 16
    assert get_response.json()['path'] == path
    assert get_response.json()['per_page'] == 15
    assert get_response.json()['prev_page_url'] == prev_page_url

    # DELETE BANNER TYPE CREATIVE SET WITH MANDATORY + OPTIONAL PARAMS
    delete_response = Creative.delete_creative_set(config, access_token=access_token,
                                                   creative_set_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'])

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_update_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == creative_set_creation_data['creative_type_id']
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 0


def test_create_edit_and_delete_native_type_creative_set_with_mandatory_and_optional_params(setup):
    config, access_token = setup

    with open('assets/creative/creative_set_creation_data.json') as json_file:
        creative_set_creation_data = json.load(json_file)
    creative_set_creation_data['title'] = creative_set_creation_data['title'] + Creative.get_random_string(5)
    creative_set_creation_data['creative_type_id'] = 2

    # CREATE NATIVE TYPE CREATIVE SET WITH MANDATORY + OPTIONAL PARAMS
    response = Creative.create_creative_set(config, access_token=access_token,
                                            creative_set_data=creative_set_creation_data)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    assert response.status_code == 200
    assert response.json()['title'] == creative_set_creation_data['title']
    assert response.json()['creative_type_id'] == creative_set_creation_data['creative_type_id']

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'], db_close=False)

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_creation_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == creative_set_creation_data['creative_type_id']
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 1

    # UPDATE NATIVE TYPE CREATIVE SET WITH MANDATORY + OPTIONAL PARAMS
    with open('assets/creative/creative_set_update_data.json') as json_file:
        creative_set_update_data = json.load(json_file)
    creative_set_update_data['title'] = creative_set_update_data[
                                            'title'] + Creative.get_random_string(5)
    update_response = Creative.update_creative_set(config, access_token=access_token,
                                                   creative_set_data=creative_set_update_data,
                                                   creative_set_id=(response.json())['id'])

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'], db_close=False)

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_update_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == creative_set_creation_data['creative_type_id']
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 1

    # DELETE NATIVE TYPE CREATIVE SET WITH MANDATORY + OPTIONAL PARAMS
    delete_response = Creative.delete_creative_set(config, access_token=access_token,
                                                   creative_set_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'])

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_update_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == creative_set_creation_data['creative_type_id']
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 0


def test_create_edit_and_delete_creative_set_with_mandatory_params(setup):
    config, access_token = setup

    with open('assets/creative/creative_set_creation_data.json') as json_file:
        creative_set_creation_data = json.load(json_file)
    del (creative_set_creation_data['creative_type_id'])
    creative_set_creation_data['title'] = creative_set_creation_data['title'] + Creative.get_random_string(5)

    # CREATE BANNER TYPE CREATIVE SET WITH MANDATORY PARAMS
    response = Creative.create_creative_set(config, access_token=access_token,
                                            creative_set_data=creative_set_creation_data)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    assert response.status_code == 200
    assert response.json()['title'] == creative_set_creation_data['title']

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'], db_close=False)

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_creation_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == 1
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 1

    # UPDATE BANNER TYPE CREATIVE SET WITH MANDATORY PARAMS
    with open('assets/creative/creative_set_update_data.json') as json_file:
        creative_set_update_data = json.load(json_file)
    creative_set_update_data['title'] = creative_set_update_data[
                                            'title'] + Creative.get_random_string(5)
    update_response = Creative.update_creative_set(config, access_token=access_token,
                                                   creative_set_data=creative_set_update_data,
                                                   creative_set_id=(response.json())['id'])

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'], db_close=False)

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_update_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == 1
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 1

    # DELETE BANNER TYPE CREATIVE SET WITH MANDATORY PARAMS
    delete_response = Creative.delete_creative_set(config, access_token=access_token,
                                                   creative_set_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, created_at, updated_at = \
        CreativeUtils.pull_creative_set_data_from_db(response.json()['id'])

    create_at = str(created_at).split(' ')
    update_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == create_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == update_at[0]
    assert title == creative_set_update_data['title']
    assert user_id == creative_set_creation_data['userId']
    assert creative_type_id == 1
    assert creative_count == 0
    assert duplicate_count == 0
    assert is_reserved == 0
    assert status == 0


def test_creative_set_invalid_response(setup):
    config, access_token = setup

    with open('assets/creative/creative_set_creation_data.json') as json_file:
        creative_set_creation_data = json.load(json_file)
    creative_set_creation_data['title'] = creative_set_creation_data['title'] + Creative.get_random_string(5)

    with open('assets/creative/creative_set_update_data.json') as json_file:
        creative_set_update_data = json.load(json_file)
    creative_set_update_data['title'] = creative_set_update_data[
                                            'title'] + Creative.get_random_string(5)

    with open('assets/creative/get_creative_set_list_data.json') as json_file:
        get_creative_set_list_data = json.load(json_file)

    # ERROR RESPONSE
    response = Creative.create_creative_set(config, access_token=access_token,
                                            creative_set_data=creative_set_creation_data, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"

    response = Creative.create_creative_set(config, access_token=access_token,
                                            creative_set_data=creative_set_creation_data)
    update_response = Creative.update_creative_set(config, access_token=access_token,
                                                   creative_set_data=creative_set_update_data,
                                                   creative_set_id=(response.json())['id'], error_response_check=True)
    assert update_response.status_code == 400
    assert (update_response.json())['error'] == "Bad request"

    get_response = Creative.get_creative_set_list(config, access_token=access_token,
                                                  creative_set_data=get_creative_set_list_data,
                                                  error_response_check=True)
    assert get_response.status_code == 400
    assert (get_response.json())['error'] == "Bad request"

    delete_response = Creative.delete_creative_set(config, access_token=access_token,
                                                   creative_set_id=(response.json())['id'], error_response_check=True)
    assert delete_response.status_code == 400

    # INVALID RESPONSE
    creative_set_creation_data['userId'] = 1231232423423414125555555555555
    invalid_response = Creative.create_creative_set(config, access_token=access_token,
                                                    creative_set_data=creative_set_creation_data)
    assert invalid_response.status_code == 400
    assert (invalid_response.json())['error'] == "The given data was invalid.  Invalid user ID."

    del (creative_set_creation_data['userId'])
    del (creative_set_creation_data['title'])
    invalid_response = Creative.create_creative_set(config, access_token=access_token,
                                                    creative_set_data=creative_set_creation_data)
    assert invalid_response.status_code == 400
    assert (invalid_response.json())[
               'error'] == "The given data was invalid.  The user id field is required.. The title field is required.."

    del (creative_set_update_data['title'])
    invalid_response = Creative.update_creative_set(config, access_token=access_token,
                                                    creative_set_data=creative_set_update_data,
                                                    creative_set_id=(response.json())['id'])
    assert invalid_response.status_code == 400
    assert (invalid_response.json())[
               'error'] == "The given data was invalid.  The title field is required.."


def test_create_edit_and_delete_banner_type_creative(setup):
    config, access_token = setup

    index = None
    path = '{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                           config['api']['creative_list'])
    next_page_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['creative_list'], '?page=2')

    with open('assets/creative/banner_creative_creation_data.json') as json_file:
        banner_creative_creation_data = json.load(json_file)
    banner_creative_creation_data['title'] = banner_creative_creation_data['title'] + Creative.get_random_string(5)

    # CREATE CREATIVE
    response = Creative.create_creative(config, access_token=access_token, creative_data=banner_creative_creation_data)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    assert response.status_code == 200

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(response.json()['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == banner_creative_creation_data['title']
    assert user_id == banner_creative_creation_data['userId']
    assert creative_set_id == banner_creative_creation_data['creativeSetId']
    assert type_id == 1
    assert subtype_id == 1
    assert is_reserved == 0
    assert status == 10
    assert width == 0
    assert height == 0

    # UPDATE CREATIVE
    with open('assets/creative/banner_creative_update_data.json') as json_file:
        banner_creative_update_data = json.load(json_file)
    banner_creative_update_data['title'] = banner_creative_update_data[
                                               'title'] + Creative.get_random_string(5)
    update_response = Creative.update_banner_type_creative(config, access_token=access_token,
                                                           creative_id=response.json()['id'],
                                                           creative_data=banner_creative_update_data)

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(response.json()['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == banner_creative_update_data['title']
    assert user_id == banner_creative_creation_data['userId']
    assert creative_set_id == banner_creative_creation_data['creativeSetId']
    assert type_id == 1
    assert subtype_id == 1
    assert is_reserved == 0
    assert status == 10
    assert width == 0
    assert height == 0

    # GET CREATIVE LIST
    with open('assets/creative/get_banner_creative_list_data.json') as json_file:
        get_banner_creative_list_data = json.load(json_file)
    get_response = Creative.get_banner_type_creative_list(config, access_token=access_token,
                                                          creative_data=get_banner_creative_list_data)

    for i, item in enumerate(get_response.json()['data']):
        if item["id"] == response.json()['id']:
            index = i
            break
    assert get_response.json()['data'][index]['id'] == response.json()['id']
    assert get_response.json()['data'][index]['title'] == banner_creative_update_data['title']
    assert get_response.json()['data'][index]['type_id'] == 1
    assert get_response.json()['data'][index]['width'] == 0
    assert get_response.json()['data'][index]['height'] == 0
    assert get_response.json()['data'][index]['assets'] == []
    assert get_response.json()['current_page'] == get_banner_creative_list_data['page']
    assert get_response.json()['from'] == 1
    assert get_response.json()['next_page_url'] is None or next_page_url
    assert get_response.json()['path'] == path
    assert get_response.json()['per_page'] == 15
    assert get_response.json()['to'] == len(get_response.json()['data'])
    assert get_response.json()['prev_page_url'] is None

    # DELETE CREATIVE
    delete_response = Creative.delete_banner_type_creative(config, access_token=access_token,
                                                           creative_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(response.json()['id'])

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == banner_creative_update_data['title']
    assert user_id == banner_creative_creation_data['userId']
    assert creative_set_id == banner_creative_creation_data['creativeSetId']
    assert type_id == 1
    assert subtype_id == 1
    assert is_reserved == 0
    assert status == 0
    assert width == 0
    assert height == 0

    # ERROR RESPONSE
    response = Creative.create_creative(config, access_token=access_token, creative_data=banner_creative_creation_data,
                                        error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"

    response = Creative.create_creative(config, access_token=access_token, creative_data=banner_creative_creation_data)
    update_response = Creative.update_banner_type_creative(config, access_token=access_token,
                                                           creative_data=banner_creative_update_data,
                                                           creative_id=(response.json())['id'],
                                                           error_response_check=True)
    assert update_response.status_code == 400
    assert (update_response.json())['error'] == "Bad request"

    get_response = Creative.get_banner_type_creative_list(config, access_token=access_token,
                                                          creative_data=get_banner_creative_list_data,
                                                          error_response_check=True)
    assert get_response.status_code == 400
    assert (get_response.json())['error'] == "Bad request"

    delete_response = Creative.delete_banner_type_creative(config, access_token=access_token,
                                                           creative_id=(response.json())['id'],
                                                           error_response_check=True)
    assert delete_response.status_code == 400

    # INVALID RESPONSE
    banner_creative_creation_data['userId'] = 8736836587368563846385682368
    banner_creative_creation_data['creativeSetId'] = 64613
    invalid_response = Creative.create_creative(config, access_token=access_token,
                                                creative_data=banner_creative_creation_data)
    assert invalid_response.status_code == 400
    assert (invalid_response.json())[
               'error'] == "The given data was invalid.  Invalid user ID. Invalid creatives set ID."

    del (banner_creative_creation_data['userId'])
    del (banner_creative_creation_data['creativeSetId'])
    del (banner_creative_creation_data['title'])
    invalid_response = Creative.create_creative(config, access_token=access_token,
                                                creative_data=banner_creative_creation_data)
    assert invalid_response.status_code == 400
    assert (invalid_response.json())[
               'error'] == "The given data was invalid.  The user id field is required.. The title" \
                           " field is required.. The creative set id field is required.."

    del (banner_creative_update_data['title'])
    invalid_response = Creative.update_banner_type_creative(config, access_token=access_token,
                                                            creative_id=response.json()['id'],
                                                            creative_data=banner_creative_update_data)
    assert invalid_response.status_code == 400
    assert (invalid_response.json())[
               'error'] == "The given data was invalid.  The title field is required.."


def test_create_edit_and_delete_native_type_creative(setup):
    config, access_token = setup

    with open('assets/creative/native_creative_creation_data.json') as json_file:
        native_creative_creation_data = json.load(json_file)
    native_creative_creation_data['title'] = native_creative_creation_data['title'] + Creative.get_random_string(5)

    # CREATE CREATIVE
    response = Creative.create_creative(config, access_token=access_token, creative_data=native_creative_creation_data)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'

    assert response.status_code == 200

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(response.json()['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == native_creative_creation_data['title']
    assert user_id == native_creative_creation_data['userId']
    assert creative_set_id == native_creative_creation_data['creativeSetId']
    assert type_id == 2
    assert subtype_id == 0
    assert is_reserved == 0
    assert status == 10
    assert width == 0
    assert height == 0

    # UPDATE CREATIVE
    with open('assets/creative/banner_creative_update_data.json') as json_file:
        native_creative_update_data = json.load(json_file)
    native_creative_update_data['title'] = native_creative_update_data[
                                               'title'] + Creative.get_random_string(5)
    update_response = Creative.update_banner_type_creative(config, access_token=access_token,
                                                           creative_id=response.json()['id'],
                                                           creative_data=native_creative_update_data)

    assert update_response.headers['Server'] == 'nginx'
    assert update_response.headers['Content-Type'] == 'application/json'
    assert update_response.headers['Transfer-Encoding'] == 'chunked'
    assert update_response.headers['Cache-Control'] == 'no-cache, private'
    assert update_response.headers['Content-Encoding'] == 'gzip'

    assert update_response.status_code == 200
    assert (update_response.json())['success'] is True

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(response.json()['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == native_creative_update_data['title']
    assert user_id == native_creative_creation_data['userId']
    assert creative_set_id == native_creative_creation_data['creativeSetId']
    assert type_id == 2
    assert subtype_id == 0
    assert is_reserved == 0
    assert status == 10
    assert width == 0
    assert height == 0

    # DELETE CREATIVE
    delete_response = Creative.delete_banner_type_creative(config, access_token=access_token,
                                                           creative_id=(response.json())['id'])
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(response.json()['id'])

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == native_creative_update_data['title']
    assert user_id == native_creative_creation_data['userId']
    assert creative_set_id == native_creative_creation_data['creativeSetId']
    assert type_id == 2
    assert subtype_id == 0
    assert is_reserved == 0
    assert status == 0
    assert width == 0
    assert height == 0


def test_upload_creative_asset_of_banner_type(setup):
    config, access_token = setup

    with open('assets/creative/banner_creative_creation_data.json') as json_file:
        banner_creative_creation_data = json.load(json_file)
    banner_creative_creation_data['title'] = banner_creative_creation_data['title'] + Creative.get_random_string(5)

    response = Creative.create_creative(config, access_token=access_token, creative_data=banner_creative_creation_data)

    base = Creative.base64_encoder('assets/creative/creative_files/banner_file.zip')
    with open('assets/creative/banner_creative_upload_data.json') as json_file:
        banner_creative_upload_data = json.load(json_file)
    banner_creative_upload_data['creativeId'] = int(response.json()['id'])
    banner_creative_upload_data['creativeFile'] = base

    upload_response = Creative.upload_creative_asset_of_banner_type(config, access_token,
                                                                    creative_data=banner_creative_upload_data)
    assert upload_response.status_code == 200
    assert (upload_response.json())['success'] is True

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(response.json()['id'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == banner_creative_creation_data['title'] + "_128x128"
    assert user_id == banner_creative_creation_data['userId']
    assert creative_set_id == banner_creative_creation_data['creativeSetId']
    assert type_id == 1
    assert subtype_id == 1
    assert is_reserved == 0
    assert status == 2
    assert width == 128
    assert height == 128

    db_results = CreativeUtils.pull_creative_data_from_creative_assets_db_table(
        banner_creative_upload_data['creativeId'])

    assert db_results[0]['parent_id'] == 0
    assert db_results[0]['creative_id'] == banner_creative_upload_data['creativeId']
    assert db_results[0]['asset_key'] == 'image'
    data = json.loads(db_results[0]['asset_value'])
    assert data['width'] == 128
    assert data['height'] == 128
    assert db_results[0]['status'] == 10
    assert db_results[0]['fixed'] == 0

    created_at = db_results[0]['created_at']
    updated_at = db_results[0]['updated_at']
    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]

    # DELETE CREATED CREATIVE
    delete_response = Creative.delete_banner_type_creative(config, access_token=access_token,
                                                           creative_id=(banner_creative_upload_data['creativeId']))
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    # ERROR RESPONSE
    upload_response = Creative.upload_creative_asset_of_banner_type(config, access_token,
                                                                    creative_data=banner_creative_upload_data,
                                                                    error_response_check=True)
    assert upload_response.status_code == 400
    assert (upload_response.json())['error'] == "Bad request"

    del (banner_creative_upload_data['creativeId'])
    del (banner_creative_upload_data['creativeFile'])
    upload_response = Creative.upload_creative_asset_of_banner_type(config, access_token,
                                                                    creative_data=banner_creative_upload_data)
    assert upload_response.status_code == 400
    assert (upload_response.json())[
               'error'] == "The given data was invalid.  The creative id field is required.. " \
                           "The creative file field is required.."


def test_upload_creative_asset_of_native_type_with_mandatory_and_optional_param(setup):
    config, access_token = setup

    asset_keys = ['native_content', 'native_icon', 'native_image_600x600', 'native_image_main']
    with open('assets/creative/native_creative_creation_data.json') as json_file:
        native_creative_creation_data = json.load(json_file)
    native_creative_creation_data['title'] = native_creative_creation_data['title'] + Creative.get_random_string(5)

    creative_response = Creative.create_creative(config, access_token=access_token,
                                                 creative_data=native_creative_creation_data)

    banner_file_base = Creative.base64_encoder('assets/creative/creative_files/banner_file.zip')
    native_main_image_base = Creative.base64_encoder('assets/creative/creative_files/native_main_image.zip')

    with open('assets/creative/native_creative_upload_data.json') as json_file:
        native_creative_upload_data = json.load(json_file)
    native_creative_upload_data['creativeId'] = int(creative_response.json()['id'])
    native_creative_upload_data['iconFile'] = banner_file_base
    native_creative_upload_data['imageMainFile'] = native_main_image_base
    native_creative_upload_data['image600x600File'] = native_main_image_base

    upload_response = Creative.upload_creative_asset_of_native_type(config, access_token,
                                                                    creative_data=native_creative_upload_data)
    assert upload_response.status_code == 200
    assert (upload_response.json())['success'] is True

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(native_creative_upload_data['creativeId'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == native_creative_creation_data['title']
    assert user_id == native_creative_creation_data['userId']
    assert creative_set_id == native_creative_creation_data['creativeSetId']
    assert type_id == 2
    assert subtype_id == 0
    assert is_reserved == 0
    assert status == 10
    assert width == 600
    assert height == 600

    db_results = CreativeUtils.pull_creative_data_from_creative_assets_db_table(
        native_creative_upload_data['creativeId'])

    for i in range(0, 3):
        assert db_results[i]['parent_id'] == 0
    for i in range(0, 3):
        assert db_results[i]['creative_id'] == native_creative_upload_data['creativeId']
    for i in range(0, 3):
        assert db_results[i]['asset_key'] in asset_keys
    for i in range(0, 3):
        if db_results[i]['asset_key'] == 'native_content':
            data = json.loads(db_results[i]['asset_value'])
            assert data['title'] == native_creative_upload_data['content']['title']
            assert data['desc'] == native_creative_upload_data['content']['desc']
            assert data['desc2'] == native_creative_upload_data['content']['desc2']
            assert data['cta'] == native_creative_upload_data['content']['cta']
            assert data['sponsored'] == native_creative_upload_data['content']['sponsored']
            assert data['likes'] == native_creative_upload_data['content']['likes']
            assert data['downloads'] == native_creative_upload_data['content']['downloads']
            assert data['price'] == native_creative_upload_data['content']['price']
            assert data['sale_price'] == native_creative_upload_data['content']['sale_price']
            assert data['phone'] == native_creative_upload_data['content']['phone']
            assert data['address'] == native_creative_upload_data['content']['address']
            assert data['rating'] == native_creative_upload_data['content']['rating']
            assert data['display_url'] == native_creative_upload_data['content']['display_url']
        elif db_results[i]['asset_key'] == 'native_icon':
            data = json.loads(db_results[i]['asset_value'])
            assert data['width'] == 128
            assert data['height'] == 128
        elif db_results[i]['asset_key'] == 'native_image_600x600':
            data = json.loads(db_results[i]['asset_value'])
            assert data['width'] == 600
            assert data['height'] == 600
        else:
            data = json.loads(db_results[i]['asset_value'])
            assert data['width'] == 600
            assert data['height'] == 600
    for i in range(0, 3):
        assert db_results[i]['status'] == 10
    for i in range(0, 3):
        assert db_results[i]['fixed'] == 0
    for i in range(0, 3):
        created_at = db_results[i]['created_at']
        updated_at = db_results[i]['updated_at']
        created_at = str(created_at).split(' ')
        updated_at = str(updated_at).split(' ')
        assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at
        assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at

    # DELETE CREATED CREATIVE
    delete_response = Creative.delete_banner_type_creative(config, access_token=access_token,
                                                           creative_id=(native_creative_upload_data['creativeId']))
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True

    # ERROR RESPONSE
    upload_response = Creative.upload_creative_asset_of_native_type(config, access_token,
                                                                    creative_data=native_creative_upload_data,
                                                                    error_response_check=True)
    assert upload_response.status_code == 400
    assert (upload_response.json())['error'] == "Bad request"

    del (native_creative_upload_data['creativeId'])
    del (native_creative_upload_data['iconFile'])
    del (native_creative_upload_data['imageMainFile'])
    del (native_creative_upload_data['image600x600File'])
    del (native_creative_upload_data['content']['title'])
    upload_response = Creative.upload_creative_asset_of_native_type(config, access_token,
                                                                    creative_data=native_creative_upload_data)
    assert upload_response.status_code == 400
    assert (upload_response.json())['error'] == "The given data was invalid.  The creative id field is " \
                                                "required.. The icon file field is required.." \
                                                " The image main file field is required.. The image600x600 " \
                                                "file field is required.. The content.title field is required.."


def test_upload_creative_asset_of_native_type_with_mandatory_param(setup):
    config, access_token = setup

    asset_keys = ['native_content', 'native_icon', 'native_image_600x600', 'native_image_main']
    with open('assets/creative/native_creative_creation_data.json') as json_file:
        native_creative_creation_data = json.load(json_file)
    native_creative_creation_data['title'] = native_creative_creation_data['title'] + Creative.get_random_string(5)
    del (native_creative_creation_data['content']['desc'])
    del (native_creative_creation_data['content']['desc2'])
    del (native_creative_creation_data['content']['cta'])
    del (native_creative_creation_data['content']['sponsored'])
    del (native_creative_creation_data['content']['likes'])
    del (native_creative_creation_data['content']['downloads'])
    del (native_creative_creation_data['content']['price'])
    del (native_creative_creation_data['content']['sale_price'])
    del (native_creative_creation_data['content']['phone'])
    del (native_creative_creation_data['content']['address'])
    del (native_creative_creation_data['content']['rating'])
    del (native_creative_creation_data['content']['display_url'])

    creative_response = Creative.create_creative(config, access_token=access_token,
                                                 creative_data=native_creative_creation_data)

    banner_file_base = Creative.base64_encoder('assets/creative/creative_files/banner_file.zip')
    native_main_image_base = Creative.base64_encoder('assets/creative/creative_files/native_main_image.zip')

    with open('assets/creative/native_creative_upload_data.json') as json_file:
        native_creative_upload_data = json.load(json_file)
    native_creative_upload_data['creativeId'] = int(creative_response.json()['id'])
    native_creative_upload_data['iconFile'] = banner_file_base
    native_creative_upload_data['imageMainFile'] = native_main_image_base
    native_creative_upload_data['image600x600File'] = native_main_image_base

    upload_response = Creative.upload_creative_asset_of_native_type(config, access_token,
                                                                    creative_data=native_creative_upload_data)
    assert upload_response.status_code == 200
    assert (upload_response.json())['success'] is True

    title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, updated_at = \
        CreativeUtils.pull_creative_data_from_db(native_creative_upload_data['creativeId'], db_close=False)

    created_at = str(created_at).split(' ')
    updated_at = str(updated_at).split(' ')
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at[0]
    assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at[0]
    assert title == native_creative_creation_data['title']
    assert user_id == native_creative_creation_data['userId']
    assert creative_set_id == native_creative_creation_data['creativeSetId']
    assert type_id == 2
    assert subtype_id == 0
    assert is_reserved == 0
    assert status == 10
    assert width == 600
    assert height == 600

    db_results = CreativeUtils.pull_creative_data_from_creative_assets_db_table(
        native_creative_upload_data['creativeId'])

    for i in range(0, 3):
        assert db_results[i]['parent_id'] == 0
    for i in range(0, 3):
        assert db_results[i]['creative_id'] == native_creative_upload_data['creativeId']
    for i in range(0, 3):
        assert db_results[i]['asset_key'] in asset_keys
    for i in range(0, 3):
        if db_results[i]['asset_key'] == 'native_content':
            data = json.loads(db_results[i]['asset_value'])
            assert data['title'] == native_creative_upload_data['content']['title']
            assert data['desc'] == ""
            assert data['desc2'] == ""
            assert data['cta'] == ""
            assert data['sponsored'] == ""
            assert data['likes'] == ""
            assert data['downloads'] == ""
            assert data['price'] == ""
            assert data['sale_price'] == ""
            assert data['phone'] == ""
            assert data['address'] == ""
            assert data['rating'] == ""
            assert data['display_url'] == ""
        elif db_results[i]['asset_key'] == 'native_icon':
            data = json.loads(db_results[i]['asset_value'])
            assert data['width'] == 128
            assert data['height'] == 128
        elif db_results[i]['asset_key'] == 'native_image_600x600':
            data = json.loads(db_results[i]['asset_value'])
            assert data['width'] == 600
            assert data['height'] == 600
        else:
            data = json.loads(db_results[i]['asset_value'])
            assert data['width'] == 600
            assert data['height'] == 600
    for i in range(0, 3):
        assert db_results[i]['status'] == 10
    for i in range(0, 3):
        assert db_results[i]['fixed'] == 0
    for i in range(0, 3):
        created_at = db_results[i]['created_at']
        updated_at = db_results[i]['updated_at']
        created_at = str(created_at).split(' ')
        updated_at = str(updated_at).split(' ')
        assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == created_at
        assert Creative.get_specific_date_with_specific_format('%Y-%m-%d') == updated_at

    # DELETE CREATED CREATIVE
    delete_response = Creative.delete_banner_type_creative(config, access_token=access_token,
                                                           creative_id=(native_creative_upload_data['creativeId']))
    assert delete_response.status_code == 200
    assert (delete_response.json())['success'] is True
