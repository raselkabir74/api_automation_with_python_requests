import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules

connection = ''


class ExchangeUtils:
    @staticmethod
    def pull_exchange_data_from_db():
        attempts = 0
        db_result = None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT id, name FROM exchanges where status = 1 order by id asc'
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
