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

dim_major = pd.read_csv(os.path.join(raw_dir, "dim_major_raw.csv"))
dim_student = pd.read_csv(os.path.join(raw_dir, "dim_student_raw.csv"))
dim_date_enrollment = pd.read_csv(os.path.join(raw_dir, "dim_date_enrollment_raw.csv"))

# ---- Sales cleaning ----
def clean_quantity(value):
    """Negative quantity → 0 or NaN"""
    if pd.isna(value):
        return np.nan
    return max(0, value)

def clean_supplier(value):
    """Missing supplier → 'Unknown'"""
    if pd.isna(value) or str(value).strip() == "":
        return "Unknown"
    return value


def fill_missing_price(df):
    # Ensure Price is numeric
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Replace negative or missing prices with category average
    def replace_invalid(x):
        x[x <= 0] = pd.NA  # Treat negative and zero as invalid
        return x.fillna(x.mean())  # Fill missing/invalid with category mean

    df['Price'] = df.groupby('category_id')['Price'].transform(replace_invalid)
    return df


# ---- Student cleaning ----
def clean_age(value):
    """Convert 'twenty' → 20, negative or invalid → NaN"""
    if isinstance(value, str):
        if value.lower() == "twenty":
            return int(20)
    try:
        value = int(value)
        if value < 0:
            return np.nan
        return value
    except:
        return np.nan

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
    valid_grades = ["A", "B", "C", "D"]
    if isinstance(value, str):
        value = value.strip().upper()
        if value in valid_grades:
            return value
    return "F"



# CLEANING
# For sales
# Quantity
dim_product['Quantity'] = dim_product['product_name'].map(
    dim_product.set_index('product_name')['Quantity'].apply(clean_quantity)
) if 'Quantity' in dim_product.columns else None

# Supplier
dim_supplier['supplier_name'] = dim_supplier['supplier_name'].apply(clean_supplier)

# Price
dim_product['Price'] = pd.to_numeric(dim_product['Price'], errors='coerce') \
    if 'Price' in dim_product.columns else None
dim_product = fill_missing_price(dim_product)

# Date (Sales)
dim_date_sales['full_date'] = pd.to_datetime(dim_date_sales['full_date'], errors='coerce')
dim_date_sales['year'] = dim_date_sales['full_date'].dt.year
dim_date_sales['month'] = dim_date_sales['full_date'].dt.month
dim_date_sales['day'] = dim_date_sales['full_date'].dt.day



# for students
# Age
dim_student['age'] = dim_student['age'].apply(clean_age)

# Major
dim_major['major_name'] = dim_major['major_name'].apply(clean_major)

# Enrollment Date
dim_date_enrollment['full_date'] = pd.to_datetime(dim_date_enrollment['full_date'], errors='coerce')
dim_date_enrollment['year'] = dim_date_enrollment['full_date'].dt.year
dim_date_enrollment['month'] = dim_date_enrollment['full_date'].dt.month
dim_date_enrollment['day'] = dim_date_enrollment['full_date'].dt.day
dim_student['gender'] = dim_student['gender'].apply(clean_gender)
dim_student['grade'] = dim_student['grade'].apply(clean_grade)



#saving all the cleaned dimensions data frames into csv

dim_category.to_csv(os.path.join(clean_dir, "dim_category_cleaned.csv"), index=False, na_rep="NULL")
dim_product.to_csv(os.path.join(clean_dir, "dim_product_cleaned.csv"), index=False, na_rep="NULL")
dim_supplier.to_csv(os.path.join(clean_dir, "dim_supplier_cleaned.csv"), index=False, na_rep="NULL")
dim_date_sales.to_csv(os.path.join(clean_dir, "dim_date_sales_cleaned.csv"), index=False, na_rep="NULL")

dim_major.to_csv(os.path.join(clean_dir, "dim_major_cleaned.csv"), index=False, na_rep="NULL")
dim_student.to_csv(os.path.join(clean_dir, "dim_student_cleaned.csv"), index=False, na_rep="NULL")
dim_date_enrollment.to_csv(os.path.join(clean_dir, "dim_date_enrollment_cleaned.csv"), index=False, na_rep="NULL")

print(f"All cleaned dimension tables saved successfully in '{clean_dir}'")


