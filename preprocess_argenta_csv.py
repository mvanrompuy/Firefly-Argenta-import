import argparse
import csv
import os

def file_path(string):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), string))
    if os.path.isfile(path):
        return path
    else:
        raise FileNotFoundError(string)

def output_file_path(path):
    filepath, extension = os.path.splitext(path)
    return f"{filepath}_clean{extension}"

parser = argparse.ArgumentParser(description='Preprocess CSV file exported from Argent for usage in Firefly III CSV import tool.')
parser.add_argument('--path', type=file_path, help='Path of CSV input file')

args = parser.parse_args()

path = args.path
expected_header = ['Rekening', 'Boekdatum', 'Valutadatum', 'Referentie', 'Beschrijving', 'Bedrag', 'Munt', 'Verrichtingsdatum', 'Rekening tegenpartij', 'Naam tegenpartij', 'Mededeling']

# Cleanup CSV
# - Strip any leading whitespace
# - Remove duplicate source and destination for administrative costs
# - Replace 'Inkomende overschrijving' en 'Uitgaande overschrijving' with 'Overschrijving' to allow duplicate detection to work (+ direction is clear from source and destination anyway).
with open(path, 'r', encoding='utf-8-sig', newline='') as f_csv_input, open(output_file_path(path), 'w', encoding='utf-8-sig', newline='') as f_csv_output:
    # CSV reader for excel CSV file
    reader = csv.DictReader(f_csv_input, dialect='excel', delimiter=';', skipinitialspace=True)

    # Check the header fieldnames
    if (reader.fieldnames != expected_header):
        print(f"[FATAL] Unexpected header found '{reader.fieldnames}'!")
        raise RuntimeError

    writer = csv.DictWriter(f_csv_output, fieldnames=expected_header, dialect='excel', delimiter=';')
    writer.writeheader()

    # Process each row
    for row in reader:
        # Argenta presents internal tranasaction (administrative costs) as an outgoing transaction
        # from and to the same account (ignore whitespaces in account number).
        # Fix: remove duplicate IBAN (destination) and set Argenta as destination name (instead of ' ')
        if "".join(row['Rekening'].split()) == "".join(row['Rekening tegenpartij'].split()):
            row['Rekening tegenpartij'] = ''
            row['Naam tegenpartij'] = 'Argenta Spaarbank N.V.'

        if row['Beschrijving'].strip().lower() in ['inkomende overschrijving', 'uitgaande overschrijving']:
            row['Beschrijving'] = 'Overschrijving'

        writer.writerow(row)


