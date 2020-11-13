# Firefly III Argenta CSV importer

A small script to cleanup the CSV that can be extracted from the bank accounts of
the Belgian bank Argenta (for usage in the Firefly CSV import tool). By default this exported data contains the following issues:

- Transfers from and to the same account are listed. These are administrative costs the bank charges and for some reason records as a negative transfer
  to your own account. This script fixes this by removing the duplicate IBAN in the destination field and adding the bank's name in the destination name field instead.
- The 'Beschrijving' field details the direction of a transfer ('Uitgaande overschrijving' en 'Inkomende overschrijving'). If you do a transfer from your checking account to
  your savings account the outgoing transaction and incoming transfer will get a different value. This causes the Firefly CSV importer to wrongfully assume the transactions are
  not related (duplicates). To fix this, the script will replace 'Ingaande/Uitgaande overschrijving' with 'Overschrijving'.

## Exporting a CSV

Login on the online portal, select an account, and download your transactions by clicking the corresponding button.

**Note!**: For some reason, the export button will only trigger a download of max 250 rows. You'll have to repeat this download
step for multiple smaller ranges and bundle the output files afterwards to get an complete export.**

## Cleaning up the CSV

Run (using python3.6 or higher):

python3 preprocess_argenta_csv.py --path #path_to_csv_file#

The output file will be created in the same location with '_clean' appended to the filename.