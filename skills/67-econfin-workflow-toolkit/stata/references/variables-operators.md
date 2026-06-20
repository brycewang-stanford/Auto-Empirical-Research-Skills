# Variables and Operators in Stata

## Variable Types

### Numeric Variables

| Storage Type | Bytes | Range | Description |
|-------------|-------|-------|-------------|
| `byte` | 1 | -127 to 100 | Small integers |
| `int` | 2 | -32,767 to 32,740 | Medium integers |
| `long` | 4 | -2,147,483,647 to 2,147,483,620 | Large integers |
| `float` | 4 | +/-1.7e+38 | Floating point (default) |
| `double` | 8 | +/-8.9e+307 | High precision floating point |

Only `float` and `double` can hold decimals.

```stata
describe          // View current variable types
recast byte age   // Change storage type
recast double price
```

### String Variables

- `str1` to `str2045`: Fixed-length strings (Stata 13+)
- `strL`: Variable-length strings (up to 2 billion characters)

```stata
gen str20 name = "John Doe"
recast strL description
```

**Best Practice:** Categorical variables should be stored as numeric with value labels, not strings.

### Date and Time Variables

Stored as numbers representing units since January 1, 1960:

| Type | Format | Unit |
|------|--------|------|
| Daily | `%td` | Days |
| Weekly | `%tw` | Weeks |
| Monthly | `%tm` | Months |
| Quarterly | `%tq` | Quarters |
| Yearly | `%ty` | Years |
| Datetime | `%tc` | Milliseconds |

```stata
gen date_var = date(string_date, "DMY")
format date_var %td

gen year = year(date_var)
gen month = month(date_var)

gen double datetime_var = clock(string_datetime, "DMYhms")
format datetime_var %tc
```

## Variable Naming Rules

- Up to 32 characters
- Must start with letter or underscore
- Letters, numbers, underscores only
- **Case-sensitive**: `Age` and `age` are different
- Cannot use reserved words (`if`, `in`, `using`)
- Use lowercase with underscores for readability

## Operators

### Arithmetic
| Operator | Description |
|----------|-------------|
| `+`, `-`, `*`, `/` | Basic arithmetic |
| `^` | Exponentiation |
| `-` (prefix) | Negation |

### Relational
| Operator | Description |
|----------|-------------|
| `==` | Equal to |
| `!=` or `~=` | Not equal to |
| `>`, `>=`, `<`, `<=` | Comparisons |

Returns 1 if true, 0 if false.

### Logical
| Operator | Description |
|----------|-------------|
| `&` | AND |
| `|` | OR |
| `!` or `~` | NOT |

### Operator Precedence (highest to lowest)
1. Parentheses `( )`
2. Negation: `-`, `!`, `~`
3. `^`
4. `*`, `/`
5. `+`, `-`
6. Relational: `>`, `>=`, `<`, `<=`, `==`, `!=`
7. `&`
8. `|`

**Key:** `&` binds tighter than `|`. Use parentheses for clarity:
```stata
gen flag = (age > 18 & income > 50000) | (student == 1)
```

### String Operator
`+` concatenates strings: `gen fullname = firstname + " " + lastname`

## Missing Values

Stata has 27 missing values: `.`, `.a` through `.z`

### Critical: Missing as Positive Infinity

**Missing values are treated as larger than any number.** This affects conditional statements:

```stata
// WRONG - includes missing values!
list if age > 60

// CORRECT
list if age > 60 & !missing(age)
// or
list if age > 60 & age < .
```

### Common Patterns
```stata
misstable summarize              // Overview of missing data
misstable patterns               // Missing patterns
count if missing(age)

replace income = . if income == 999 | income == -99
mvdecode _all, mv(999=. \ -99=.)    // Batch recode to missing

// Forward fill
bysort id (date): replace value = value[_n-1] if missing(value)
```

## if and in Qualifiers

### if Qualifier
```stata
summarize income if age > 25
count if age >= 18 & age <= 65
gen eligible = 1 if (age >= 18 & citizen == 1) | (age >= 21 & resident == 1)
list if inlist(state, 1, 2, 5, 10)
count if inrange(age, 18, 65)
```

**Gotcha:** Wildcards (`*`) do NOT work in `if` expressions. They only work in variable lists.

### in Qualifier
```stata
list in 1/10          // First 10
list in -10/l         // Last 10 ('l' = last)
list in f             // First observation
```

When combined, `in` is evaluated first, then `if`.

## Variable Lists and Wildcards

```stata
describe age-education       // Range of variables
summarize inc*               // Wildcard at end
describe *_id                // Wildcard at beginning
drop _*                      // Variables starting with underscore

// By variable type
ds, has(type numeric)        // All numeric variables
ds, has(type string)         // All string variables
ds, has(vallabel)            // Variables with value labels
```

## Temporary Variables

Automatically deleted when program/do-file ends.

```stata
tempvar sumsq
gen `sumsq' = x^2          // Reference with backticks

tempname myscalar mymatrix  // For scalars/matrices
scalar `myscalar' = 100

tempfile mydata             // For temporary datasets
save `mydata'
```

**Key features:**
- Automatic cleanup (even on error)
- Unique names guaranteed by Stata
- Scoped to the program/do-file where created
- Reference with backticks: `` `varname' ``

```stata
// Common pattern: preserve sort order
tempvar orig_order
gen `orig_order' = _n
sort age income
// ... operations ...
sort `orig_order'
```
