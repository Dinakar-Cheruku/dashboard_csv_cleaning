**Everyone take a look at the data and first everyone create DB tables like what different dim tables can be created from these two data sets.**

**- ETL Workflow**
Raw CSVs
   │
   ▼
Python / Pandas Exploration
   │
   ▼
Data Cleaning Policies
   ├─ Normalize numeric fields
   ├─ Standardize categorical values
   ├─ Parse and extract date components
   └─ Handle missing values
   │
   ▼
Dimension Tables
   ├─ dim_product, dim_category, dim_supplier, dim_date, dim_sale(Sales)
   └─ dim_student, dim_major, dim_date (Student)
   │
   ▼
Cleaning Dimension Tables
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
  - dim_sale ( sale_id, ,product_id, Price, Quantity )

**- Dimension Tables (Student data):**
  - dim_student ( studentId, firstName, lastName, age, gender )
  - dim_major ( majorId, majorName )
  - dim_date ( dateId, fullDate, year, semester )

_We include a dim_date table for both Sales and Student datasets to standardize date information and simplify analysis. Instead of storing full dates repeatedly in fact tables, each record can reference a date_id, reducing redundancy and ensuring consistency. This makes it easy to aggregate, filter, or group data by year, month, quarter, or semester. Additionally, having a consistent date dimension allows multiple datasets to be joined reliably in the future for time-based analytics and dashboards._
  

**Next using python built-in function do all the changes you want to the data like correct the names formatting the dates removing extra spaces combining the name or combining two rows to get one value adding data to find the today average of some columns that makes sense etc.**

- **Cleaning Policies**
- 
**Sales Data Cleaning**

Quantity -> Negative values	-> Set to 0
Price -> Missing or non-numeric -> Replace with category average
Supplier -> Missing -> Replace with "Unknown"
DateAdded -> Invalid / malformed dates -> Convert to NaT and extract year, month, day, quarter 
TotalAmount -> derived from quantity * price

**Student Data Cleaning**

Age -> Invalid text ("twenty"), negative numbers -> Convert "twenty" → 20, negatives → NaN, "" -> "Unknown"
Gender -> Inconsistent values (Male, female, M, F) -> Normalize to "M", "F", else "Unknown"
Grade -> Invalid grades (M, Z, empty, etc.) -> Keep "A+", "A", "B", "C", "D"; others → "F"
Major -> Missing -> Fill with "Undeclared"
EnrollmentDate -> Invalid / malformed dates -> Convert to NaT and extract year, month, semester

**Also as a part of the exercise try to determine what kind of data from this will help build a dashboard explain in your own words how this data can help in a dashboard and how will you send this data to a Analyst and what type of methods will be used build a complete flow diagram as well for how the ETL will work.**

From our cleaned and fact/dimension tables, here’s what can be used for dashboard analytics:

**Sales Dashboard Data :**
- Product Performance : product_id, product_name, category_id, quantity, price, total_amount. (Show best-selling products, revenue per product, quantity sold)
- Category trends: category_id, category_name, total_amount (Track revenue per category, category growth, trends over months/quarters.)
- Supplier performance: supplier_id, supplier_name, total_amount ( identify top suppliers, underperforming suppliers, late/low-volume suppliers.)
- Time analysis: date_id, year, month, day, quarter. ( Track sales over time, seasonal trends, monthly/quarterly revenue. )

**Student/Enrollment Dashboard Data :** 
- Student demographics: student_id, age, gender, grade, major_id ( Track age distribution, gender ratio, grades per major.)
- Major-wise performance: major_id, major_name, grade. ( Compare student grades across majors, performance trends. )
- Enrollment trends: date_id, year, semester. ( Monitor enrollments over time, semester-wise intake. )

**Data Delivery to Analyst :**
- Method: Provide cleaned fact tables and dimension tables as CSV files or load into a relational database (like PostgreSQL/MySQL).

- Structure: Analysts get fact tables (fact_sales.csv, fact_student.csv) linked with dimension tables (dim_product, dim_category, dim_supplier, dim_student, dim_major, dim_date).

- Tools Analysts Can Use: Power BI, Tableau, Excel, or Python notebooks. Using dimension keys, they can join tables for reporting.

Probable Scenario : In this project, data is delivered to analysts as cleaned fact and dimension tables in CSV format or via a database.
No API is required at this stage since analysts primarily consume data using SQL or BI tools. However, in a production environment, APIs may be introduced to expose aggregated metrics to dashboards or downstream applications, or to automate data delivery through cloud storage services.