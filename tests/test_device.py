import json

from pages.device import Device
from utils.device import DeviceUtils


def test_device_brand(setup):
    config, access_token = setup
    next_page_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['device_brands'], '?page=2')
    prev_page_url = None
    response = Device.get_device_brands(config, access_token=access_token)
    device_brand_list = DeviceUtils.pull_device_page_list_item_from_db()
    device_brand_list = Device.ordered(device_brand_list)
    json_data = Device.ordered(response.json()['data'])
    assert json_data == device_brand_list
    assert response.json()['next_page_url'] == next_page_url
    assert response.json()['prev_page_url'] == prev_page_url
    assert response.json()["current_page"] == 1
    # ERROR RESPONSE
    response = Device.get_device_brands(config, access_token=access_token,
                                        error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_brands_custom(setup):
    config, access_token = setup

    next_page_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['device_brands'], '?page=4')
    prev_page_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['device_brands'], '?page=2')
    path = '{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                           config['api']['device_brands'])
    current_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['device_brands'], '?page=3')
    with open('assets/device/device_page_data.json') as json_file:
        device_brand_page = json.load(json_file)

    response = Device.get_device_brands_custom(config, access_token=access_token, brand_page=device_brand_page)
    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200

    assert response.json()["current_page"] == 3
    assert response.json()["per_page"] == 1
    assert response.json()['from'] == 3
    assert response.json()['links'][3]['active'] == True
    assert response.json()['links'][2]['active'] == False
    assert response.json()['links'][14]['active'] == False
    assert response.json()['links'][3]['label'] == "3"
    assert response.json()['links'][0]['label'] == "&laquo; Previous"
    assert response.json()['links'][14]['label'] == "Next &raquo;"
    assert response.json()['links'][3]['url'] == current_url
    assert response.json()['links'][0]['url'] == prev_page_url
    assert response.json()['links'][14]['url'] == next_page_url
    assert response.json()['next_page_url'] == next_page_url
    assert response.json()['prev_page_url'] == prev_page_url
    assert response.json()['path'] == path
    device_total_count_from_db = DeviceUtils.pull_total_device_count_from_db()
    assert response.json()["total"] == device_total_count_from_db

    # ERROR RESPONSE
    response = Device.get_device_brands_custom(config, access_token=access_token,
                                               error_response_check=True, brand_page=device_brand_page)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_connections(setup):
    config, access_token = setup

    response = Device.get_device_connections(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    device_connection_list_from_db = DeviceUtils.pull_device_connections_from_db()
    json_data = Device.ordered(response.json())
    device_connection_list_from_db = Device.ordered(device_connection_list_from_db)
    assert json_data == device_connection_list_from_db
    # ERROR RESPONSE
    response = Device.get_device_connections(config, access_token=access_token,
                                             error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_oses(setup):
    config, access_token = setup

    response = Device.get_device_oses(config, access_token=access_token)

    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    device_oses_list_from_db = DeviceUtils.pull_device_oses_from_db()
    json_data = Device.ordered(response.json())
    device_oses_list_from_db = Device.ordered(device_oses_list_from_db)
    assert json_data == device_oses_list_from_db

    # ERROR RESPONSE
    response = Device.get_device_oses(config, access_token=access_token,
                                      error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_types(setup):
    config, access_token = setup
    response = Device.get_device_types(config, access_token=access_token)
    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.headers['Content-Encoding'] == 'gzip'
    assert response.status_code == 200
    device_types_list_from_db = DeviceUtils.pull_device_types_from_db()
    json_data = Device.ordered(response.json())
    device_types_list_from_db = Device.ordered(device_types_list_from_db)
    assert json_data == device_types_list_from_db
    # ERROR RESPONSE
    response = Device.get_device_types(config, access_token=access_token,
                                       error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_model(setup):
    config, access_token = setup
    next_page_url = '{}{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                        config['api']['device_model_by_bandID'], '5', '?page=2')
    prev_page_url = None
    path = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                             config['api']['device_model_by_bandID'], '5')
    """
    brandID = 5, 5 = apple mobile brand ID
    """
    response = Device.get_device_by_brandID(config, brandID=5, access_token=access_token)
    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'
    assert response.headers['Transfer-Encoding'] == 'chunked'
    assert response.headers['Cache-Control'] == 'no-cache, private'
    assert response.status_code == 200
    device_model_list_from_db = DeviceUtils.pull_device_model_from_db()
    device_brand_list = Device.ordered(device_model_list_from_db)
    json_data = Device.ordered(response.json()['data'])
    assert json_data == device_brand_list
    assert response.json()["current_page"] == 1
    assert response.json()["per_page"] == 15
    assert response.json()['from'] == 1
    assert response.json()['next_page_url'] == next_page_url
    assert response.json()['prev_page_url'] == prev_page_url
    assert response.json()['path'] == path
    # ERROR RESPONSE
    response = Device.get_device_by_brandID(config, brandID=5, access_token=access_token,
                                            error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
