# Mata Introduction

## What is Mata?

Mata is Stata's compiled matrix programming language. Key characteristics:

| Aspect | Stata | Mata |
|--------|-------|------|
| Execution | Interpreted line-by-line | Compiled to bytecode |
| Speed | Good for data operations | 10-1000x faster for computations |
| Data model | Observations and variables | Matrices and scalars |
| Syntax | Command-based | C-style |
| Primary use | Data management, statistics | Matrix operations, algorithms |

**Use Mata when:** loops are slow, matrix operations needed, custom estimators, simulations.
**Use Stata when:** data management, standard statistical procedures, interactive exploration.

---

## Mata Environment and Syntax

### Starting and Exiting

```stata
mata                    // Enter interactive mode
// ... Mata code ...
end                     // Return to Stata

mata: x = I(5)          // Single-line execution
```

### Syntax Basics

```mata
// Assignment
x = 5
name = "Hello"
matrix = (1, 2, 3 \ 4, 5, 6)

// Comments: // or /* ... */
// Semicolons optional (separate statements on one line)
// Case-sensitive: x and X are different

// Display
x                       // Type name to display
printf("Value: %f\n", x)
```

---

## Data Types

### Numeric

```mata
x = 3.14159             // Real scalar
z = .                   // Missing value
c = 3 + 4i             // Complex
magnitude = abs(c)
real_part = Re(c)
```

### String

```mata
name = "Stata"
upper = strupper(name)
length = strlen(name)
substr = substr(name, 1, 3)
concat = name + " 18"
```

### Pointer

```mata
x = 10
p = &x                 // Address-of
*p                      // Dereference: returns 10
*p = 20                 // Modify through pointer

// Function pointer
fp = &square()
(*fp)(5)                // Call function via pointer
```

### Structure

```mata
struct person {
    string scalar name
    real scalar age
    real scalar income
}

struct person scalar p
p.name = "Alice"
p.age = 30
```

### transmorphic (any type)

```mata
transmorphic x
x = 5                   // Now real
x = "hello"             // Now string
x = (1, 2, 3)           // Now matrix
```

---

## Scalars, Vectors, and Matrices

```mata
// Row vector
row_vec = (1, 2, 3, 4, 5)

// Column vector
col_vec = (1 \ 2 \ 3 \ 4 \ 5)

// Special constructors
zeros_vec = J(1, 5, 0)         // 1x5 zeros
ones_vec = J(5, 1, 1)          // 5x1 ones
range_vec = 1::10              // Column 1 to 10

// Matrix (\ separates rows, , separates columns)
A = (1, 2, 3 \ 4, 5, 6 \ 7, 8, 9)

// Special matrices
I3 = I(3)                      // Identity
zeros = J(3, 4, 0)
d = diag((1, 2, 3, 4))        // Diagonal

// Dimensions and access
rows(A)                         // 3
cols(A)                         // 3
A[2, 3]                         // Element (6)
A[2, .]                         // Row 2
A[., 3]                         // Column 3
A[1..2, 2..3]                  // Submatrix

// Random matrices
rnorm = rnormal(5, 3, 0, 1)
runif = runiform(4, 4)

// Concatenation
horiz = (A, B)                 // Horizontal
vert = (A \ B)                 // Vertical

// Type checks
isscalar(x)
isvector(v)
isrowvector(v)
issymmetric(A)
```

---

## Operators

### Arithmetic

```mata
// Matrix operations
C = A + B               // Addition
D = A - B               // Subtraction
E = A * B               // Matrix multiplication
F = A :* B              // Element-wise multiplication
G = A :/ B              // Element-wise division
H = A :^ 2              // Element-wise power
K = A * 5               // Scalar multiply
L = A :+ 10             // Scalar add to all elements
```

### Comparison (element-wise on matrices)

```mata
A :== B                  // (0, 1 \ 1, 0) etc.
A :< B
A :>= B
```

### Logical

```mata
a & b                    // AND
a | b                    // OR
!a                       // NOT
A :& B                   // Element-wise AND
```

### Matrix-Specific

```mata
A'                       // Transpose
invsym(A'A)              // Symmetric inverse
luinv(B)                 // LU inverse
cross(A, A)              // A'A (faster than A'*A)
A # B                    // Kronecker product
```

### Math Functions (apply element-wise to matrices)

```mata
ln(x); log10(x); exp(x); sqrt(x); abs(x)
floor(x); ceil(x); round(x, 0.1)
sin(x); cos(x); tan(x)
```

---

## Calling Mata from Stata

### Management Commands

```stata
mata describe                   // List all Mata objects
mata clear                      // Clear Mata memory
mata: mata drop A B C           // Drop specific objects
mata matsave results A B, replace
mata matuse results
```

### From Do-files

```stata
mata
    price = st_data(., "price")
    mean_price = mean(price)
    st_numscalar("r(mean_price)", mean_price)
end
display "Mean price: " r(mean_price)
```

### External .mata Files

```stata
do mycode.mata
// or
mata: source mycode.mata
```

---

## Interactive vs Compiled Mata

### Interactive: for exploration

```mata
mata
    x = 1::10
    y = x:^2
    mean(y)
end
```

### Compiled Functions: for reuse and performance

```mata
mata
    function real scalar mymean(real colvector x) {
        return(sum(x) / rows(x))
    }
end
```

### Saving Compiled Functions

```stata
// .mo files (single function)
mata: mata mosave mymean(), replace

// .mlib files (library of functions)
mata mlib create lmylib, replace
mata mlib add lmylib func1() func2() func3()
mata mlib index                 // Rebuild index
```

---

## Stata Data Interface (st_* functions)

```mata
// Read data
vardata = st_data(., "varname")
all_data = st_data(., .)

// Write data
st_store(., "newvar", result)
idx = st_addvar("double", "newvar")
st_store(., idx, result)

// Macros
value = st_global("mymacro")
st_global("result_macro", strofreal(result))

// Scalars
n = st_numscalar("r(N)")
st_numscalar("r(mean_mata)", result)
```

---

## Practical Tips

1. **Start simple** with interactive Mata
2. **Convert bottlenecks** from Stata loops to Mata
3. **Use built-in functions** (mean, variance, correlation, optimize)
4. **Use explicit types** for safety and performance: `real colvector x` instead of `transmorphic`
5. **Use st_view() instead of st_data()** for large datasets (no copy)
6. **Minimize Stata-Mata transitions** -- batch operations in single Mata blocks
7. **Don't call Stata commands from Mata loops** -- defeats the speed purpose

**Next:** See mata-programming.md for functions/control flow, mata-matrix-operations.md for linear algebra, mata-data-access.md for the st_* interface.
