import os
import configparser
import hvac

config = configparser.RawConfigParser()
config.read(['global.ini', 'local.ini', 'local_generated.ini'])


def get_credential_by_user_type(user_type):
    client = hvac.Client(url=config['vault']['url'])
    client.auth.approle.login(os.environ['APPROLE_ROLE_ID'], os.environ['APPROLE_SECRET_ID'])
    secret_version_response = client.secrets.kv.v2.read_secret_version(
        mount_point=config['vault']['mount-point'],
        path=config['user-by-types-secret-path'][user_type]
    )
    return secret_version_response['data']['data']
