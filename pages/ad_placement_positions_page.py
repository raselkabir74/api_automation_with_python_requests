import requests
from pages.base_page import BasePage


class AdPlacementPosition(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_ad_placement_positions(config, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['ad_placement_positions'], "error")
        else:
            api_url = '{}{}{}'.format(config['credential']['api-url'], config['api']['v1'],
                                      config['api']['ad_placement_positions'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
