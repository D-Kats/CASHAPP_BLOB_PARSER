# CASHAPP_BLOP_PARSER
A parser for the BLOB column (ZSYNCPAYMENT) of the "CCEntitySync-api-squareup.com.sqlite" database of the Cash App

## USAGE

Copy the sqlite db to the folder where the exe file is. Run the exe. A message will appear notifying about the outcome. A report.csv file will be created in case everything works fine. Add the csv to an excel spreadsheet with UTF-8 encoding and set TAB as a delimiter. All the timestamps have been converted to UTC timezone. In case a key (csv header) is not found in on of the parsed BLOBs, the "KEY NOT FOUND" value will be written in the final csv report.

## ERROR

In case of an error a log file will be created, named either JSONError.log that has to do with the parsing of the blob itself or error.log which has to do with the parsing of each individual key (header) of the exported csv file. In the first case, no report file will be created and in the second one a partially filled report containing just the fields that were parsed till the point the error occured.

