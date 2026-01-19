import pandas as pd

sales_file = '../data/sales_inventory_dataset.csv'
student_file = "../data/student_information_dataset.csv"

sales_df = pd.read_csv(sales_file)
student_df = pd.read_csv(student_file)

# print(sales_df.head())
# print(student_df.head())

# sales_df.info()
# student_df.info()

# print(sales_df.isna().sum())
# print(student_df.isna().sum())

# print(sales_df[sales_df["Quantity"]<0])
# print(sales_df[sales_df["Price"] < 0])

# print(student_df[student_df["Age"].astype(str).str.isalpha()])

print(sales_df.info())

