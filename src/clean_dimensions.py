import pandas as pd
import numpy as np
import os

# Folder paths
raw_dir = "../data/uncleaned_dimensions"
clean_dir = "../data/cleaned_dimensions"
os.makedirs(clean_dir, exist_ok=True)

# Load raw dimension tables
dim_category = pd.read_csv(os.path.join(raw_dir, "dim_category_raw.csv"))
dim_product = pd.read_csv(os.path.join(raw_dir, "dim_product_raw.csv"))
dim_supplier = pd.read_csv(os.path.join(raw_dir, "dim_supplier_raw.csv"))
dim_date_sales = pd.read_csv(os.path.join(raw_dir, "dim_date_sales_raw.csv"))
dim_sale = pd.read_csv(os.path.join(raw_dir, "dim_sale_raw.csv"))

dim_major = pd.read_csv(os.path.join(raw_dir, "dim_major_raw.csv"))
dim_student = pd.read_csv(os.path.join(raw_dir, "dim_student_raw.csv"))
dim_date_enrollment = pd.read_csv(os.path.join(raw_dir, "dim_date_enrollment_raw.csv"))


# ---- Sales cleaning ----
def clean_quantity(value):
    """Negative quantity → NaN"""
    try:
        value = float(value)
        if value < 0:
            return np.nan
        return int(value)
    except:
        return np.nan


def clean_supplier(value):
    """Missing supplier → 'Unknown'"""
    if pd.isna(value) or str(value).strip() == "":
        return "Unknown"
    return value


def clean_price(value):
    try:
        value = str(value).replace("$", "").replace(",", "").strip()
        value = float(value)
        if value <= 0:
            return np.nan
        return value
    except:
        return np.nan


# ---- Student cleaning ----
def clean_age(value):
    """Convert age to int, handle invalid or missing values as 'Unknown'."""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return "Unknown"
    if isinstance(value, str):
        if value.lower() == "twenty":
            return 20
    try:
        value = int(value)
        if value < 0:
            return "Unknown"
        return value
    except:
        return "Unknown"



def clean_major(value):
    """Missing major → 'Undeclared'"""
    if pd.isna(value) or str(value).strip() == "":
        return "Undeclared"
    return value


def clean_gender(value):
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ["male", "m"]:
            return "M"
        elif v in ["female", "f"]:
            return "F"
    return "Unknown"


def clean_grade(value):
    valid_grades = ["A+", "A", "B", "C", "D"]
    if isinstance(value, str):
        value = value.strip().upper()
        if value in valid_grades:
            return value
    return "F"


# CLEANING
# For sales
# Quantity
dim_sale['Quantity'] = dim_sale['Quantity'].apply(clean_quantity)

dim_sale = dim_sale.merge(
    dim_product[['product_id', 'category_id']],
    on='product_id',
    how='left'
)
# Supplier
dim_supplier['supplier_name'] = dim_supplier['supplier_name'].apply(clean_supplier)

# Price
dim_sale['Price'] = dim_sale['Price'].apply(clean_price)
dim_sale['Price'] = dim_sale.groupby('category_id')['Price'].transform(
    lambda x: x.fillna(x[x > 0].mean())
)
dim_sale['Price'] = dim_sale['Price'].round(2)

dim_sale['total_amount'] = dim_sale['Price'] * dim_sale['Quantity']
dim_sale['total_amount'] = dim_sale['total_amount'].round(2)

dim_sale_cleaned = dim_sale[['sale_id', 'product_id', 'Price', 'Quantity', 'total_amount']]

# Date (Sales)
dim_date_sales['full_date'] = pd.to_datetime(dim_date_sales['full_date'], errors='coerce')
dim_date_sales['year'] = dim_date_sales['full_date'].dt.year.astype("Int64")
dim_date_sales['month'] = dim_date_sales['full_date'].dt.month.astype("Int64")
dim_date_sales['day'] = dim_date_sales['full_date'].dt.day.astype("Int64")

# for students
# Age
dim_student['age'] = dim_student['age'].apply(clean_age)

# Major
dim_major['major_name'] = dim_major['major_name'].apply(clean_major)

# Enrollment Date
dim_date_enrollment['full_date'] = pd.to_datetime(dim_date_enrollment['full_date'], errors='coerce')
dim_date_enrollment['year'] = dim_date_enrollment['full_date'].dt.year.astype("Int64")
dim_date_enrollment['month'] = dim_date_enrollment['full_date'].dt.month.astype("Int64")
dim_date_enrollment['day'] = dim_date_enrollment['full_date'].dt.day.astype("Int64")
dim_student['gender'] = dim_student['gender'].apply(clean_gender)
dim_student['grade'] = dim_student['grade'].apply(clean_grade)

# saving all the cleaned dimensions data frames into csv

dim_category.to_csv(os.path.join(clean_dir, "dim_category_cleaned.csv"), index=False, na_rep="NULL")
dim_product.to_csv(os.path.join(clean_dir, "dim_product_cleaned.csv"), index=False, na_rep="NULL")
dim_supplier.to_csv(os.path.join(clean_dir, "dim_supplier_cleaned.csv"), index=False, na_rep="NULL")
dim_date_sales.to_csv(os.path.join(clean_dir, "dim_date_sales_cleaned.csv"), index=False, na_rep="NULL")
dim_sale_cleaned.to_csv(os.path.join(clean_dir, "dim_sale_cleaned.csv"), index=False, na_rep="NULL")

dim_major.to_csv(os.path.join(clean_dir, "dim_major_cleaned.csv"), index=False, na_rep="NULL")
dim_student.to_csv(os.path.join(clean_dir, "dim_student_cleaned.csv"), index=False, na_rep="NULL")
dim_date_enrollment.to_csv(os.path.join(clean_dir, "dim_date_enrollment_cleaned.csv"), index=False, na_rep="NULL")

print(f"All cleaned dimension tables saved successfully in '{clean_dir}'")
