import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules

connection = ''


class CampaignUtils:
    @staticmethod
    def pull_campaign_id_from_db(campaign_name):
        attempts = 0
        db_result = None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT id FROM campaigns where name like \'%{}%\' and user_id = 7722 ' \
                                       'and status = 0'.format(campaign_name)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_result = cursor.fetchall()
                connection.close()
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return db_result
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return db_result

    @staticmethod
    def pull_campaign_type_from_db(campaign_name):
        attempts = 0
        db_result = None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT type FROM campaigns where name like \'%{}%\' and user_id = 7722 ' \
                                       'and status = 0'.format(campaign_name)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_result = cursor.fetchall()
                connection.close()
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return db_result
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return db_result

    @staticmethod
    def pull_campaign_status_from_db(campaign_name):
        attempts = 0
        db_result = None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT status FROM campaigns where name like \'%{}%\' and user_id = 7722'.\
                        format(campaign_name)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_result = cursor.fetchall()
                connection.close()
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return db_result
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return db_result

    @staticmethod
    def pull_campaign_bid_from_db(campaign_name):
        attempts = 0
        db_result = None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT bid_currency FROM campaigns where name like \'%{}%\' and user_id = 7722 ' \
                                       'and status = 0'.format(campaign_name)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_result = cursor.fetchall()
                connection.close()
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return db_result
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return db_result
