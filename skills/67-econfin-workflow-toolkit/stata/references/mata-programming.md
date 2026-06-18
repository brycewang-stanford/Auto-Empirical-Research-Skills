# Mata Programming

## Functions

### Defining Functions

```mata
function real scalar add_numbers(real scalar a, real scalar b) {
    return(a + b)
}

function real matrix matrix_multiply(real matrix A, real matrix B) {
    if (cols(A) != rows(B)) _error(3200)  // conformability error
    return(A * B)
}

function void display_message(string scalar msg) {
    printf("Message: %s\n", msg)
}
```

### Type Declarations

- `real scalar`, `real vector`, `real matrix`, `real rowvector`, `real colvector`
- `string scalar`, `string matrix`
- `pointer`, `transmorphic` (any type, default if unspecified)

### Statistical Function Example

```mata
function real scalar compute_mean(real colvector x) {
    if (rows(x) == 0) return(.)
    return(sum(x) / rows(x))
}

function real scalar compute_variance(real colvector x) {
    real scalar n, m
    n = rows(x)
    if (n <= 1) return(.)
    m = compute_mean(x)
    return(sum((x :- m):^2) / (n - 1))
}
```

---

## Flow Control

### If Statements

```mata
if (condition) { ... }
else if (condition2) { ... }
else { ... }
```

**Gotcha:** Conditions must evaluate to a single scalar. For matrices use `all()` or `any()`:

```mata
if (all(x :> 0)) printf("All positive\n")
if (any(x :== 0)) printf("At least one zero\n")
```

### For Loops

```mata
for (i = 1; i <= 10; i++) {
    printf("%f\n", i)
}

// Prefer vectorized operations over element loops:
// Slow:  for (i...) result[i,j] = X[i,j] * factor
// Fast:  result = X :* factor
```

### While and Do-While

```mata
while (condition) { ... }

do {
    ...
} while (condition)      // Guarantees at least one execution
```

### Loop Control

- `break` -- exit loop immediately
- `continue` -- skip to next iteration

---

## Pointers

```mata
x = 10
p = &x          // Address-of
*p              // Dereference: 10
*p = 20         // Modify through pointer

// Pointer to matrix
X = (1, 2 \ 3, 4)
p = &X
(*p)[2,2]       // Access element: 4

// Function pointers
fp = &square()
(*fp)(5)         // 25

// Practical: generic function application
function real scalar apply_op(real scalar x, real scalar y,
                              pointer(function) scalar op) {
    return((*op)(x, y))
}
result = apply_op(5, 3, &add())
```

### Pointer Matrices

```mata
ptrs = J(3, 3, NULL)
a = 1
ptrs[1,1] = &a
*ptrs[1,1]      // 1
```

---

## Structures

```mata
struct point {
    real scalar x
    real scalar y
}

struct point scalar p
p.x = 5.0
p.y = 3.0

// Functions with structures
struct point scalar create_point(real scalar x, real scalar y) {
    struct point scalar p
    p.x = x; p.y = y
    return(p)
}

function real scalar distance(struct point scalar p1, struct point scalar p2) {
    return(sqrt((p2.x - p1.x)^2 + (p2.y - p1.y)^2))
}

// Nested structures
struct rectangle {
    struct point scalar top_left
    struct point scalar bottom_right
}
```

---

## Classes

### Basic Class

```mata
class BankAccount {
    protected:
        real scalar balance
        string scalar owner
    public:
        void new()
        void deposit()
        void withdraw()
        real scalar get_balance()
        void set_owner()
}

void BankAccount::new() { balance = 0; owner = "" }
void BankAccount::deposit(real scalar amount) {
    if (amount > 0) balance = balance + amount
}
void BankAccount::withdraw(real scalar amount) {
    if (amount > 0 & amount <= balance) balance = balance - amount
}
real scalar BankAccount::get_balance() { return(balance) }
void BankAccount::set_owner(string scalar name) { owner = name }

// Usage
account = BankAccount()
account.deposit(1000)
account.get_balance()   // 1000
```

### Inheritance

```mata
class SavingsAccount extends BankAccount {
    protected:
        real scalar interest_rate
    public:
        void new()
        void apply_interest()
}
void SavingsAccount::new() {
    super.new()
    interest_rate = 0.03
}
void SavingsAccount::apply_interest() {
    balance = balance * (1 + interest_rate)
}
```

### Access Modifiers

- `public` -- accessible from anywhere
- `protected` -- accessible within class and derived classes
- `private` -- accessible only within the class
- `static` -- shared across all instances

---

## Mata Libraries

### Creating and Using

```stata
// Define functions, then:
mata mlib create lmylib, replace
mata mlib add lmylib mysum() mymean()
mata mlib index                     // Required after adding

// Functions are then auto-available
mata: mysum((1,2,3))
```

### Management

```stata
mata mlib create libname [, replace size(#)]
mata mlib add libname function() [...]
mata mlib index
mata describe using lmylib.mlib     // View contents
mata which functionname()           // Find where function lives

// Individual object code
mata mosave functionname, replace
```

---

## st_ Interface Functions

### Reading Data

```mata
// Copy data (independent matrix)
X = st_data(., ("mpg", "weight", "price"))
X = st_data((1::10), ("mpg", "weight"))
X = st_data(., "mpg", "foreign==1")     // With selection

// View (no copy, changes affect Stata data)
st_view(X, ., ("mpg", "weight", "price"))
X[1,1] = 999                            // Modifies Stata data!

// String data
S = st_sdata(., "make")
```

**st_data() vs st_view():** `st_data()` copies (safe, more memory). `st_view()` references (fast, memory-efficient, changes propagate).

### Writing Data

```mata
st_store(., "varname", Y)               // Store to existing var
idx = st_addvar("double", "predicted")  // Create new var
st_store(., idx, Y)
st_addvar("float", ("var1", "var2"))    // Multiple vars
```

### Variables, Macros, Scalars, Matrices

```mata
// Variable info
st_varindex("mpg")
st_varname(1)
st_nvar()
st_nobs()

// Macros
varlist = st_local("varlist")
st_local("result", "success")
path = st_global("S_ADO")

// Scalars
n = st_numscalar("r(N)")
st_numscalar("r(mean)", mean_value)

// Matrices
M = st_matrix("e(V)")
st_matrix("mymatrix", M)
st_replacematrix("e(V)", V)
```

---

## Optimization

### Efficient Coding

```mata
// Use explicit types (fast) not transmorphic (slow)
function real scalar sum2(real colvector x) { return(sum(x)) }

// Use views for large data
st_view(X, ., vars)

// Vectorize (fast), don't loop (slow)
Y = X :* 2              // not: for (i...) Y[i] = X[i]*2

// Preallocate
X = J(1000, 1, .)       // not: X = X \ i^2 in loop

// Use built-in functions
result = sum(x)          // not: manual loop

// Use appropriate solvers
b = cholsolve(X'X, X'y)  // For positive definite (faster)
// instead of: b = invsym(X'X) * X'y
```

### Mata Optimizer

```mata
// Define objective function
void myeval(todo, p, y, g, H) {
    y = -(p[1]^2 + p[2]^2)     // Negative for maximization
    if (todo >= 1) {
        g = J(1, 2, .)
        g[1] = -2*p[1]
        g[2] = -2*p[2]
    }
}

S = optimize_init()
optimize_init_evaluator(S, &myeval())
optimize_init_evaluatortype(S, "d1")    // d0, d1, d2, v0
optimize_init_params(S, (0, 0))
p = optimize(S)

optimize_result_value(S)
optimize_result_iterations(S)
```

**Evaluator types:** `d0` (numeric derivatives), `d1` (gradient provided), `d2` (gradient + Hessian), `v0` (vector of values for least squares).

**Algorithms:** `optimize_init_technique(S, "nr")` (Newton-Raphson), `"dfp"`, `"bfgs"`, `"nm"` (Nelder-Mead, derivative-free).

### Complete MLE Example

```mata
void normal_ll(todo, theta, y, lnf, g, H) {
    real scalar mu, sigma2, n
    mu = theta[1]; sigma2 = theta[2]; n = rows(y)
    resid = y :- mu
    lnf = -n/2*log(2*pi()) - n/2*log(sigma2) - sum(resid:^2)/(2*sigma2)
    if (todo >= 1) {
        g = J(1, 2, .)
        g[1] = sum(resid) / sigma2
        g[2] = -n/(2*sigma2) + sum(resid:^2)/(2*sigma2^2)
    }
}

function real rowvector estimate_normal(string scalar varname) {
    y = st_data(., varname)
    S = optimize_init()
    optimize_init_evaluator(S, &normal_ll())
    optimize_init_evaluatortype(S, "d1")
    optimize_init_params(S, (mean(y), variance(y)))
    optimize_init_argument(S, 1, y)
    optimize_init_which(S, "max")
    return(optimize(S))
}
```

---

## Compiling and Managing

```stata
mata describe                   // List all compiled functions
mata describe myfunc            // Describe specific
mata drop myfunc()              // Remove function
mata clear                      // Remove all
```

## Sources

- [Stata Mata documentation](https://www.stata.com/mata/)
- [SSCC Wisconsin: Introduction to Mata](https://sscc.wisc.edu/sscc/pubs/4-26.htm)
- [Stata Blog: Mata 101](https://blog.stata.com/2015/12/15/programming-an-estimation-command-in-stata-mata-101/)
