import pandas as pd
import os

# ----------------------------
# Paths
# ----------------------------
CLEAN_DIM_DIR = "../data/cleaned_dimensions"
FACT_DIR = "../data/fact_tables"
os.makedirs(FACT_DIR, exist_ok=True)

# ----------------------------
# Load cleaned dimension tables
# ----------------------------
dim_product = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_product_cleaned.csv")
dim_category = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_category_cleaned.csv")
dim_supplier = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_supplier_cleaned.csv")
dim_date_sales = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_date_sales_cleaned.csv")  # Sales dates

dim_student = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_student_cleaned.csv")
dim_major = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_major_cleaned.csv")
dim_date_enrollment = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_date_enrollment_cleaned.csv")  # Enrollment dates

# ----------------------------
# Load raw CSVs (for IDs reference only)
# ----------------------------
sales_df = pd.read_csv("../data/sales_inventory_dataset.csv")
students_df = pd.read_csv("../data/student_information_dataset.csv")

# ----------------------------
# --- Build fact_sales ---
# ----------------------------

# Standardize string columns to avoid merge mismatches
sales_df['ItemName'] = sales_df['ItemName'].str.strip()
sales_df['Category'] = sales_df['Category'].str.strip()
sales_df['Supplier'] = sales_df['Supplier'].str.strip()

# Merge with cleaned dimension tables
fact_sales = sales_df.merge(
    dim_product[['product_id', 'product_name', 'category_id']],
    left_on='ItemName',
    right_on='product_name',
    how='left'
)

fact_sales = fact_sales.merge(
    dim_supplier[['supplier_id', 'supplier_name']],
    left_on='Supplier',
    right_on='supplier_name',
    how='left'
)

# Parse DateAdded in fact_sales
fact_sales['DateAdded_parsed'] = pd.to_datetime(fact_sales['DateAdded'], errors='coerce', dayfirst=True)

# Ensure dim_date_sales['full_date'] is datetime
dim_date_sales['full_date'] = pd.to_datetime(dim_date_sales['full_date'], errors='coerce', dayfirst=True, format='%Y-%m-%d')

# Merge Date ID
fact_sales = fact_sales.merge(
    dim_date_sales[['date_id', 'full_date']],
    left_on='DateAdded_parsed',
    right_on='full_date',
    how='left'
)

# Use cleaned numeric columns from the original CSV
# Negative or missing values are corrected by dim tables, but just in case
fact_sales['quantity'] = fact_sales['Quantity'].apply(lambda x: 0 if pd.isna(x) or x < 0 else x)
fact_sales['price'] = fact_sales['Price'].apply(lambda x: 0 if pd.isna(x) or x < 0 else x)

# Compute total_amount safely
fact_sales['total_amount'] = fact_sales['quantity'] * fact_sales['price']

# Keep only relevant columns
fact_sales_final = fact_sales[['product_id', 'category_id', 'supplier_id', 'date_id', 'quantity', 'price', 'total_amount']]

# Save
fact_sales_final.to_csv(f"{FACT_DIR}/fact_sales.csv", index=False)
print("fact_sales.csv saved successfully!")

# ----------------------------
# --- Build fact_student ---
# ----------------------------

# Standardize string columns
students_df['Name'] = students_df['Name'].str.strip()
students_df['Major'] = students_df['Major'].str.strip()

# Split names to join with dim_student
students_df[['first_name', 'last_name']] = students_df['Name'].str.split(n=1, expand=True)

# Merge with dim_student
fact_student = students_df.merge(
    dim_student[['student_id', 'first_name', 'last_name']],
    on=['first_name', 'last_name'],
    how='left'
)

# Merge Major ID
fact_student = fact_student.merge(
    dim_major[['major_id', 'major_name']],
    left_on='Major',
    right_on='major_name',
    how='left'
)

# Parse EnrollmentDate in students_df
students_df['EnrollmentDate_parsed'] = pd.to_datetime(students_df['EnrollmentDate'], errors='coerce', dayfirst=True)

# Ensure dim_date_enrollment['full_date'] is datetime
dim_date_enrollment['full_date'] = pd.to_datetime(dim_date_enrollment['full_date'], errors='coerce', dayfirst=True, format='%Y-%m-%d')

# Merge Date ID
fact_student = fact_student.merge(
    dim_date_enrollment[['date_id', 'full_date']],
    left_on='EnrollmentDate_parsed',
    right_on='full_date',
    how='left'
)


# Keep only relevant columns
fact_student_final = fact_student[['student_id', 'major_id', 'date_id', 'Grade']]

# Save
fact_student_final.to_csv(f"{FACT_DIR}/fact_student.csv", index=False)
print("fact_student.csv saved successfully!")
