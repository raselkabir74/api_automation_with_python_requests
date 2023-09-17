import os
from functools import lru_cache

import hvac
import pymysql
from sshtunnel import SSHTunnelForwarder

from configurations import configurations

config = configurations.load_config_by_usertype()

ssh_service = None


def is_jenkins():
    return os.environ.get('JENKINS_HOME') is not None


def set_tunnel(service):
    global ssh_service
    ssh_service = SSHTunnelForwarder(
        config['mysql-hosts']['ssh-host'],
        ssh_username=config['mysql']['ssh-user'],
        remote_bind_address=(config['mysql-hosts']['{}'.format(service)], 3306)
    )
    ssh_service.start()
    print('Setting up SSH tunnel on port {}'.format(ssh_service.local_bind_port))
    return ssh_service.local_bind_port


def destroy_tunnel():
    global ssh_service
    ssh_service.stop()


def connection_test(connection):
    try:
        with connection.cursor() as cursor:
            sql_select_query = 'SELECT VERSION()'
            cursor.execute(sql_select_query)
            connection.commit()
            result = cursor.fetchone()
            if len(result.keys()):
                print('Connection Success')
                connected = True
    except Exception as e:
        pass
    finally:
        try:
            connection.close()
            destroy_tunnel()
        except Exception as e:
            pass
        return not connected


@lru_cache(maxsize=1)
def mysql_connection_test():
    stage = connection_test(get_mysql_client())
    prod = connection_test(get_production_mysql_client())
    return stage and prod


@lru_cache(maxsize=1)
def get_mysql_credentials():
    if "JENKINS_URL" in os.environ:
        client = hvac.Client(url=config['vault']['url'])
        client.auth.approle.login(os.environ['APPROLE_ROLE_ID'], os.environ['APPROLE_SECRET_ID'])
        secret_version_response = client.secrets.kv.v2.read_secret_version(
            mount_point=config['vault']['mount-point'],
            path=config['vault']['mysql-path'],
        )
        mysql_credentials = {
            'username': secret_version_response['data']['data']['user_name'],
            'password': secret_version_response['data']['data']['user_pass']
        }
    else:
        mysql_credentials = {
            'username': config['mysql_credentials']['username'],
            'password': config['mysql_credentials']['password']
        }
    return mysql_credentials


def get_mysql_client():
    mysql_credentials = get_mysql_credentials()
    connection = pymysql.connect(host=config['mysql-hosts']['stage-mysql-host'],
                                 user=mysql_credentials['username'],
                                 password=mysql_credentials['password'],
                                 db=config['mysql']['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection


def get_production_mysql_client():
    mysql_credentials = get_mysql_credentials()
    connection = pymysql.connect(host=config['mysql-hosts']['master-mysql-host'],
                                 user=mysql_credentials['username'],
                                 password=mysql_credentials['password'],
                                 db=config['mysql']['db'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection
