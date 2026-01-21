import os
import pandas as pd

from src.build_fact_tables import fact_sales

raw_dir = "../data/uncleaned_dimensions"
clean_dir = "../data/cleaned_dimensions"
CLEAN_DIM_DIR = "../data/cleaned_dimensions"
FACT_DIR = "../data/fact_tables"

# Load raw dimension tables
# dim_category_raw = pd.read_csv(os.path.join(raw_dir, "dim_category_raw.csv"))
# dim_product_raw = pd.read_csv(os.path.join(raw_dir, "dim_product_raw.csv"))
# dim_supplier_raw = pd.read_csv(os.path.join(raw_dir, "dim_supplier_raw.csv"))
# dim_date_sales_raw = pd.read_csv(os.path.join(raw_dir, "dim_date_sales_raw.csv"))
# dim_sale_raw = pd.read_csv(os.path.join(raw_dir, "dim_sale_raw.csv"))
#
# dim_major_raw = pd.read_csv(os.path.join(raw_dir, "dim_major_raw.csv"))
# dim_student_raw = pd.read_csv(os.path.join(raw_dir, "dim_student_raw.csv"))
# dim_date_enrollment_raw = pd.read_csv(os.path.join(raw_dir, "dim_date_enrollment_raw.csv"))


dim_category_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_category_cleaned.csv")
dim_date_sales_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_date_sales_cleaned.csv")
dim_date_enrollment_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_date_enrollment_cleaned.csv")
dim_product_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_product_cleaned.csv")
dim_sale_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_sale_cleaned.csv")
dim_supplier_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_supplier_cleaned.csv")

dim_student_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_student_cleaned.csv")
dim_major_cleaned = pd.read_csv(f"{CLEAN_DIM_DIR}/dim_major_cleaned.csv")

fact_sales = pd.read_csv(f"{FACT_DIR}/fact_sales.csv")
fact_student = pd.read_csv(f"{FACT_DIR}/fact_student.csv")
print(fact_sales.info())
print(fact_student.info())
print(fact_sales.head())
print(fact_student.head())
