import base64
import uuid
import datetime as dt

""" This class is the parent of all pages """
""" It contains all the generic methods and functionalities available to all the pages """


class BasePage:

    def __init__(self, config):
        self.driver = config

    @staticmethod
    def get_random_string(length=10):
        return uuid.uuid4().hex[:length]

    @staticmethod
    def base64_encoder(path_to_file):
        with open(path_to_file, 'rb') as zip_file:
            zip_data = zip_file.read()
        base64_encoded_data = base64.b64encode(zip_data).decode('utf-8')
        return base64_encoded_data

    @staticmethod
    def get_specific_date_with_specific_format(date_format, days_to_add=0, days_to_subtract=0):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        expected_date = None
        if days_to_add != 0:
            expected_date = dt.datetime.today() + dt.timedelta(days=days_to_add)
        elif days_to_subtract != 0:
            expected_date = dt.datetime.today() - dt.timedelta(days=days_to_subtract)
        elif days_to_add == 0 and days_to_subtract == 0:
            expected_date = dt.datetime.today()
        date1 = expected_date.strftime(date_format)
        return str(date1)

    @staticmethod
    def ordered(data_list):
        return sorted(data_list, key=lambda x: x["id"])
