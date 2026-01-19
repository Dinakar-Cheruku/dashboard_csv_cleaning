import csv

sales_file = '../data/sales_inventory_dataset.csv'
student_file = "../data/student_information_dataset.csv"

def inspect_csv(file_path, limit=5):
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        print(f"\nFile: {file_path}")
        print("Headers:", headers)

        print("\nSample Rows:")
        for i, row in enumerate(reader):
            if i >= limit:
                break
            print(row)

inspect_csv(sales_file)
inspect_csv(student_file)