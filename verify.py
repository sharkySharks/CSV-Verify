import csv
from http import HTTPStatus
import os

import requests

import config

"""
Validate CSV File Data Against API Response
Read data from CSV file and write validation response to output CSV file with
result appended to each row.
"""


def has_correct_status(response):
    """Validate correct response status"""
    if response.status_code == HTTPStatus.OK:
        return True
    else:
        return "Error: Incorrect status code returned: {}".format(response.status_code)


def is_correct_account(response, csv_account_number, csv_account_type):
    """Validate correct account"""
    response_account_id = response[config.RESPONSE_KEYS["id"]]

    if response_account_id == "{}:{}".format(csv_account_type, csv_account_number):
        return True
    else:
        return "Error: Incorrect number and/or type: {}, {}".format(response_account_id)


def is_correct_value(response, csv_data_to_verify):
    """Validate correct data against response"""
    response_data = response[config.RESPONSE_KEYS["s"]][config.RESPONSE_KEYS["data"]]

    if response_data == csv_data_to_verify:
        return True
    else:
        return "Error: Incorrect value returned: {}".format(response_data)


def verify(response, account_info):
    """
    `checks` values are tuples, with the first tuple value being a function
    and the second tuple value being params to execute the function
    """
    r_json = response.json()
    checks = {
        "1": (has_correct_status, {"response": response}),
        "2": (is_correct_account, {
                "response": r_json,
                "csv_account_number": account_info["csv_account_number"],
                "csv_account_type": account_info["csv_account_type"]
            }),
        "3": (is_correct_value, {
                "response": r_json,
                "csv_data_to_verify": account_info["csv_data_to_verify"]
            })
    }
    for k, v in checks.items():
        result = v[0](**v[1])
        if result is True:
            if k == "3":
                return "=)"
            else:
                continue
        else:
            return result


def verify_tiers(input_csv_file, output_csv_file, environment):
    """
    Validate data from CSV file
    :param: input_csv_file - csv file to be tested
    :param: output_csv_file - name for csv file to output, will be created
    """
    cwd = os.getcwd()

    input_file_path = "{}/input_csv_files/{}".format(cwd, input_csv_file)
    with open(input_file_path, "r") as file:
        reader = csv.reader(file, dialect="excel")
        for i, line in enumerate(reader, start=1):
            # Line read from CSV file
            print("Line [{}] : {}".format(i, line))

            account_info = {
                "csv_account_number": line[0],
                "csv_data_to_verify": line[1],
                "csv_account_type": "managed_hosting" if line[2].lower() == "dedicated" else line[2].lower(),
                "csv_file_name": line[3]
            }

            # Make API call with each row's account information
            response = config.API_CALL(account_info["csv_account_number"],
                                       account_info["csv_account_type"], environment)

            # Validate
            result = verify(response, account_info)

            # Create new result row, append outcome of verify result above
            RESULT_ROW = [
                account_info["csv_account_number"],
                account_info["csv_data_to_verify"],
                account_info["csv_account_type"],
                account_info["csv_file_name"]
            ]

            RESULT_ROW.append(result)

            # Result Row
            print("result row: {}".format(RESULT_ROW))

            # Write row result to output_results/<output.csv>
            output_file_path = "{}/output_results/{}".format(cwd, output_csv_file)
            with open(output_file_path, "a", newline='') as output_file:
                writer = csv.writer(output_file, dialect="excel")
                writer.writerow(RESULT_ROW)
                output_file.close()


def main():
    print("Input CSV file should be saved under `input_csv_files/` folder")
    input_csv_file = input("Enter CSV input file ----> ")
    print("Output files will be saved under `output_results/` folder")
    output_csv_file = input("Enter full name and file extension for output file ----> ")
    print("Which environment in your config file do you want to test in?")
    environment = input("Enter config environment you wish to test in ----> ")

    verify_tiers(input_csv_file, output_csv_file, environment)

if __name__ == "__main__":
    main()
