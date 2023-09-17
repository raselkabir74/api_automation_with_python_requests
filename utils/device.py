import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules

connection = ''


class DeviceUtils:

    @staticmethod
    def pull_device_connections_from_db(db_close=True):
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
                    sql_select_query = 'SELECT id, title FROM device_connections WHERE enabled = "1"'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
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
    def pull_device_page_list_item_from_db(db_close=True):
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
                    sql_select_query = "SELECT id , title FROM device_brands WHERE enabled = '1' ORDER BY id ASC LIMIT 15"
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
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
    def pull_total_device_count_from_db(db_close=True):
        global connection
        attempts = 0
        total_count = 0
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                if connection == '':
                    time.sleep(generic_modules.MYSQL_WAIT_TIME)
                    connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = "SELECT COUNT(id) as Total FROM device_brands WHERE enabled = '1'"
                    cursor.execute(sql_select_query)
                    db_result = cursor.fetchone()
                    if db_result:
                        total_count = db_result["Total"]
                    connection.commit()
                if db_close:
                    connection.close()
                return total_count
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    if db_close:
                        connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return total_count  # Return zero if an error occurs or the count is not found

    @staticmethod
    def pull_device_oses_from_db(db_close=True):
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
                    sql_select_query = 'SELECT id, title FROM oses WHERE enabled = "1"'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
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
    def pull_device_types_from_db(db_close=True):
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
                    sql_select_query = 'SELECT id, title FROM device_types WHERE enabled = "1"'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
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

    def pull_device_model_from_db(db_close=True):
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
                    sql_select_query = "SELECT id , title FROM device_models WHERE device_brand_id = '5' and enabled = '1' ORDER BY title ASC LIMIT 15"
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                if db_close:
                    connection.close()
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
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
