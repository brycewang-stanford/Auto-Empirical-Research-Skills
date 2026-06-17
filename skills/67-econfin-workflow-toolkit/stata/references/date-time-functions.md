# Date and Time Functions in Stata

## How Stata Stores Dates

Dates are numeric values counting time units from January 1, 1960. This enables arithmetic and comparisons with standard operators.

## Date Formats

| Format | Description | Example Display |
|--------|-------------|-----------------|
| `%td` | Daily | 15feb2023 |
| `%tw` | Weekly | 2023w7 |
| `%tm` | Monthly | 2023m2 |
| `%tq` | Quarterly | 2023q1 |
| `%th` | Half-yearly | 2023h1 |
| `%ty` | Yearly | 2023 |
| `%tc` | Datetime (milliseconds) | 15feb2023 14:30:00 |
| `%tb` | Business dates | Varies by calendar |

## Creating Dates from Components

| Function | Purpose |
|----------|---------|
| `mdy(m,d,y)` | Month, day, year -> daily date |
| `ym(y,m)` | Year, month -> monthly date |
| `yq(y,q)` | Year, quarter -> quarterly date |
| `yw(y,w)` | Year, week -> weekly date |
| `mdyhms(m,d,y,h,m,s)` | Full datetime |

```stata
gen date_var = mdy(month, day, year)
format date_var %td

gen month_var = ym(year, month)
format month_var %tm

gen double datetime_var = mdyhms(2, 15, 2023, 14, 30, 0)
format datetime_var %tc
```

## Converting Between Date Types

| Function | Converts |
|----------|----------|
| `mofd(d)` | Daily -> monthly |
| `qofd(d)` | Daily -> quarterly |
| `wofd(d)` | Daily -> weekly |
| `yofd(d)` | Daily -> yearly |
| `dofm(m)` | Monthly -> daily (first day) |
| `dofq(q)` | Quarterly -> daily (first day) |
| `dofw(w)` | Weekly -> daily (first day) |
| `dofc(c)` | Datetime -> daily |

```stata
gen monthly = mofd(date_var)
format monthly %tm

gen daily = dofm(monthly)     // Returns first day of month
format daily %td
```

## Converting String Dates

### date() Function

| Mask Symbol | Meaning |
|-------------|---------|
| `D` | Day |
| `M` | Month (numeric, full name, or 3-letter) |
| `Y` | Year (4-digit) |
| `20Y` / `19Y` | Two-digit year (assumes 2000s / 1900s) |
| `#` | Ignore this element |

```stata
gen date1 = date("2023-02-15", "YMD")
gen date2 = date("15/02/2023", "DMY")
gen date3 = date("Feb. 15 2023", "MDY")
gen date4 = date("12/31/99", "MD19Y")   // Assumes 1999
format date1 %td
```

The function handles various delimiters (`-`, `/`, `.`, spaces) and month formats (numeric, abbreviated, full name).

### clock() for Datetime
```stata
gen double dt = clock("2023-02-15 14:30:00", "YMDhms")
format dt %tc
```

### Other String-to-Date Functions
```stata
monthly("2023-02", "YM")
quarterly("2023-Q1", "YQ")
weekly("2023-W7", "YW")
```

## Extracting Date Components

### From Daily Dates
| Function | Returns | Range |
|----------|---------|-------|
| `year(d)` | Year | 1000-9999 |
| `month(d)` | Month | 1-12 |
| `day(d)` | Day of month | 1-31 |
| `quarter(d)` | Quarter | 1-4 |
| `dow(d)` | Day of week | 0 (Sun) - 6 (Sat) |
| `doy(d)` | Day of year | 1-366 |
| `week(d)` | Week of year | 1-52 |

### From Datetime
```stata
gen dt_year = year(dofc(dt))
gen hour_val = hh(dt)
gen minute_val = mm(dt)
gen second_val = ss(dt)
```

### Current Date/Time
```stata
gen current_date = today()
format current_date %td

gen double current_datetime = now()
format current_datetime %tc
```

### Month/Leap Year Functions
```stata
daysinmonth(mdy(2, 15, 2023))           // 28
firstdayofmonth(mdy(2, 15, 2023))       // Feb 1, 2023
lastdayofmonth(mdy(2, 15, 2023))        // Feb 28, 2023
isleapyear(mdy(2, 15, 2024))            // 1

// Stata 17+
age(birthdate, today())                  // Age in complete years
age_frac(birthdate, today())             // Precise fractional age
```

## Date Arithmetic

Dates are numbers, so arithmetic works directly.

```stata
gen days_elapsed = date2 - date1               // Days between dates
gen end_date = start_date + 30                 // Add 30 days
gen last_week = today() - 7

// Datetime: subtraction yields milliseconds
gen duration_hours = (end_time - start_time) / (60 * 60 * 1000)

// Add 2 hours to datetime
gen double new_time = original_time + (2 * 60 * 60 * 1000)

// Stata 17+
gen years_diff = datediff(date1, date2, "year")
gen months_diff = datediff(date1, date2, "month")
gen exact_months = datediff_frac(date1, date2, "month")
```

### Using Dates in Conditions
```stata
keep if date_var > mdy(3, 15, 2020)
gen pandemic = (date_var >= mdy(3, 15, 2020) & date_var <= mdy(12, 31, 2021))
keep if year(date_var) == 2023
```

## Time-Series Setup

### tsset Command
```stata
gen quarterly = yq(year, quarter)
format quarterly %tq
tsset quarterly

// Panel time series
tsset company_id date_var
```

### Time-Series Operators (require tsset)
| Operator | Meaning |
|----------|---------|
| `L.` / `L2.` | Lag / 2-period lag |
| `F.` / `F3.` | Lead / 3-period lead |
| `D.` | First difference |

```stata
gen price_lag1 = L.price
gen price_change = D.price
gen price_lead = F.price
```

### Subsetting Time Periods
```stata
regress unemp interest if tin(1957q1, 1999q4)     // Inclusive
regress unemp interest if twithin(2000q1, 2005q1)  // Exclusive
```

### Converting Daily to Other Frequencies
```stata
gen monthly = mofd(date_var)
format monthly %tm
collapse (mean) price volume, by(monthly)
tsset monthly
```

## Business Dates

Business calendars skip non-trading days (weekends, holidays).

```stata
// Create calendar from data gaps
bcal create sp500, from(date)
format trading_date %tbsp500
tsset trading_date

// L. and F. now reference trading days, not calendar days
gen prev_price = L.price    // Previous TRADING day
gen price_5days = L5.price  // 5 TRADING days ago
```

## Display Format Customization

```stata
format date_var %tdMon_dd,_CCYY    // Feb 15, 2023
format date_var %tdCCYY-NN-DD      // 2023-02-15
format date_var %tdDD.Month.CCYY   // 15.February.2023
```

| Code | Meaning |
|------|---------|
| `DD` | 2-digit day |
| `NN` | 2-digit month |
| `CCYY` | 4-digit year |
| `Month` / `Mon` | Full / 3-letter month |
| `hh` / `HH` | 24-hour / 12-hour |
| `MM` | Minute |
| `SS` | Second |
| `am` | AM/PM indicator |
| `_` | Single space |

## Common Recipes

### Age Calculation
```stata
gen age_years = floor((today() - birthdate) / 365.25)
// Or Stata 17+:
gen age_exact = age(birthdate, today())
```

### Fiscal Years (April start)
```stata
gen fiscal_year = year(date_var)
replace fiscal_year = fiscal_year + 1 if month(date_var) >= 4
```

### First/Last Day of Quarter
```stata
gen quarter_start = dofq(qofd(date_var))
gen quarter_end = dofq(qofd(date_var) + 1) - 1
```

### Excel Date Conversion
```stata
// Excel counts from Jan 1, 1900; Stata from Jan 1, 1960
// Difference: 21,916 days
gen stata_date = excel_date - 21916
format stata_date %td
```
**Note:** Excel incorrectly treats 1900 as a leap year; dates before March 1, 1900 may need adjustment.

### Fill Missing Dates / Identify Gaps
```stata
bysort id (date_var): replace date_var = date_var[_n-1] if missing(date_var)
sort date_var
gen date_gap = date_var - date_var[_n-1] if _n > 1
```

### Date Validation
```stata
gen valid_date = !missing(mdy(month, day, year))
gen in_range = (date_var >= mdy(1, 1, 2000) & date_var <= mdy(12, 31, 2023))
```
