**Everyone take a look at the data and first everyone create DB tables like what different dim tables can be created from these two data sets.**

**- ETL Workflow**
Raw CSVs
   │
   ▼
Python / Pandas Exploration
   │
   ▼
Data Cleaning
   ├─ Normalize numeric fields
   ├─ Standardize categorical values
   ├─ Parse and extract date components
   └─ Handle missing values
   │
   ▼
Dimension Tables
   ├─ dim_product, dim_category, dim_supplier, dim_date (Sales)
   └─ dim_student, dim_major, dim_date (Student)
   │
   ▼
Saved Cleaned CSVs (or DB insert)
   │
   ▼
Fact Table / Dashboard Ready

**- Dimension Tables (Sales data):**
  - dim_product ( productId, productName, categoryId (fk))
  - dim_category ( categoryId, categoryName )
  - dim_supplier ( supplierId, supplierName )
  - dim_date ( dateId, fullDate, day, month, year, quarter )

**- Dimension Tables (Student data):**
  - dim_student ( studentId, firstName, lastName, age, gender )
  - dim_major ( majorId, majorName )
  - dim_date ( dateId, fullDate, year, semester )

_We include a dim_date table for both Sales and Student datasets to standardize date information and simplify analysis. Instead of storing full dates repeatedly in fact tables, each record can reference a date_id, reducing redundancy and ensuring consistency. This makes it easy to aggregate, filter, or group data by year, month, quarter, or semester. Additionally, having a consistent date dimension allows multiple datasets to be joined reliably in the future for time-based analytics and dashboards._
  

**Next using python built in function do all the changes you want to the data like correct the names formatting the dates removing extra spaces combining the name or combining two rows to get one value adding data to find the today average of some columns that makes sense etc.**

- **Cleaning Policies**
- 
**Sales Data Cleaning**

Quantity -> Negative values	-> Set to 0
Price -> Missing or non-numeric -> Replace with category average
Supplier -> Missing -> Replace with "Unknown"
DateAdded -> Invalid / malformed dates -> Convert to NaT and extract year, month, day, quarter 

**Student Data Cleaning**

Age -> Invalid text ("twenty"), negative numbers -> Convert "twenty" → 20, negatives → NaN
Gender -> Inconsistent values (Male, female, M, F) -> Normalize to "M", "F", else "Unknown"
Grade -> Invalid grades (M, Z, empty, etc.) -> Keep "A", "B", "C", "D"; others → "F"
Major -> Missing -> Fill with "Undeclared"
EnrollmentDate -> Invalid / malformed dates -> Convert to NaT and extract year, month, semester

**Also as a part of the exercise try to determine what kind of data from this will help build a dashboard explain in your own words how this data can help in a dashboard and how will you send this data to a Analyst and what type of methods will be used build a complete flow diagram as well for how the ETL will work.**

