import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules

connection = ''


class CreativeUtils:

    @staticmethod
    def pull_creative_set_data_from_db(creative_set_id, db_close=True):
        global connection
        attempts = 0
        db_result = None
        title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, \
            created_at, updated_at = None, None, None, None, None, None, None, None, None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                if connection == '':
                    time.sleep(generic_modules.MYSQL_WAIT_TIME)
                    connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT * FROM `creative_sets` WHERE id = {}'.format(creative_set_id)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    title = db_result['title']
                    user_id = db_result['user_id']
                    creative_type_id = db_result['creative_type_id']
                    creative_count = db_result['creative_count']
                    duplicate_count = db_result['duplicate_count']
                    is_reserved = db_result['is_reserved']
                    status = db_result['status']
                    created_at = db_result['created_at']
                    updated_at = db_result['updated_at']
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, \
                        status, created_at, updated_at
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    if db_close:
                        connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, \
            status, created_at, updated_at

    @staticmethod
    def pull_creative_data_from_db(creative_id, db_close=True):
        global connection
        attempts = 0
        db_result = None
        title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, \
            updated_at = None, None, None, None, None, None, None, None, None, None, None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                if connection == '':
                    time.sleep(generic_modules.MYSQL_WAIT_TIME)
                    connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT * FROM `creatives` WHERE id = {}'.format(creative_id)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    title = db_result['title']
                    user_id = db_result['user_id']
                    creative_set_id = db_result['creative_set_id']
                    type_id = db_result['type_id']
                    subtype_id = db_result['subtype_id']
                    is_reserved = db_result['is_reserved']
                    status = db_result['status']
                    width = db_result['width']
                    height = db_result['height']
                    created_at = db_result['created_at']
                    updated_at = db_result['updated_at']
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, \
                        created_at, updated_at
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    if db_close:
                        connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, \
            created_at, updated_at

    @staticmethod
    def pull_creative_data_from_creative_assets_db_table(creative_id, db_close=True):
        global connection
        attempts = 0
        db_result = None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                if connection == '':
                    time.sleep(generic_modules.MYSQL_WAIT_TIME)
                    connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT * FROM `creative_assets` WHERE creative_id = {}'.format(creative_id)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return db_results
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    if db_close:
                        connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return db_results
