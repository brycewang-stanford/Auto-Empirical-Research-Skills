# String Functions in Stata

## String Basics

- `str1` to `str2045`: Fixed-length strings
- `strL`: Variable-length strings (up to 2 billion characters)

```stata
gen str20 name = "John Doe"
gen strL description = "Long text..."
ds, has(type string)         // Identify all string variables
```

---

## Extraction and Position Functions

### substr(s, n1, n2) - Extract Substring
```stata
display substr("Hello World", 1, 5)     // "Hello"
display substr("Hello World", 7, .)     // "World" (to end)
display substr("Hello World", -5, 5)    // "World" (from end)

gen area_code = substr(phone, 1, 3)
gen first_name = substr(full_name, 1, strpos(full_name, " ") - 1)
```

### strpos(s1, s2) - Find First Occurrence (0 if not found)
```stata
gen has_keyword = (strpos(text, "important") > 0)
gen domain = substr(email, strpos(email, "@") + 1, .)

// Parse delimited data
gen comma_pos = strpos(data, ",")
gen field1 = substr(data, 1, comma_pos - 1)
gen field2 = substr(data, comma_pos + 1, .)
```

### strrpos(s1, s2) - Find Last Occurrence
```stata
gen last_name = substr(full_name, strrpos(full_name, " ") + 1, .)
gen filename = substr(filepath, strrpos(filepath, "/") + 1, .)
```

### strlen(s) - String Length (in bytes)
```stata
gen valid_zip = (strlen(zipcode) == 5)
list name if strlen(name) == 0
```

### indexnot(s1, s2) - First Character Not in s2
```stata
display indexnot("000123", "0")   // 4
gen trimmed = substr(code, indexnot(code, "0"), .)  // Trim leading zeros
```

---

## Replacement Functions

### subinstr(s1, s2, s3, n) - Replace Substring
`n` = number of replacements (`.` for all)

```stata
gen cleaned = subinstr(text, "$", "", .)         // Remove all $
replace price = subinstr(price, ",", "", .)      // Remove commas
gen no_spaces = subinstr(text, " ", "", .)
```

### subinword(s1, s2, s3, n) - Replace Complete Words Only
```stata
display subinword("chev chevette", "chev", "chevrolet", .)
// "chevrolet chevette" -- won't match partial words
```

---

## Case Conversion

```stata
replace state = strupper(state)              // UPPERCASE
replace email = strlower(email)              // lowercase
replace name = strproper(name)               // Proper Case

// Case-insensitive comparison
gen match = (strlower(text1) == strlower(text2))
```

---

## Regular Expressions

### regexm(s, re) - Match (returns 1/0)
```stata
gen has_number = regexm(text, "[0-9]")
gen valid_email = regexm(email, "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
gen is_phone = regexm(text, "^\([0-9]{3}\) [0-9]{3}-[0-9]{4}$")
gen is_zip = regexm(zipcode, "^[0-9]{5}(-[0-9]{4})?$")
gen is_url = regexm(text, "^https?://")
```

### regexr(s, re, replacement) - Replace First Match
```stata
gen clean = regexr(text, "[0-9]+", "")              // Remove first number group
gen alpha_only = regexr(text, "[^a-zA-Z ]", "")     // Remove non-alpha
replace text = regexr(text, "^ +", "")              // Leading spaces
replace text = regexr(text, " +$", "")              // Trailing spaces
```

### regexs(n) - Extract Captured Groups (after regexm)
```stata
// Extract area code from phone
gen has_area = regexm(phone, "^\(([0-9]{3})\)")
gen area_code = regexs(1) if has_area

// Parse "Last, First" format
gen has_comma = regexm(name, "^([^,]+), ([^,]+)$")
gen last_name = regexs(1) if has_comma
gen first_name = regexs(2) if has_comma

// Extract numbers from mixed text
gen has_num = regexm(text, "([0-9]+)")
gen number = real(regexs(1)) if has_num
```

---

## Trimming Functions

```stata
trim(s)       // or strtrim(s)   - Remove leading AND trailing spaces
ltrim(s)      // or strltrim(s)  - Remove leading spaces only
rtrim(s)      // or strrtrim(s)  - Remove trailing spaces only
stritrim(s)   // Reduce multiple internal spaces to single spaces

// Complete cleanup
replace text = trim(stritrim(text))

// Clean all string variables
ds, has(type string)
foreach var of varlist `r(varlist)' {
    replace `var' = trim(`var')
}
```

---

## Parsing Functions

### word(s, n) - Extract Word by Position
```stata
gen first_name = word(full_name, 1)
gen last_name = word(full_name, -1)      // Last word
gen middle = word(full_name, 2) if wordcount(full_name) >= 3
```

### wordcount(s) - Count Words
```stata
gen num_words = wordcount(description)
keep if wordcount(comment) >= 5
```

### split - Split String into Variables
```stata
split full_name                          // By spaces: full_name1, full_name2...
split phone, parse("-")                  // By delimiter
split date_str, parse("/") generate(d)   // Custom variable names
```

### tokenize - Parse into Local Macros
```stata
tokenize "one two three"
display "`1'"    // one
display "`2'"    // two

tokenize "apple,banana,cherry", parse(",")
display "`1'"    // apple
display "`3'"    // banana (delimiters are tokens too)
```

---

## String/Number Conversion

### real(s) - String to Number (missing if fails)
```stata
gen price_num = real(price_str)
list id price_str if missing(real(price_str))  // Find non-numeric values
```

### string(n [, format]) - Number to String
```stata
gen id_str = string(id)
gen price_str = string(price, "%9.2f")
gen id_padded = string(id, "%05.0f")           // Zero-padded
gen pct_str = string(pct * 100, "%5.1f") + "%"
```

### destring / tostring - Batch Conversion
```stata
destring price, replace
destring price, ignore("$,") replace           // Remove chars first
destring value, force replace                  // Force, errors become missing
destring _all, replace                         // All variables

tostring id, replace
tostring price, format(%9.2f) replace
tostring id, format(%05.0f) replace            // Zero-padded
```

### encode / decode - With Value Labels
```stata
encode color, generate(color_num)   // String -> labeled numeric (alphabetical codes)
decode color_num, generate(color_str)  // Labeled numeric -> string
```

---

## Unicode String Functions

Use `ustr*` functions for international text (multi-byte characters). Standard functions operate on bytes; Unicode functions operate on characters.

```stata
display strlen("cafe\u0301")     // 5 (bytes)
display ustrlen("cafe\u0301")    // 4 (characters)
```

### Key Unicode Functions
```stata
ustrlen(s)                    // Character count (not bytes)
usubstr(s, n1, n2)           // Extract by character position
ustrpos(s1, s2)              // Find by character position
ustrupper(s) / ustrlower(s) / ustrproper(s)  // Case conversion
ustrtrim(s) / ustrltrim(s) / ustrrtrim(s)    // Trimming
ustrword(s, n)               // Extract word
ustrwordcount(s)             // Count words
ustrregexm(s, re)            // Unicode regex match
ustrregexrf(s, re, repl)     // Replace first match
ustrregexra(s, re, repl)     // Replace ALL matches
```

---

## Practical Recipes

### Clean Currency Data
```stata
replace price = subinstr(price, "$", "", .)
replace price = subinstr(price, ",", "", .)
destring price, replace
```

### Handle Negative Numbers in Parentheses
```stata
gen is_negative = (strpos(amount, "(") > 0)
replace amount = subinstr(amount, "(", "", .)
replace amount = subinstr(amount, ")", "", .)
destring amount, replace
replace amount = -amount if is_negative
```

### Clean Phone Numbers to Standard Format
```stata
replace phone = subinstr(phone, "(", "", .)
replace phone = subinstr(phone, ")", "", .)
replace phone = subinstr(phone, "-", "", .)
replace phone = subinstr(phone, " ", "", .)
gen phone_formatted = "(" + substr(phone,1,3) + ") " + substr(phone,4,3) + "-" + substr(phone,7,4)
```

### Standardize Survey Responses
```stata
replace response = strlower(trim(response))
replace response = "yes" if inlist(response, "y", "yes", "yeah", "yep")
replace response = "no" if inlist(response, "n", "no", "nope")
```

### Create Matching Keys
```stata
gen match_key = strlower(trim(name))
replace match_key = subinstr(match_key, " ", "", .)
replace match_key = subinstr(match_key, ".", "", .)
replace match_key = subinstr(match_key, ",", "", .)
```

### Extract Dates from Text
```stata
gen has_date = regexm(text, "([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})")
gen month = real(regexs(1)) if has_date
gen day = real(regexs(2)) if has_date
gen year = real(regexs(3)) if has_date
gen date = mdy(month, day, year) if has_date
format date %td
```

### Replace Missing Indicators
```stata
replace text = "" if inlist(strlower(trim(text)), "na", "n/a", "missing", ".", "null")
```

### Batch Operations on All String Variables
```stata
ds, has(type string)
foreach var of varlist `r(varlist)' {
    quietly {
        replace `var' = trim(stritrim(`var'))
        replace `var' = strproper(strlower(`var'))
    }
}
```

### Keyword-Based Categorization
```stata
gen category = ""
replace category = "tech" if regexm(strlower(text), "computer|software|digital")
replace category = "health" if regexm(strlower(text), "medical|health|hospital")
replace category = "finance" if regexm(strlower(text), "bank|finance|investment")
```
