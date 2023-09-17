import json
import requests

from configurations import configurations

config = configurations.load_config_by_usertype()

MYSQL_MAX_RETRY = int(config['mysql']['max-retry'])
MYSQL_WAIT_TIME = int(config['mysql']['wait'])


def get_api_access_token(base_url, end_point, credential):
    payload = {
        'grant_type': 'eskimi_dsp',
        'username': credential['username'],
        'password': credential['password'],
        'client_id': int(credential['client-id']),
        'client_secret': credential['client-secret']
    }
    headers = {'content-type': 'application/json'}
    response = json.loads(
        requests.request('POST', '{}{}'.format(base_url, end_point), data=json.dumps(payload), headers=headers).text)
    return response['access_token']
