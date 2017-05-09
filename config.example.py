"""
example config file for `verify.py`

fill in the values below to run `verify.py successfully
"""
import requests

URL = {
    "staging": "staging environment url",
    "prod": "prod environment url"
}

API_CALL = get_data_from_api


def get_data_from_api(account_number, account_type):
    url = "{}/{}:{}".format(URL["staging"], account_type, account_number)
    return requests.get(url)


RESPONSE_KEYS = {}
