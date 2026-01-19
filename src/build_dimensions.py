import pandas as pd
import os

# Load raw sales data
sales_df = pd.read_csv("../data/sales_inventory_dataset.csv")

# ----------------------------
# DIM_CATEGORY
# ----------------------------
dim_category = (
    sales_df[["Category"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_category["category_id"] = dim_category.index + 1
dim_category = dim_category[["category_id", "Category"]]

# ----------------------------
# DIM_PRODUCT
# ----------------------------
dim_product = sales_df[["ItemID", "ItemName", "Category"]].drop_duplicates()

# Join product with category dimension
dim_product = dim_product.merge(
    dim_category,
    on="Category",
    how="left"
)

# Rename columns to DB-friendly names
dim_product = dim_product.rename(columns={
    "ItemID": "product_id",
    "ItemName": "product_name"
})

# Final column selection
dim_product = dim_product[["product_id", "product_name", "category_id"]]

# ----------------------------
# OUTPUT CHECKS
# ----------------------------
print("\nDIM_CATEGORY")
print(dim_category)

print("\nDIM_PRODUCT (sample 10 rows)")
print(dim_product.head(10))

print("\nTotal Products:", len(dim_product))
print("Products with NULL category_id:",
      dim_product["category_id"].isna().sum())
# ----------------------------
# DIM_SALES
# ----------------------------
dim_sale = sales_df.merge(
    dim_product,
    left_on='ItemName',
    right_on='product_name',
    how='left'
)

# Add a surrogate sale key
dim_sale = dim_sale.reset_index().rename(columns={'index': 'sale_id'})
dim_sale["sale_id"] = dim_sale.index + 1

# Keep only the columns you want
dim_sale = dim_sale[['sale_id', 'product_id', 'Price', 'Quantity']]

# Add total_price column (just calculation, even if dirty for now)
# dim_sale['total_price'] = dim_sale['Price'] * dim_sale['Quantity']

# Optional: preview
print(dim_sale.head())




# ----------------------------
# DIM_SUPPLIER
# ----------------------------
dim_supplier = (
    sales_df[["Supplier"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Rename column
dim_supplier = dim_supplier.rename(columns={"Supplier": "supplier_name"})

# Add surrogate key
dim_supplier["supplier_id"] = dim_supplier.index + 1

# Reorder columns
dim_supplier = dim_supplier[["supplier_id", "supplier_name"]]

print("\nDIM_SUPPLIER")
print(dim_supplier)
print("\nTotal Suppliers:", len(dim_supplier))
print("Suppliers with NULL name:",
      dim_supplier["supplier_name"].isna().sum())

# ----------------------------
# DIM_DATE (SALES)
# ----------------------------
dim_date = (
    sales_df[["DateAdded"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Convert to datetime (invalid -> NaT)
dim_date["full_date"] = pd.to_datetime(
    dim_date["DateAdded"],
    errors="coerce",
    format="%Y-%m-%d"
)

# Extract date parts
dim_date["year"] = dim_date["full_date"].dt.year.astype("Int64")
dim_date["month"] = dim_date["full_date"].dt.month.astype("Int64")
dim_date["day"] = dim_date["full_date"].dt.day.astype("Int64")

# Add surrogate key
dim_date["date_id"] = dim_date.index + 1

# Select final columns
dim_date = dim_date[["date_id", "full_date", "year", "month", "day"]]

print("\nDIM_DATE (Sales)")
print(dim_date.head(10))
print("\nTotal Dates:", len(dim_date))
print("Invalid Dates (NULL):", dim_date["full_date"].isna().sum())

# ----------------------------
# STUDENT DIMENSIONS
# ----------------------------
students_df = pd.read_csv("../data/student_information_dataset.csv")

# ----------------------------
# DIM_MAJOR
# ----------------------------
dim_major = (
    students_df[["Major"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_major = dim_major.rename(columns={"Major": "major_name"})
dim_major["major_id"] = dim_major.index + 1
dim_major = dim_major[["major_id", "major_name"]]

print("\nDIM_MAJOR")
print(dim_major)
print("\nTotal Majors:", len(dim_major))
print("Majors with NULL:", dim_major["major_name"].isna().sum())

# ----------------------------
# DIM_STUDENT
# ----------------------------
# Split Name into first and last
students_df[["first_name", "last_name"]] = students_df["Name"].str.split(" ", n=1, expand=True)
student_merged = students_df.merge(
    dim_major,
    left_on="Major",
    right_on="major_name",
    how="left"
)
dim_student = student_merged[["StudentID", "first_name", "last_name", "Age", "Gender", "Grade", "major_id"]].drop_duplicates()
dim_student = dim_student.rename(columns={
    "StudentID": "student_id",
    "Age": "age",
    "Gender": "gender",
    "Grade": "grade"
})

print("\nDIM_STUDENT (sample 10 rows)")
print(dim_student.head(10))
print("\nTotal Students:", len(dim_student))
print("Students with NULL gender:", dim_student["gender"].isna().sum())
print("Students with NULL major_id:", dim_student["major_id"].isna().sum())

# ----------------------------
# DIM_DATE (ENROLLMENT)
# ----------------------------
dim_enroll_date = students_df[["EnrollmentDate"]].drop_duplicates().reset_index(drop=True)

dim_enroll_date["full_date"] = pd.to_datetime(
    dim_enroll_date["EnrollmentDate"],
    errors="coerce",
    format="%Y-%m-%d"
)
dim_enroll_date["year"] = dim_enroll_date["full_date"].dt.year.astype("Int64")
dim_enroll_date["month"] = dim_enroll_date["full_date"].dt.month.astype("Int64")
dim_enroll_date["day"] = dim_enroll_date["full_date"].dt.day.astype("Int64")
dim_enroll_date["date_id"] = dim_enroll_date.index + 1
dim_enroll_date = dim_enroll_date[["date_id", "full_date", "year", "month", "day"]]

print("\nDIM_DATE (Enrollment)")
print(dim_enroll_date.head(10))
print("\nTotal Enrollment Dates:", len(dim_enroll_date))
print("Invalid Enrollment Dates (NULL):", dim_enroll_date["full_date"].isna().sum())


#converting the uncleaned dimension tables into csv ( for learning purposes )
# Create folder if it doesn't exist
raw_dir = "../data/uncleaned_dimensions"
os.makedirs(raw_dir, exist_ok=True)

# Save all raw dimension tables
dim_category.to_csv(os.path.join(raw_dir, "dim_category_raw.csv"), index=False)
dim_product.to_csv(os.path.join(raw_dir, "dim_product_raw.csv"), index=False)
dim_supplier.to_csv(os.path.join(raw_dir, "dim_supplier_raw.csv"), index=False)
dim_date.to_csv(os.path.join(raw_dir, "dim_date_sales_raw.csv"), index=False)
dim_sale.to_csv(os.path.join(raw_dir, "dim_sale_raw.csv"), index=False)


dim_major.to_csv(os.path.join(raw_dir, "dim_major_raw.csv"), index=False)
dim_student.to_csv(os.path.join(raw_dir, "dim_student_raw.csv"), index=False)
dim_enroll_date.to_csv(os.path.join(raw_dir, "dim_date_enrollment_raw.csv"), index=False)

print(f"All raw dimension tables saved successfully in '{raw_dir}'")
