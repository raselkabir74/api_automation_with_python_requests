import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules

connection = ''


class SitesUtils:

    @staticmethod
    def pull_sites_platforms_data_from_db(db_close=True):
        global connection
        attempts = 0
        db_result = None
        formatted_data = []
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                if connection == '':
                    time.sleep(generic_modules.MYSQL_WAIT_TIME)
                    connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT id, title FROM sites_platforms'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"]}
                    formatted_data.append(entry_dict)
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return formatted_data
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    if db_close:
                        connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return formatted_data

    @staticmethod
    def pull_sites_types_data_from_db(db_close=True):
        global connection
        attempts = 0
        db_result = None
        formatted_data = []
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                if connection == '':
                    time.sleep(generic_modules.MYSQL_WAIT_TIME)
                    connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT id, title FROM sites_types'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"]}
                    formatted_data.append(entry_dict)
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return formatted_data
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    if db_close:
                        connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return formatted_data

    @staticmethod
    def pull_sites_data_from_db(db_close=True):
        global connection
        attempts = 0
        db_result = None
        formatted_data = []
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                if connection == '':
                    time.sleep(generic_modules.MYSQL_WAIT_TIME)
                    connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT id, site_name, site_domain FROM sites where exchange_id = 7 and ' \
                                       'status = 2 order by 1 asc'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["site_name"],
                                  "domain": db_result["site_domain"]}
                    formatted_data.append(entry_dict)
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return formatted_data
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    if db_close:
                        connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return formatted_data
