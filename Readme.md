**Everyone take a look at the data and first everyone create DB tables like what different dim tables can be created from these two data sets.**


- Dimension Tables (Sales data):
  - dim_product ( productId, productName, categoryId (fk))
  - dim_category ( categoryId, categoryName )
  - dim_supplier ( supplierId, supplierName )
  - dim_date ( dateId, fullDate, day, month, year, quarter )

- Dimension Tables (Student data):
  - dim_student ( studentId, firstName, lastName, age, gender )
  - dim_major ( majorId, majorName )
  - dim_date ( dateId, fullDate, year, semester )
  

**Next using python built in function do all the changes you want to the data like correct the names formatting the dates removing extra spaces combining the name or combining two rows to get one value adding data to find the today average of some columns that makes sense etc.**

**Also as a part of the exercise try to determine what kind of data from this will help build a dashboard explain in your own words how this data can help in a dashboard and how will you send this data to a Analyst and what type of methods will be used build a complete flow diagram as well for how the ETL will work.**

