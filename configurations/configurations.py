import configparser
import os

import secrets

global credential


def load_config_by_usertype(user_type='admin'):
    global credential
    if "JENKINS_URL" in os.environ:
        credential = secrets.get_credential_by_user_type(user_type)
    config = configparser.RawConfigParser()
    config.read(['global.ini', 'local.ini', 'local_generated.ini'])
    if "JENKINS_URL" in os.environ:
        for key in credential.keys():
            config['credential'][key.replace('_', '-')] = credential[key]
    return config
