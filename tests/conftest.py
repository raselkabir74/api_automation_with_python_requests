import os

import pytest

from configurations import configurations, generic_modules

debug_mode = "JENKINS_URL" not in os.environ


@pytest.fixture
def setup(scope='session'):
    config = configurations.load_config_by_usertype()
    access_token = generic_modules.get_api_access_token(config['credential']['api-url'], config['api']['oauth'],
                                                        config['credential'])
    return config, access_token
