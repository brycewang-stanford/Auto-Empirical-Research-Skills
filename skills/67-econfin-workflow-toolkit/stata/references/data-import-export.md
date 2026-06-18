# Data Import and Export

## File Format Summary

| Format | Import Command | Export Command |
|--------|---------------|----------------|
| Stata (.dta) | `use` | `save` |
| CSV/TXT | `import delimited` | `export delimited` |
| Excel | `import excel` | `export excel` |
| dBASE | `import dbase` | `export dbase` |
| ODBC | `odbc load` | `odbc insert` |
| SAS XPORT | `import sasxport5` | `export sasxport5` |

---

## Import Delimited Files

```stata
import delimited [using] filename [, options]
```

### Key Options
- `delimiter("char")` / `delimiter(tab)`: Specify delimiter
- `varnames(#)` / `varnames(nonames)`: Row with variable names
- `clear`: Replace data in memory
- `case(preserve|lower|upper)`: Variable name case
- `encoding("UTF-8")`: Character encoding
- `rowrange([start][:end])`: Import specific rows
- `colrange([start][:end])`: Import specific columns
- `numericcols(numlist)` / `stringcols(numlist)`: Force column types

### Examples
```stata
import delimited "data.csv", clear
import delimited "data.txt", delimiter(tab) clear
import delimited "data.csv", delimiter(";") clear          // European datasets
import delimited "data.csv", varnames(1) rowrange(2:1000) case(preserve) clear
import delimited "data.csv", stringcols(1 3 5) clear
import delimited "data.csv", encoding("UTF-8") clear
import delimited "data.csv", varnames(nonames) clear
```

---

## Import Excel Files

```stata
import excel [using] filename [, options]
```

### Key Options
- `sheet("sheetname")`: Specify worksheet
- `cellrange([start][:end])`: Import specific cell range
- `firstrow`: First row as variable names
- `allstring`: Import all data as strings (useful for mixed types)

### Examples
```stata
import excel "data.xlsx", firstrow clear
import excel "workbook.xlsx", sheet("Sales_2023") firstrow clear
import excel "data.xlsx", sheet("Data") cellrange(A1:E100) firstrow clear

// Import all as strings then convert
import excel "data.xlsx", firstrow allstring clear
destring var1 var2 var3, replace

// Describe Excel file before importing
import excel "workbook.xlsx", describe
```

---

## Use and Save Commands

```stata
// Load entire dataset
use "data/mydata.dta", clear

// Load specific variables
use id name age income using "data/mydata.dta", clear

// Load subset of observations
use "data/mydata.dta" if age > 18, clear

// Describe file without loading
describe using "data/mydata.dta"

// Save
save "data/mydata.dta", replace

// Save in older format for compatibility
saveold "data/mydata_v13.dta", replace version(13)

// Preserve and restore
preserve
    keep if year == 2020
    summarize
restore
```

---

## Export Commands

### Export Delimited
```stata
export delimited using "output/data.csv", replace
export delimited using "output/data.txt", delimiter(tab) replace
export delimited id name income using "output/subset.csv", replace
export delimited using "output/data.csv", nolabel replace     // Values instead of labels
export delimited using "output/data.csv", quote replace        // Quote strings
```

### Export Excel
```stata
export excel using "output/data.xlsx", firstrow(variables) replace
export excel using "output/data.xlsx", firstrow(varlabels) replace
export excel using "output/data.xlsx", sheet("Results") firstrow(variables) replace
export excel using "output/data.xlsx", sheet("Data") cell(B2) firstrow(variables) replace

// Add sheet to existing workbook
export excel using "output/existing.xlsx", sheet("NewData") firstrow(variables) modify
```

---

## ODBC and SQL Database Connections

```stata
// List available data sources and tables
odbc list
odbc query "MyDataSource"

// Load from database
odbc load, dsn("MyDatabase") table("customers") clear

// Execute SQL query
odbc load, exec("SELECT * FROM sales WHERE year = 2023") dsn("MyDatabase") clear

// Connection string (instead of DSN)
odbc load, exec("SELECT * FROM employees") ///
    connectionstring("Driver={SQL Server};Server=myserver;Database=mydb;Trusted_Connection=yes") clear

// Insert data into database
odbc insert, table("analysis_results") dsn("MyDatabase") create

// Execute SQL commands
odbc exec("UPDATE employees SET salary = salary * 1.05 WHERE dept = 'Sales'"), dsn("MyDatabase")
```

---

## Web Data Import

```stata
// Import CSV from URL
import delimited "https://example.com/data/mydata.csv", clear

// Stata's webuse for example datasets
webuse auto, clear
webuse nlswork, clear

// Download then import Excel
copy "https://example.com/data.xlsx" "temp_data.xlsx", replace
import excel "temp_data.xlsx", firstrow clear
erase "temp_data.xlsx"

// JSON via third-party command
ssc install jsonio
jsonio kv, file("data.json") flatten
```

---

## Common Data Import Issues and Solutions

### Variables Imported as Wrong Type
```stata
// Force columns during import
import delimited "data.csv", numericcols(2 3 4 5) clear
import delimited "data.csv", stringcols(1 6 7) clear

// Convert after import
destring var1 var2, replace ignore("$" "," "%")
tostring var3 var4, replace
```

### Character Encoding Problems
```stata
import delimited "data.csv", encoding("UTF-8") clear
import delimited "data.csv", encoding("ISO-8859-1") clear
import delimited "data.csv", encoding("Windows-1252") clear

// Convert encodings
unicode analyze
unicode encoding set "UTF-8"
unicode translate *
```

### Leading Zeros Dropped (e.g., ID "00123" becomes "123")
```stata
import delimited "data.csv", stringcols(1) clear
// Or format after import:
tostring id, replace format(%05.0f)
```

### Dates Imported as Strings
```stata
generate date_var = date(string_date, "YMD")   // "2023-01-15"
format date_var %td

generate date_var = date(string_date, "MDY")   // "01/15/2023"
format date_var %td

generate datetime_var = clock(string_datetime, "YMDhms")
format datetime_var %tc
```

### Excel Merged Cells
```stata
import excel "data.xlsx", allstring clear
replace var = var[_n-1] if missing(var)  // Fill down merged cells
```

### Large Files
```stata
set max_memory 16g
import delimited "huge.csv", rowrange(1:100000) clear

// Use frames for multiple datasets (Stata 16+)
frame create tempframe
frame tempframe: import delimited "large.csv", clear
```

### Missing Values Coded as Strings
```stata
foreach var of varlist _all {
    replace `var' = "" if inlist(`var', "NA", "N/A", ".", "missing", "-999")
}
destring, replace
```

### Variable Names with Spaces/Special Characters
```stata
rename *, lower
foreach var of varlist _all {
    local newname = subinstr("`var'", " ", "_", .)
    local newname = subinstr("`newname'", "(", "", .)
    local newname = subinstr("`newname'", ")", "", .)
    local newname = subinstr("`newname'", "$", "", .)
    rename `var' `newname'
}
```

### Corrupted or Incomplete Files
```stata
import delimited "data.csv", clear bindquote(strict)
import delimited "data.csv", rowrange(1:1000) clear  // Try importing in chunks
```

---

## Post-Import Diagnostic Commands

```stata
describe                  // Variable types and labels
summarize                 // Summary statistics
codebook, compact         // Detailed variable info
list in 1/10              // First 10 observations
count                     // Number of observations
misstable summarize       // Missing value patterns
duplicates report id      // Check for duplicates
```

## User-Written Import Extensions

```stata
ssc install jsonio          // JSON import/export
ssc install usespss         // SPSS file import
ssc install import_sas      // SAS file import
ssc install use13           // Older Stata format converter
```
