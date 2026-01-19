import pandas as pd
import numpy as np
import os

# ----------------------------
# Paths
# ----------------------------
CLEAN_DIM_DIR = "../data/cleaned_dimensions"
FACT_DIR = "../data/fact_tables"
os.makedirs(FACT_DIR, exist_ok=True)

# ----------------------------
# Load raw data
# ----------------------------
sales_df = pd.read_csv("../data/sales_inventory_dataset.csv")
students_df = pd.read_csv("../data/student_information_dataset.csv")

# ----------------------------
# Load cleaned dimension tables
# ----------------------------
dim_category = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_category_cleaned.csv")
dim_date_sales = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_date_sales_cleaned.csv")
dim_date_enrollment = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_date_enrollment_cleaned.csv")
dim_product = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_product_cleaned.csv")
dim_sale = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_sale_cleaned.csv")
dim_supplier = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_supplier_cleaned.csv")

dim_student = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_student_cleaned.csv")
dim_major = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_major_cleaned.csv")

# ----------------------------
# Ensure consistent types for merge
# ----------------------------
# IDs as strings
id_cols = [
    ('dim_sale', 'product_id'),
    ('dim_product', 'product_id'),
    ('dim_category', 'category_id'),
    ('dim_supplier', 'supplier_id'),
    ('dim_date_sales', 'date_id'),
    ('dim_date_enrollment', 'date_id'),
    ('dim_student', 'student_id'),
    ('dim_major', 'major_id')
]

for df_name, col in id_cols:
    locals()[df_name][col] = locals()[df_name][col].astype(str)

# Raw dataset IDs
sales_df['ItemID'] = sales_df['ItemID'].astype(str).str.strip()
sales_df['Supplier'] = sales_df['Supplier'].astype(str).str.strip()
sales_df['DateAdded'] = pd.to_datetime(sales_df['DateAdded'], errors='coerce', format='%Y-%m-%d')

students_df['StudentID'] = students_df['StudentID'].astype(str).str.strip()
students_df['EnrollmentDate'] = pd.to_datetime(students_df['EnrollmentDate'], errors='coerce', format='%Y-%m-%d')

# Date columns in dim tables
dim_date_sales['full_date'] = pd.to_datetime(dim_date_sales['full_date'], errors='coerce', format='%Y-%m-%d')
dim_date_enrollment['full_date'] = pd.to_datetime(dim_date_enrollment['full_date'], errors='coerce', format='%Y-%m-%d')

# ----------------------------
# --- Build fact_sales ---
# ----------------------------

# Merge dim_sale with dim_product to get category_id
fact_sales = dim_sale.merge(
    dim_product[['product_id', 'category_id']],
    on='product_id',
    how='left'
)

# Map supplier_id from raw sales via supplier name
sales_supplier = sales_df[['ItemID', 'Supplier']].drop_duplicates()
sales_supplier = sales_supplier.merge(
    dim_supplier[['supplier_id', 'supplier_name']],
    left_on='Supplier',
    right_on='supplier_name',
    how='left'
)
fact_sales = fact_sales.merge(
    sales_supplier[['ItemID', 'supplier_id']],
    left_on='product_id',
    right_on='ItemID',
    how='left'
)

# Map date_id using DateAdded
sales_dates = sales_df[['ItemID', 'DateAdded']].drop_duplicates()
fact_sales = fact_sales.merge(
    sales_dates,
    left_on='product_id',
    right_on='ItemID',
    how='left'
)
fact_sales = fact_sales.merge(
    dim_date_sales[['date_id', 'full_date']],
    left_on='DateAdded',
    right_on='full_date',
    how='left'
)

# Clean numeric measures
fact_sales['Quantity'] = fact_sales['Quantity'].fillna(0).clip(lower=0).astype(int)
fact_sales['Price'] = fact_sales['Price'].fillna(0).clip(lower=0).round(2)
fact_sales['total_amount'] = (fact_sales['Quantity'] * fact_sales['Price']).round(2)

# Final fact_sales columns
fact_sales_final = fact_sales[
    ['sale_id', 'product_id', 'category_id', 'supplier_id', 'date_id', 'Quantity', 'Price', 'total_amount']
]

# Save
fact_sales_final.to_csv(f"{FACT_DIR}/fact_sales.csv", index=False)
print("fact_sales.csv saved successfully!")

# ----------------------------
# --- Build fact_student ---
# ----------------------------

# Ensure major_id columns are the same type (string)
dim_student['major_id'] = dim_student['major_id'].astype(str)
dim_major['major_id'] = dim_major['major_id'].astype(str)

# Ensure student_id columns are strings
dim_student['student_id'] = dim_student['student_id'].astype(str)
students_df['StudentID'] = students_df['StudentID'].astype(str)

# Merge dim_student with dim_major
fact_student = dim_student.merge(
    dim_major[['major_id', 'major_name']],
    on='major_id',
    how='left'
)

# Merge enrollment date
students_df['EnrollmentDate'] = pd.to_datetime(students_df['EnrollmentDate'], errors='coerce', format='%Y-%m-%d')
dim_date_enrollment['date_id'] = dim_date_enrollment['date_id'].astype(str)
dim_date_enrollment['full_date'] = pd.to_datetime(dim_date_enrollment['full_date'], errors='coerce', format='%Y-%m-%d')

# Map student enrollment date to date_id
student_dates = students_df[['StudentID', 'EnrollmentDate']].drop_duplicates()
fact_student = fact_student.merge(
    student_dates,
    left_on='student_id',
    right_on='StudentID',
    how='left'
)
fact_student = fact_student.merge(
    dim_date_enrollment[['date_id', 'full_date']],
    left_on='EnrollmentDate',
    right_on='full_date',
    how='left'
)

# Final columns for fact_student
fact_student_final = fact_student[['student_id', 'major_id', 'date_id', 'age', 'gender', 'grade']]

# Save
fact_student_final.to_csv(f"{FACT_DIR}/fact_student.csv", index=False)
print("fact_student.csv saved successfully!")
