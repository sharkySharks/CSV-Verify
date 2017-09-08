# CSV-Verify

### Validate CSV File Data Against API Response

Python module to read data from a CSV file and write validation responses to an output CSV file with results appended to each row.

This was written with a specific use case: given a CSV file with n rows, validate that the correct data for an account is returned from an API, as per the CSV file. While this is a specific use case, this module can be adapted for any kind of mass data validation against an API call.

For my use case, the CSV file is expected to be formatted as follows:

    [Col 1]         [Col 2]             [Col 3]         [Col 4]
    Account #       data_to_verify      Account Type    CSV File Name

#### Initial Setup 

Use a virtual environment to run Python3. From the root of this repo, run the following:
```
virtualenv -p python3 ENV
source ENV/bin/activate
pip install -r requirements.txt
```

In order to run `verify.py` successfully, a `config.py` file needs to be created. Copy `config.example.py` as `config.py` and fill it in with your specific values. See `config.example.py` for more details on setting up the config file. 

#### Executing

Run `python verify.py` to start the script on the command line. 

It will first prompt for the `input CSV file`, this is the file that you want to test. Make sure the columns are in the format discussed above, or change the script to suit your needs. **Save the `input CSV file` under the `input_csv_files/` folder.**

The second prompt will ask for the `output CSV file` name and full extension. No need to create this file before running the script, just provide a name, EX: `test_output.csv`, and it will be saved under the `output_results/` folder.

The third and final prompt will ask for the environment you want to test in, which is set in the config file. See `config.example.py` to set up properly.

#### File Structure

```
verify_tiers
├── config.example.py           # config template
├── config.py                   # config file used to run script
├── input_csv_files
│   └── example_input.csv       # put CSV file to test here
├── output_results
│   └── example_output.csv      # output dropped in here
└── verify.py                   # main file to execute
```


