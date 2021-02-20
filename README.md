# CASHAPP_BLOP_PARSER
A parser for the BLOB column (ZSYNCPAYMENT) of the "CCEntitySync-api-squareup.com.sqlite" database of the Cash App.

## USAGE

Run the exe and point it to the database file. Choose the output folder and parse. A report.csv file will be created in case everything worked fine.
Add the csv to an excel spreadsheet with UTF-8 encoding and set TAB as a delimiter. All the timestamps have been converted to human readable UTC timezone. In case a key (csv header) is not found in one of the parsed BLOBs, the "KEY NOT FOUND" value will be written in the final csv report.

## DATA 

The values that are being extracted from each BLOB of every record in the db are the following: Z_PK(not in the BLOB - Primary Key for identification of each recorded presented in the csv final report file), token, auth_token, role, amount (from amount key), currency code (from amount key), pull_amount, sender_payment_amount_in_default_currency, recipient_payment_amount_in_default_currency, state, note, instrument_type, transaction_id, created_at, captured_at, reached_customer_at, paid_out_at, deposited_at, display_date, token (from instrument key), card_brand (from instrument key), bank_name (from instrument key), display_name (from instrument key)


## ERROR

In case of an error the error console will log it to inform the user about the specific nature of it.

