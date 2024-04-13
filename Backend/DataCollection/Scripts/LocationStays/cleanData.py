import csv

def csv_field_size_limit():
   csv.field_size_limit(2147483647)

def read_csv_file(file_path):
   with open(file_path, 'r', encoding='utf-8') as file:
       reader = csv.DictReader(file)
       return [row for row in reader]

def filter_unique_rows(data):
   unique_rows = {}
   for row in data:
       key = (
           row['Name'],
           row['geonameId'],
           row['Latitude'],
           row['Longitude'],
           row['First Order'],
           row['Second Order'],
           row['Third Order']
       )
       hotels = row['hotels']
       if key not in unique_rows and hotels != "[]":
           unique_rows[key] = row
       elif key in unique_rows and hotels != "[]" and unique_rows[key]['hotels'] == "[]":
           unique_rows[key] = row
   return list(unique_rows.values())

def write_csv_file(data, file_path):
   with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
       fieldnames = data[0].keys()
       writer = csv.DictWriter(output_file, fieldnames=fieldnames)
       writer.writeheader()
       for row in data:
           writer.writerow(row)

def main():
   csv_field_size_limit()
   input_file_path = '../allData/all_stays.csv'
   output_file_path = '../allData/all_unique_stays.csv'
   data = read_csv_file(input_file_path)
   unique_data = filter_unique_rows(data)
   write_csv_file(unique_data, output_file_path)
   print("\033[92mStay Data has been cleaned\033[0m")

if __name__ == "__main__":
   main()