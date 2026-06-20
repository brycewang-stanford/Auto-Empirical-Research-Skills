# External Tools Integration

## Contents

- [Python Integration](#python-integration)
- [R Integration](#r-integration)
- [LaTeX and Stata Workflows](#latex-and-stata-workflows)
- [Excel Automation](#excel-automation)
- [Database Connections](#database-connections)
- [Web Scraping and APIs](#web-scraping-and-apis)
- [Shell Commands and System Integration](#shell-commands-and-system-integration)
- [Markdown and Dynamic Documents](#markdown-and-dynamic-documents)
- [Git Version Control](#git-version-control)
- [Package Management](#package-management)
- [Best Practices](#best-practices)

## Python Integration

### The python Command (Stata 16+)

```stata
* Execute single Python command
python: print("Hello from Python!")

* Execute Python block
python:
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(f"Mean: {arr.mean()}")
end

* Use Python script file
python script "analysis.py"
```

### Exchanging Data Between Stata and Python

```stata
sysuse auto, clear

python:
from sfi import Data, Scalar, Macro

# Read Stata data into Python
price = Data.get("price")
mpg = Data.get("mpg")

# Perform Python calculations
import numpy as np
correlation = np.corrcoef(price, mpg)[0,1]

# Send result back to Stata
Scalar.setValue("r(corr)", correlation)
end

* Access result in Stata
display "Correlation: " r(corr)
```

### Reading All Data into pandas

```stata
python:
import pandas as pd
from sfi import Data, Macro

df = pd.DataFrame({
    'price': Data.get("price"),
    'mpg': Data.get("mpg"),
    'weight': Data.get("weight")
})

summary = df.groupby(pd.cut(df['mpg'], bins=3)).agg({
    'price': ['mean', 'std'],
    'weight': 'mean'
})
print(summary)
end
```

### Machine Learning with scikit-learn

```stata
sysuse auto, clear
keep if !missing(price, mpg, weight, foreign)

python:
from sfi import Data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

X = np.column_stack([
    Data.get("mpg"),
    Data.get("weight"),
    Data.get("foreign")
])
y = Data.get("price")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

print(f"R-squared: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

for i, imp in enumerate(rf.feature_importances_):
    print(f"Feature {i+1} importance: {imp:.4f}")
end
```

### PyStata: Running Stata from Python (Stata 17+)

```python
import stata_setup
stata_setup.config("/usr/local/stata17", "mp")

from pystata import stata

stata.run("sysuse auto, clear")
stata.run("summarize price mpg")
stata.run("do analysis.do")
```

#### Mixed Python-Stata Workflow

```python
import pandas as pd
from pystata import stata

df = pd.read_csv("raw_data.csv")
df = df.dropna()
df['log_income'] = np.log(df['income'])
df.to_stata("prepared_data.dta")

stata.run("""
    use prepared_data, clear
    regress log_income education experience
    estimates store model1
    esttab model1 using results.tex, replace
""")
```

---

## R Integration

### The rcall Package

```stata
* Install from GitHub
net install github, from("https://haghish.github.io/github/")
github install haghish/rcall

* Execute R command
rcall: print("Hello from R!")

* Execute R block
rcall:
x <- c(1, 2, 3, 4, 5)
mean_x <- mean(x)
print(paste("Mean:", mean_x))
end

* Use R script file
rcall script analysis.R
```

### Data Exchange with R

```stata
sysuse auto, clear

rcall:
# Data is automatically available as a data frame called df
library(dplyr)

summary_stats <- df %>%
    group_by(foreign) %>%
    summarise(
        mean_price = mean(price),
        mean_mpg = mean(mpg),
        n = n()
    )
print(summary_stats)
end

* Retrieve R objects
rcall: summary_stats
```

### Graphics with ggplot2

```stata
sysuse auto, clear

rcall:
library(ggplot2)

p <- ggplot(df, aes(x=mpg, y=price, color=factor(foreign))) +
    geom_point(size=3, alpha=0.6) +
    geom_smooth(method="lm", se=TRUE) +
    scale_color_manual(
        values=c("0"="blue", "1"="red"),
        labels=c("Domestic", "Foreign"),
        name="Origin"
    ) +
    labs(title="Price vs. MPG by Origin", x="Miles per Gallon", y="Price (USD)") +
    theme_minimal()

ggsave("price_mpg.png", p, width=8, height=6, dpi=300)
end
```

### Statistical Modeling in R

```stata
sysuse auto, clear

rcall:
library(broom)

model <- glm(foreign ~ mpg + weight + price, data=df, family=binomial(link="logit"))
results <- tidy(model)
print(results)
glance(model)

# Return coefficients to Stata
coef_mpg <- coef(model)["mpg"]
end

* Access R results in Stata
rcall: coef_mpg
```

---

## LaTeX and Stata Workflows

### Exporting Tables with esttab

```stata
sysuse auto, clear

regress price mpg weight
estimates store m1
regress price mpg weight foreign
estimates store m2
regress price mpg weight foreign length
estimates store m3

esttab m1 m2 m3 using "regression_results.tex", ///
    replace label booktabs ///
    title("Price Regression Models") ///
    mtitles("Model 1" "Model 2" "Model 3") ///
    addnote("Standard errors in parentheses" ///
            "* p<0.05, ** p<0.01, *** p<0.001") ///
    star(* 0.05 ** 0.01 *** 0.001) ///
    stats(N r2 r2_a, labels("Observations" "R-squared" "Adjusted R-squared"))
```

### Using texdoc for Dynamic LaTeX Documents

```stata
ssc install texdoc

texdoc init analysis_report.tex, replace

/***
\documentclass{article}
\usepackage{booktabs}
\usepackage{graphicx}
\title{Stata Analysis Report}
\begin{document}
\maketitle
\section{Data Description}
***/

texdoc stlog
sysuse auto, clear
summarize price mpg weight
texdoc stlog close

/***
\section{Regression Analysis}
***/

texdoc stlog
regress price mpg weight foreign
texdoc stlog close

/***
\section{Visualization}
***/

graph twoway scatter price mpg, title("Price vs. MPG")
graph export "scatter.png", replace

/***
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{scatter.png}
\caption{Price vs. MPG}
\end{figure}
\end{document}
***/

texdoc close
```

### Automated LaTeX Report Program

```stata
program define latex_report
    version 16
    syntax using/, dataset(string) outcome(string) predictors(string)

    use "`dataset'", clear
    texdoc init "`using'", replace

    /***
    \documentclass[12pt]{article}
    \usepackage{booktabs, graphicx, float}
    \begin{document}
    \section{Automated Analysis Report}
    ***/

    texdoc stlog
    summarize `outcome' `predictors'
    texdoc stlog close

    texdoc stlog
    regress `outcome' `predictors'
    estimates store model
    texdoc stlog close

    esttab model using "temp_table.tex", booktabs replace label

    /***
    \input{temp_table.tex}
    \end{document}
    ***/

    texdoc close
end

latex_report using "report.tex", ///
    dataset("auto.dta") outcome("price") predictors("mpg weight foreign")
```

---

## Excel Automation

### The putexcel Command

```stata
* Create new Excel file
putexcel set "results.xlsx", replace

* Write values
putexcel A1 = "Analysis Results"
putexcel A2 = "Variable" B2 = "Mean" C2 = "SD"

sysuse auto, clear
summarize price
putexcel A3 = "Price" B3 = r(mean) C3 = r(sd)
```

### Exporting Matrices

```stata
correlate price mpg weight length, covariance
matrix C = r(C)
putexcel set "correlation.xlsx", replace
putexcel A1 = matrix(C), names
```

### Advanced Excel Formatting

```stata
putexcel set "formatted_results.xlsx", replace

* Title with formatting
putexcel A1 = "Automobile Analysis Report", ///
    bold font(Arial, 14) fpattern(solid, "lightblue")

* Headers
putexcel A3 = "Statistic" B3 = "Value", bold underline border(bottom)

summarize price
local row = 4
putexcel A`row' = "Mean Price"
putexcel B`row' = r(mean), nformat(#,##0.00)

local ++row
putexcel A`row' = "SD Price"
putexcel B`row' = r(sd), nformat(#,##0.00)

* Add formula
local ++row
putexcel A`row' = "Range"
putexcel B`row' = formula(B`=`row'-1'-B`=`row'-2'), nformat(#,##0)
```

### Multiple Sheets

```stata
sysuse auto, clear

* Sheet 1: Summary statistics
putexcel set "complete_report.xlsx", sheet("Summary") replace
putexcel A1 = "Summary Statistics", bold font(Arial, 12)
summarize price mpg weight length
matrix define stats = r(StatTotal)
putexcel A3 = matrix(stats), names

* Sheet 2: Regression results
putexcel set "complete_report.xlsx", sheet("Regression") modify
regress price mpg weight foreign
matrix define coef = r(table)
putexcel A3 = matrix(coef), names rownames

* Sheet 3: Embedded graph
scatter price mpg
graph export "temp_graph.png", replace
putexcel set "complete_report.xlsx", sheet("Graphs") modify
putexcel A2 = image("temp_graph.png")
erase "temp_graph.png"
```

### Dynamic Excel Dashboard Program

```stata
program define excel_dashboard
    syntax using/, dataset(string)

    use "`dataset'", clear
    putexcel set "`using'", replace

    putexcel A1:E1, merge
    putexcel A1 = "Executive Dashboard", ///
        bold font(Arial, 16) fpattern(solid, "navy") fontcolor(white) hcenter

    putexcel A5 = "Total Observations"
    putexcel B5 = _N, nformat(#,##0)

    quietly summarize price
    putexcel A6 = "Average Price"
    putexcel B6 = r(mean), nformat($#,##0.00)

    putexcel B5:B7, nformat(#,##0.00) fpattern(solid, "lightyellow") border(all)

    putexcel A10 = "Detailed Data", bold
    export excel A11:E100, firstrow(variables)
end
```

---

## Database Connections

### ODBC

```stata
* List available ODBC data sources
odbc list

* View tables / describe structure
odbc query "datasource_name"
odbc describe "table_name", dsn("datasource_name")

* Load entire table
odbc load, table("customers") dsn("sales_db") clear

* Load with SQL query
odbc load, exec("SELECT * FROM customers WHERE country='USA'") ///
    dsn("sales_db") clear

* Load specific columns
odbc load customerid customername country, ///
    table("customers") dsn("sales_db") clear

* Write data to database
odbc insert customerid customername country, ///
    as("new_customers") dsn("sales_db") create

* Execute arbitrary SQL
odbc exec("UPDATE customers SET status='active' WHERE country='USA'"), ///
    dsn("sales_db")
```

### Complex SQL Queries

```stata
* Join multiple tables
odbc load, ///
    exec("SELECT c.customerid, c.customername, o.orderdate, o.amount " ///
         "FROM customers c " ///
         "INNER JOIN orders o ON c.customerid = o.customerid " ///
         "WHERE o.orderdate >= '2023-01-01'") ///
    dsn("sales_db") clear
```

### JDBC Connections (Stata 15+)

```stata
set java_heapmax 1g

jdbc connect jdbc:mysql://localhost:3306/mydb, ///
    user(username) password(password)

jdbc load, exec("SELECT * FROM sales WHERE year = 2023") clear

jdbc disconnect
```

---

## Web Scraping and APIs

### Simple Downloads with copy

```stata
copy "https://example.com/data.csv" "local_data.csv", replace
import delimited "local_data.csv", clear
```

### API Integration with Python

```stata
python:
import requests
import json
from sfi import Data, Macro

url = "https://api.example.com/data"
params = {'key': 'YOUR_API_KEY', 'format': 'json'}
response = requests.get(url, params=params)

data = response.json()
ids = [item['id'] for item in data['results']]
values = [item['value'] for item in data['results']]

Data.addObs(len(ids))
Data.store('id', None, ids)
Data.store('value', None, values)
end
```

### Reusable API Wrapper

```stata
capture program drop api_get
program define api_get
    version 16
    syntax, url(string) [key(string) params(string)]

    python:
    import requests
    from sfi import Macro

    url = Macro.getLocal("url")
    api_key = Macro.getLocal("key")
    params_str = Macro.getLocal("params")

    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    params = {}
    if params_str:
        for param in params_str.split(','):
            key, val = param.split('=')
            params[key.strip()] = val.strip()

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Success: Retrieved {len(data)} records")
    else:
        print(f"Error: {response.status_code}")
    end
end

api_get, url("https://api.example.com/data") ///
    key("your_api_key") params("limit=100,offset=0")
```

### Automated Data Updates from Web

```stata
program define update_from_web
    version 16
    syntax, source(string) destination(string)

    copy "`source'" "temp_download.csv", replace
    import delimited "temp_download.csv", clear
    assert _N > 0

    generate download_date = clock("`c(current_date)' `c(current_time)'", "DMY hms")
    format download_date %tc

    save "`destination'", replace
    erase "temp_download.csv"
    display as result "Data updated successfully: " _N " observations"
end
```

---

## Shell Commands and System Integration

### Shell Commands

```stata
* Execute shell command (opens new window)
shell ls -la

* Run command inline (doesn't wait)
! ls -la

* Platform-specific
if "`c(os)'" == "Unix" {
    ! rm tempfile.txt
}
else {
    ! del tempfile.txt
}

* Capture shell output
shell ls -la > file_list.txt
```

### File System Operations

```stata
mkdir "output/tables"
mkdir "output/figures"
copy "source.dta" "backup/source.dta", replace
erase "temporary.dta"

* Check file existence
capture confirm file "data.dta"
if _rc {
    display "File does not exist"
}
```

### Batch Processing / Parallel Execution

```stata
* Create shell script from Stata
file open script using "run_analysis.sh", write replace
file write script "#!/bin/bash" _n
file write script "stata-mp -b do analysis.do" _n
file write script "stata-mp -b do graphs.do" _n
file write script "pdflatex report.tex" _n
file close script
! chmod +x run_analysis.sh

* Create multiple do-files for parallel execution
forvalues i = 1/10 {
    file open dofile using "process_`i'.do", write replace
    file write dofile "use full_data, clear" _n
    file write dofile "keep if group == `i'" _n
    file write dofile "regress y x1 x2 x3" _n
    file write dofile "estimates save results_`i'" _n
    file close dofile
}

* Run in parallel (Unix/Linux)
! for i in {1..10}; do stata-mp -b do process_$i.do & done; wait
```

### System Information

```stata
display "`c(username)'"
display "`c(hostname)'"
display "`c(pwd)'"
display "`c(os)'"
```

---

## Markdown and Dynamic Documents

### The markstat Package

```stata
ssc install markstat
ssc install whereis
whereis pandoc "/usr/local/bin/pandoc"
```

#### Stata Markdown (.stmd) Example

The `.stmd` format embeds `{stata}` code blocks in markdown. Inline expressions use `` `s expression' `` syntax:

```
The R-squared is `s %4.3f e(r2)'.
```

```stata
* Compile to various formats
markstat using analysis.stmd, mathjax   // HTML
markstat using analysis.stmd, pdf       // PDF (requires LaTeX)
markstat using analysis.stmd, docx      // Word
```

### The dyndoc Command (Stata 15+)

```stata
dyndoc analysis.md, replace
dyndoc analysis.md, replace template(custom_template.html)
```

Inline expressions in dyndoc: `` `s c(current_date)' ``, `` `%6.2f _b[mpg]' ``

### Markdown Report Generator Program

```stata
program define markdown_report
    version 16
    syntax using/, dataset(string) outcome(string) predictors(string)

    file open md using "`using'", write replace

    file write md "# Automated Analysis Report" _n _n
    file write md "**Date**: `c(current_date)'" _n _n

    use "`dataset'", clear

    file write md "## Descriptive Statistics" _n _n
    file write md "| Variable | Mean | SD | Min | Max |" _n
    file write md "|----------|------|----|----|-----|" _n

    foreach var in `outcome' `predictors' {
        quietly summarize `var'
        file write md "| `var' | " %9.2f (r(mean)) " | " ///
                      %9.2f (r(sd)) " | " ///
                      %9.2f (r(min)) " | " ///
                      %9.2f (r(max)) " |" _n
    }

    quietly regress `outcome' `predictors'
    file write md _n "## Regression Results" _n _n
    file write md "- R-squared: " %6.4f (e(r2)) _n
    file write md "- N: " (e(N)) _n _n

    file close md
    display "Markdown report created: `using'"
end
```

---

## Git Version Control

### .gitignore for Stata Projects

```stata
file open gitignore using ".gitignore", write replace
file write gitignore "*.log" _n
file write gitignore "*.smcl" _n
file write gitignore "*.dta~" _n
file write gitignore "*~" _n
file write gitignore "temp*.dta" _n
file write gitignore "temp*.do" _n
file write gitignore ".DS_Store" _n
file write gitignore "Thumbs.db" _n
file close gitignore
```

### Git Commands from Stata

```stata
! git init
! git add .
! git commit -m "Initial commit"
! git checkout -b analysis-update
! git status
! git pull origin main
! git push origin main
```

### Automated Git Save Program

```stata
program define git_save
    syntax using/, message(string)
    save "`using'", replace
    ! git add "`using'"
    ! git commit -m "`message'"
    display "File saved and committed: `using'"
end
```

### Versioned Analysis Pipeline

```stata
program define versioned_analysis
    version 16
    syntax, project(string) [branch(string)]

    cd "`project'"

    if "`branch'" != "" {
        ! git checkout -b `branch'
    }

    do "code/01_import.do"
    ! git add "code/01_import.do" "data/imported.dta"
    ! git commit -m "Data import completed"

    do "code/02_clean.do"
    ! git add "code/02_clean.do" "data/clean.dta"
    ! git commit -m "Data cleaning completed"

    do "code/03_analysis.do"
    ! git add "code/03_analysis.do" "output/*"
    ! git commit -m "Analysis completed"

    local date = subinstr("`c(current_date)'", " ", "-", .)
    ! git tag -a "analysis-`date'" -m "Analysis completed on `c(current_date)'"
end
```

---

## Package Management

### SSC (Statistical Software Components)

```stata
* Search and install
ssc describe estout
findit regression tables
ssc install estout
ssc install outreg2
ssc install coefplot

* Update
adoupdate              // check all
ssc install estout, replace  // reinstall specific

* Uninstall
ssc uninstall estout
```

### Managing ado Paths

```stata
adopath                    // view ado path
adopath + "/path/to/my/ado" // add custom directory
ado dir                    // list installed packages
ado describe estout        // describe specific package
```

### GitHub Package Installation

```stata
net install github, from("https://haghish.github.io/github/")
github install haghish/markdoc
github install gtools-econ/stata-gtools
github update markdoc
github install user/package, version("abc123def")  // specific commit
```

### Creating Custom Packages

#### Package Structure

```stata
* File: mypackage.ado
program define mypackage
    version 16.0
    syntax varlist [if] [in], [options]
    display "Running mypackage"
    summarize `varlist' `if' `in'
end
```

#### Help File (mypackage.sthlp)

```
{smcl}
{title:Title}
{p2colset 5 18 20 2}{...}
{p2col :{cmd:mypackage} {hline 2}}Custom analysis package{p_end}

{title:Syntax}
{p 8 17 2}
{cmd:mypackage} {varlist} {ifin} [{cmd:,} {it:options}]

{title:Examples}
{phang}{cmd:. sysuse auto}{p_end}
{phang}{cmd:. mypackage price mpg}{p_end}
```

#### Distribution Files

```
* mypackage.pkg
v 3
d mypackage - Custom analysis package
d Author: Your Name
f mypackage.ado
f mypackage.sthlp

* stata.toc
v 3
d My Stata Packages
p mypackage Custom analysis package
```

---

## Best Practices

### Tool Selection
- **Python**: Machine learning, web scraping, complex data structures
- **R**: Advanced visualization (ggplot2), specialized statistical packages
- **Stata**: Econometric analysis, panel data, survey data
- **LaTeX**: Professional academic reports
- **Excel**: Business stakeholder communication
- **Markdown**: Quick reports, documentation

### Reproducibility
```stata
* Document tool versions
python: import sys; print(f"Python {sys.version}")
rcall: R.version.string
display "Stata version: `c(stata_version)'"
```

### Error Handling Across Tools
```stata
capture {
    python:
    # Python code
    end
}
if _rc {
    display as error "Python execution failed"
    exit _rc
}

capture {
    rcall:
    # R code
    end
}
if _rc {
    display as error "R execution failed"
    exit _rc
}
```

### Performance
- Minimize data transfers between Stata and Python/R -- do bulk operations in the external tool, transfer only results
- Use Mata or Python/Cython for performance-critical sections
