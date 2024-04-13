import csv
import os
import shutil

def clear_folder(folder_name):
    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
            
def generate_example_queries(file_name, max_rows):
    count = 0
    query_number = 0

    with open(file_name, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            name = row["Name"]
            first_order = row["First Order"]
            count += 1

            if count > max_rows:
                count = 0
                query_number += 1
            with open(f"Queries/example-queries_{query_number}.txt", "a") as file:
                file.write(f"attractions in {name}, {first_order}\n")

def main():
    clear_folder("Queries")
    generate_example_queries("../allData/all_locations.csv", 50)
    print("\033[92mQueries generated successfully.\033[0m")

if __name__ == "__main__":
    main()