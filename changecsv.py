import csv

def reformat_name(name):
    parts = name.split()
    for i, part in enumerate(parts):
        if part.isupper():
            last_name = part
            first_name = ' '.join(parts[:i] + parts[i+1:])
            return f"{last_name} {first_name}"
    return name

input_file = 'scraped_data_with_pid.csv'    # Your input CSV file name
output_file = 'players.csv'  # Output CSV file name

with open(input_file, newline='', encoding='utf-8') as csvfile_in, \
     open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:

    reader = csv.DictReader(csvfile_in)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row['Name'] = reformat_name(row['Name'])
        writer.writerow(row)

print(f"Reformatted names written to {output_file}")
