# Mata Matrix Operations

## Matrix Creation

```mata
// Constants and special matrices
A = J(3, 4, 0)                 // 3x4 zeros
B = J(2, 2, 1)                 // 2x2 ones
I3 = I(3)                      // 3x3 identity
D = diag((1, 2, 3, 4))        // Diagonal matrix

// Direct input
v = (1, 2, 3, 4)              // Row vector
w = (1 \ 2 \ 3 \ 4)           // Column vector
M = (1, 2, 3 \ 4, 5, 6)      // Matrix (\ = new row)

// Sequences and random
x = range(1, 10, 1)            // 1 to 10 step 1
y = range(0, 1, 0.1)           // 0 to 1 step 0.1
U = runiform(3, 4)             // Uniform [0,1)
Z = rnormal(3, 4, 0, 1)       // Standard normal
rseed(12345)                    // Set seed

// Extract diagonal
d = diagonal(M)
```

---

## Matrix Arithmetic

```mata
C = A + B                       // Addition
D = A - B                       // Subtraction
E = A * B                       // Matrix multiplication
F = A :* B                      // Element-wise multiply
G = A :/ 2                      // Element-wise divide
H = A :^ 2                      // Element-wise power
K = 2 * A                       // Scalar multiply
L = A :+ 10                     // Scalar add

// Transpose
At = A'
// Complex conjugate transpose
Ct = conj(C')
```

---

## Matrix Functions

### Dimensions

```mata
rows(A); cols(A); length(v)
```

### Element-wise Functions

```mata
sqrt(A); exp(A); log(A); abs(A); floor(A); ceil(A)
```

### Summary Functions

**Warning:** These functions propagate missing values silently -- they do NOT
exclude missings. A single `.` in a column makes `mean()` return `.` for that
column. Filter first with `select(X, rowmissing(X) :== 0)`.
See mata-data-access.md > "Critical: Missing Values in Mata" for details.

```mata
sum(A)                          // All elements (. if any missing)
colsum(A); rowsum(A)            // (. propagates per column/row)
mean(A)                         // Column means (. if any missing in col)
variance(A)                     // Covariance matrix (. if any missing)
min(A); max(A)
colmin(A); colmax(A)
```

### Manipulation

```mata
C = A \ B                       // Vertical concatenation
D = A, B                        // Horizontal concatenation
F = rowshape(E, 3)             // Reshape to 3 rows
M = colshape(v, 2)             // Reshape to 2 columns
```

---

## Eigenvalues and Eigenvectors

### Symmetric Matrices

```mata
// Full decomposition
symeigensystem(A, eigenvectors=., eigenvalues=.)
// Eigenvalues only (faster)
evals = symeigenvalues(A)       // Ascending order

// Reconstruct: A = V * diag(L) * V'
A_reconstructed = V * diag(L) * V'
```

### General Matrices

```mata
eigensystem(A, eigenvectors=., eigenvalues=.)
evals = eigenvalues(A)          // May be complex
```

---

## Matrix Decompositions

### SVD

```mata
svd(A, U=., s=., V=.)          // A = U * diag(s) * V'
s = svdsv(A)                    // Singular values only (faster)

// Matrix rank
tol = 1e-10
rank = sum(s :> tol)

// Condition number
cond = s[1] / s[length(s)]
```

### Cholesky (symmetric positive definite)

```mata
L = cholesky(A)                 // A = L * L' (lower triangular)
```

### QR

```mata
qrd(A, Q=., R=.)               // A = Q * R
x = qrsolve(A, b)              // Least squares solution
```

### LU

```mata
lud(A, L=., U=., p=.)          // A[p,.] = L * U
x = lusolve(A, b)              // Solve A*x = b
A_inv = luinv(A)                // Inverse via LU
```

---

## Solving Linear Systems

### Direct Methods

```mata
// General: A*x = b
x = lusolve(A, b)

// Symmetric positive definite (faster)
x = cholsolve(A, b)

// Multiple right-hand sides
X = lusolve(A, B)              // A*X = B
```

### Least Squares (overdetermined)

```mata
x = qrsolve(A, b)              // Minimizes ||Ax - b||
resid = b - A * x
SSR = sum(resid:^2)
```

### Underdetermined (minimum norm)

```mata
A_pinv = pinv(A)
x = A_pinv * b                 // Minimum-norm solution
```

---

## Matrix Inversion

```mata
// Symmetric positive definite (fastest)
A_inv = invsym(A)

// General (LU-based)
A_inv = luinv(A)

// General
A_inv = inv(A)

// Pseudo-inverse (works for any matrix, including singular)
A_pinv = pinv(A)
// Properties: A * pinv(A) * A == A

// Determinant
d = det(A)
```

---

## Cross Products and Norms

### Cross Products

```mata
XtX = cross(X, X)              // X'X (faster than X'*X)
XtY = cross(X, Y)              // X'Y

// Deviations from mean
S = crossdev(X, X)             // (X-mean(X))'(X-mean(X))
Cov = S / (rows(X) - 1)

// Weighted: X'*diag(w)*X
XwX = quadcross(X, w, X)
```

### Norms

```mata
norm(v, 2)                      // Euclidean (2-norm)
norm(v, 1)                      // Manhattan (1-norm)
norm(v, .)                      // Infinity (max absolute)
norm(A)                         // Frobenius norm

// Normalized vector
v_unit = v / norm(v)

// Euclidean distance
dist = norm(x - y)
```

---

## Applications

### Principal Component Analysis

```mata
X_centered = X :- mean(X)
Cov = cross(X_centered, X_centered) / (rows(X) - 1)
symeigensystem(Cov, V=., L=.)
scores = X_centered * V         // PC scores
// L contains variance explained by each PC
```

### Matrix Exponential (symmetric)

```mata
symeigensystem(A, V=., L=.)
expA = V * diag(exp(L)) * V'
```

### Condition Number and Stability

```mata
s = svdsv(A)
cond = s[1] / s[length(s)]
if (cond > 1e10) {
    printf("Warning: ill-conditioned (cond=%g)\n", cond)
}
```

---

## Best Practices

### Choosing Decompositions

| Matrix Type | Best Method | Use Case |
|---|---|---|
| Symmetric positive definite | Cholesky | Covariance matrices, fastest |
| Tall/skinny, least squares | QR | Numerical stability |
| General square | LU | Multiple systems, determinants |
| Any, max stability | SVD | Pseudo-inverse, rank, PCA |

### Performance Tips

```mata
// Only compute what you need
s = svdsv(A)                    // Not full svd() if only values needed
evals = symeigenvalues(A)       // Not full eigensystem()

// Use symmetric functions for symmetric matrices
invsym(A)                       // Faster than inv()
symeigenvalues(A)               // Faster than eigenvalues()

// Force exact symmetry when constructing
B = (A + A') / 2

// Check condition before inverting
s = svdsv(A)
rank = sum(s :> 1e-10 * s[1])
```

## See Also

- [M-1] matrix -- Mata matrix functions reference
- [M-5] LAPACK -- Linear algebra routines
- [M-5] optimize() -- Optimization functions
