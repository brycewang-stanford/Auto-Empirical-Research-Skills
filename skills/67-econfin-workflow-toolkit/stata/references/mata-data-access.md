# Mata-Stata Data Access Interface

## st_data() -- Copy Data

Creates an independent copy of Stata data in a Mata matrix.

```mata
// All observations, named variables
X = st_data(., ("price", "mpg", "weight"))

// Specific observations
X = st_data((1::10), ("mpg", "weight"))

// With selection variable (obs included where selectvar != 0)
foreign_data = st_data(., ("price", "mpg"), "foreign")

// By variable index
X = st_data(., (1, 2, 3))
```

### Critical: Missing Values in Mata

Mata's `mean()`, `variance()`, `correlation()`, and similar aggregate functions **propagate missing values silently** -- they do NOT exclude missings like Stata's `summarize` does. A single missing value in a column makes `mean()` return `.` for that column with no warning.

**Always filter missings before computing:**

```mata
// WRONG: if any value in X is missing, mean() returns "."
result = mean(X)

// RIGHT: drop rows with any missing values
Xclean = select(X, rowmissing(X) :== 0)
result = mean(Xclean)

// RIGHT: drop missings in a single column
x = select(x, missing(x) :== 0)
result = mean(x)
```

**Missing-value detection functions:**

| Function | Returns |
|---|---|
| `missing(x)` | 1 if scalar x is missing, element-wise for matrices |
| `hasmissing(X)` | 1 if any element of X is missing |
| `rowmissing(X)` | Column vector: count of missings per row |
| `colmissing(X)` | Row vector: count of missings per column |

**Tip:** Check `hasmissing()` early and handle it explicitly rather than debugging silent wrong answers downstream.

---

## st_view() -- Create View (No Copy)

Creates a reference into Stata data. **Changes to the view modify Stata data.** More memory-efficient than st_data().

```mata
st_view(X=., ., ("price", "mpg", "weight"))
X[1,1] = 999                   // Modifies Stata data!

// With selection
st_view(domestic=., ., ("price", "mpg"), "!foreign")

// Specific rows
st_view(subset=., (1::10), ("price", "mpg"))
```

### When to Use Which

- **st_data():** Need independent copy, data may change during processing, small datasets
- **st_view():** Large datasets (memory), want to modify Stata data, read-only computation

---

## st_store() -- Write Data

Variables must exist before storing. Matrix dimensions must match.

```mata
// Store to existing variable
mpg_sq = st_data(., "mpg") :^ 2
st_store(., "mpg_squared", mpg_sq)

// Store to specific observations
st_store((1::10), "mpg_squared", J(10, 1, 0))

// With selection
st_store(., "mpg", foreign_mpg, "foreign")
```

### Creating New Variables

```mata
// Single variable
idx = st_addvar("double", "log_price")
st_store(., idx, log(st_data(., "price")))

// Multiple variables
indices = st_addvar("double", ("log_mpg", "log_weight"))
st_store(., indices, (log(st_data(., "mpg")), log(st_data(., "weight"))))
```

---

## Macros: st_local() and st_global()

### Local Macros

```mata
// Read
varname = st_local("varlist")
n = strtoreal(st_local("count"))

// Write
st_local("result", "success")
st_local("mean_mpg", strofreal(mean(st_data(., "mpg"))))
```

### Global Macros

```mata
ds = st_global("dataset")
st_global("obs_count", strofreal(st_nobs()))
```

### Parameter Passing Pattern

```stata
program myprog
    args varname
    mata
        var = st_local("varname")
        data = st_data(., var)
        st_local("mean", strofreal(mean(data)))
        st_local("sd", strofreal(sqrt(variance(data))))
    end
    display "Mean of `varname': `mean'"
end
```

---

## Matrices: st_matrix()

```mata
// Read Stata matrix
M = st_matrix("mymat")

// Read estimation results
V = st_matrix("e(V)")
b = st_matrix("e(b)")
se = sqrt(diagonal(V))'

// Write Mata matrix to Stata
st_matrix("mymat_t", M')
st_replacematrix("e(V)", V)

// Row/column names (stripes)
r = st_matrixrowstripe("e(V)")
c = st_matrixcolstripe("e(V)")

// Set stripes
stripe = (("", "var1") \ ("", "var2"))
st_matrixrowstripe("newmat", stripe)
st_matrixcolstripe("newmat", stripe)
```

---

## Scalars: st_numscalar() and st_strscalar()

```mata
// Read
mean_price = st_numscalar("r(mean)")
r2 = st_numscalar("e(r2)")

// Write
st_numscalar("r(mean)", mean_value)
st_numscalar("gamma", alpha * beta)
```

---

## Variable Utilities

```mata
// Name <-> index conversion
idx = st_varindex("price")
name = st_varname(1)
names = st_varname(1..st_nvar())

// Check existence (returns 0 if not found)
idx = _st_varindex("nonexistent", 0)

// Counts
st_nvar()                       // Number of variables
st_nobs()                       // Number of observations

// Type checking
st_isnumvar(i)                  // Is variable i numeric?
st_vartype("mpg")               // Returns "byte", "int", etc.
```

### Get All Numeric Variables

```mata
string vector get_numeric_vars() {
    real scalar i, nvars
    string vector numvars
    nvars = st_nvar()
    numvars = J(1, 0, "")
    for (i=1; i<=nvars; i++) {
        if (st_isnumvar(i)) numvars = numvars, st_varname(i)
    }
    return(numvars)
}
```

---

## Efficient Data Access Patterns

### 1. Use Views for Large Datasets

```mata
// Slow: copies data
data = st_data(., ("price", "mpg", "weight"))

// Fast: creates reference
st_view(data=., ., ("price", "mpg", "weight"))
```

### 2. Cache Variable Indices

```mata
// Slow: repeated lookups
for (i=1; i<=100; i++) result[i] = mean(st_data(., "price"))

// Fast: lookup once, read once
price_data = st_data(., st_varindex("price"))
for (i=1; i<=100; i++) result[i] = mean(price_data)
```

### 3. Bulk Transfers

```mata
// Slow: one observation at a time
for (i=1; i<=st_nobs(); i++) sum = sum + st_data(i, var)

// Fast: all at once
sum = sum(st_data(., var))
```

### 4. Minimize Context Switches

```stata
// Slow: multiple Mata sessions
mata: x = st_data(., "price")
mata: y = st_data(., "mpg")
mata: z = x :/ y

// Fast: single session
mata
    x = st_data(., "price")
    y = st_data(., "mpg")
    z = x :/ y
end
```

### 5. Preallocate Output Variables

```mata
// Must create variable before storing
idx = st_addvar("double", "newvar")
st_store(., idx, runiform(st_nobs(), 1))
```

---

## Complete Examples

### Z-Score Function

```mata
void create_zscores(string scalar varname, string scalar newvar) {
    real vector data, zscores
    real scalar mu, sd
    data = st_data(., varname)

    // Filter missings -- mean()/variance() propagate them silently
    // (see "Critical: Missing Values in Mata" above)
    real vector clean
    clean = select(data, missing(data) :== 0)
    mu = mean(clean)
    sd = sqrt(variance(clean))

    // Apply to full vector (missings in data stay missing in output)
    zscores = (data :- mu) :/ sd
    st_addvar("double", newvar)
    st_store(., newvar, zscores)
}
```

### Group Statistics with panelsetup()

```mata
void group_stats(string scalar groupvar, string scalar valuevar) {
    st_view(V=., ., (groupvar, valuevar))
    info = panelsetup(V[.,1], 1)     // Requires sorted data
    for (i=1; i<=rows(info); i++) {
        subset = panelsubmatrix(V[.,2], i, info)
        printf("Group %g: N=%g Mean=%9.2f\n",
               i, rows(subset), mean(subset))
    }
}
// Usage: sort foreign first, then call
```

### Bootstrap in Mata

```mata
void bootstrap_mean(string scalar varname, real scalar nreps) {
    real vector data, boot_means
    data = st_data(., varname)
    n = rows(data)
    boot_means = J(nreps, 1, .)
    for (i=1; i<=nreps; i++) {
        indices = ceil(runiform(n, 1) :* n)
        boot_means[i] = mean(data[indices])
    }
    _sort(boot_means, 1)
    st_numscalar("r(mean)", mean(data))
    st_numscalar("r(se)", sqrt(variance(boot_means)))
    st_numscalar("r(ci_lower)", boot_means[ceil(nreps*0.025)])
    st_numscalar("r(ci_upper)", boot_means[floor(nreps*0.975)])
}
```

### Passing Results Back to Stata

```mata
void comprehensive_analysis(string scalar yvar, string vector xvars) {
    y = st_data(., yvar)
    st_view(X=., ., xvars)
    R = correlation((y, X))

    st_matrix("r(R)", R)
    st_numscalar("r(N)", rows(X))
    st_global("r(depvar)", yvar)

    // Set matrix stripes
    allvars = yvar, xvars
    stripe = J(length(allvars), 2, "")
    stripe[., 2] = allvars'
    st_matrixrowstripe("r(R)", stripe)
    st_matrixcolstripe("r(R)", stripe)
}
```

---

## Performance Profiling

```mata
timer_clear(1)
timer_on(1)
// ... code ...
timer_off(1)
printf("Time: %9.4f seconds\n", timer_value(1)[1])
```
