---
name: r-oop
description: R object-oriented programming guide for S7, S3, S4, and vctrs. Use when designing R classes or choosing an OOP system.
---

# R Object-Oriented Programming

*S7, S3, S4, and vctrs: choosing the right OOP system for your needs*

## S7: Modern OOP for New Projects

- **S7 combines S3 simplicity with S4 structure**
- **Formal class definitions with automatic validation**
- **Compatible with existing S3 code**

```r
# S7 class definition
Range <- new_class("Range",
  properties = list(
    start = class_double,
    end = class_double
  ),
  validator = function(self) {
    if (self@end < self@start) {
      "@end must be >= @start"
    }
  }
)

# Usage - constructor and property access
x <- Range(start = 1, end = 10)
x@start  # 1
x@end <- 20  # automatic validation

# Methods
inside <- new_generic("inside", "x")
method(inside, Range) <- function(x, y) {
  y >= x@start & y <= x@end
}
```

## OOP System Decision Matrix

### S7 vs vctrs vs S3/S4 Decision Tree

**Start here:** What are you building?

### 1. Vector-like objects (things that behave like atomic vectors)

```
Use vctrs when:
- Need data frame integration (columns/rows)
- Want type-stable vector operations
- Building factor-like, date-like, or numeric-like classes
- Need consistent coercion/casting behavior
- Working with existing tidyverse infrastructure

Examples: custom date classes, units, categorical data
```

### 2. General objects (complex data structures, not vector-like)

```
Use S7 when:
- NEW projects that need formal classes
- Want property validation and safe property access (@)
- Need multiple dispatch (beyond S3's double dispatch)
- Converting from S3 and want better structure
- Building class hierarchies with inheritance
- Want better error messages and discoverability

Use S3 when:
- Simple classes with minimal structure needs
- Maximum compatibility and minimal dependencies
- Quick prototyping or internal classes
- Contributing to existing S3-based ecosystems
- Performance is absolutely critical (minimal overhead)

Use S4 when:
- Working in Bioconductor ecosystem
- Need complex multiple inheritance (S7 doesn't support this)
- Existing S4 codebase that works well
```

## Detailed S7 vs S3 Comparison

| Feature | S3 | S7 | When S7 wins |
|---------|----|----|---------------|
| **Class definition** | Informal (convention) | Formal (`new_class()`) | Need guaranteed structure |
| **Property access** | `$` or `attr()` (unsafe) | `@` (safe, validated) | Property validation matters |
| **Validation** | Manual, inconsistent | Built-in validators | Data integrity important |
| **Method discovery** | Hard to find methods | Clear method printing | Developer experience matters |
| **Multiple dispatch** | Limited (base generics) | Full multiple dispatch | Complex method dispatch needed |
| **Inheritance** | Informal, `NextMethod()` | Explicit `super()` | Predictable inheritance needed |
| **Migration cost** | - | Low (1-2 hours) | Want better structure |
| **Performance** | Fastest | ~Same as S3 | Performance difference negligible |
| **Compatibility** | Full S3 | Full S3 + S7 | Need both old and new patterns |

## Practical Guidelines

### Choose S7 when you have

```r
# Complex validation needs
Range <- new_class("Range",
  properties = list(start = class_double, end = class_double),
  validator = function(self) {
    if (self@end < self@start) "@end must be >= @start"
  }
)

# Multiple dispatch needs
method(generic, list(ClassA, ClassB)) <- function(x, y) ...

# Class hierarchies with clear inheritance
Child <- new_class("Child", parent = Parent)
```

### Choose vctrs when you need

```r
# Vector-like behavior in data frames
percent <- new_vctr(0.5, class = "percentage")
data.frame(x = 1:3, pct = percent(c(0.1, 0.2, 0.3)))  # works seamlessly

# Type-stable operations
vec_c(percent(0.1), percent(0.2))  # predictable behavior
vec_cast(0.5, percent())          # explicit, safe casting
```

### Choose S3 when you have

```r
# Simple classes without complex needs
new_simple <- function(x) structure(x, class = "simple")
print.simple <- function(x, ...) cat("Simple:", x)

# Maximum performance needs (rare)
# Existing S3 ecosystem contributions
```

## S3 Patterns

### Basic S3 Class

```r
# Constructor
new_person <- function(name, age) {
  stopifnot(is.character(name), length(name) == 1)
  stopifnot(is.numeric(age), length(age) == 1)

  structure(
    list(name = name, age = age),
    class = "person"
  )
}

# Print method
print.person <- function(x, ...) {
  cat("Person:", x$name, "(age", x$age, ")\n")
  invisible(x)
}

# Generic + method
greet <- function(x) UseMethod("greet")
greet.person <- function(x) {
  cat("Hello, my name is", x$name, "\n")
}
greet.default <- function(x) {
  cat("Hello!\n")
}
```

### S3 Inheritance

```r
# Child class
new_employee <- function(name, age, company) {
  obj <- new_person(name, age)
  obj$company <- company
  class(obj) <- c("employee", class(obj))
  obj
}

# Method with inheritance
print.employee <- function(x, ...) {
  NextMethod()  # Call parent print method
  cat("Works at:", x$company, "\n")
  invisible(x)
}
```

## S7 Patterns

### Basic S7 Class

```r
library(S7)

# Define class
Person <- new_class("Person",
  properties = list(
    name = class_character,
    age = class_numeric
  ),
  validator = function(self) {
    if (self@age < 0) {
      "@age must be non-negative"
    }
  }
)

# Create instance
bob <- Person(name = "Bob", age = 30)
bob@name  # "Bob"
bob@age <- 31  # Validated assignment
```

### S7 Methods

```r
# Define generic
greet <- new_generic("greet", "x")

# Add method
method(greet, Person) <- function(x) {
  cat("Hello, my name is", x@name, "\n")
}

# Default method
method(greet, class_any) <- function(x) {
  cat("Hello!\n")
}
```

### S7 Inheritance

```r
Employee <- new_class("Employee",
  parent = Person,
  properties = list(
    company = class_character
  )
)

# Override method
method(greet, Employee) <- function(x) {
  super(x, Person)@greet()  # Call parent method
  cat("I work at", x@company, "\n")
}
```

### S7 Multiple Dispatch

```r
# Generic with multiple dispatch
combine <- new_generic("combine", c("x", "y"))

# Method for specific combination
method(combine, list(Person, Person)) <- function(x, y) {
  cat(x@name, "meets", y@name, "\n")
}

method(combine, list(Person, class_character)) <- function(x, y) {
  cat(x@name, "receives message:", y, "\n")
}
```

## Migration Strategy

1. **S3 -> S7**: Usually 1-2 hours work, keeps full compatibility
2. **S4 -> S7**: More complex, evaluate if S4 features are actually needed
3. **Base R -> vctrs**: For vector-like classes, significant benefits
4. **Combining approaches**: S7 classes can use vctrs principles internally

### Migration Example: S3 to S7

```r
# Original S3
new_person_s3 <- function(name, age) {
  structure(list(name = name, age = age), class = "person")
}

# Migrated S7
Person <- new_class("Person",
  properties = list(
    name = class_character,
    age = class_numeric
  )
)

# S7 is backwards compatible with S3 generics
# Existing S3 methods still work
```

## When NOT to Use OOP

Sometimes simpler approaches are better:

```r
# Don't create a class for simple data
# BAD
Point <- new_class("Point", properties = list(x = class_double, y = class_double))

# GOOD - just use a named list or vector
point <- c(x = 1.5, y = 2.3)

# Don't create classes for one-off operations
# Use functions instead
distance <- function(p1, p2) {
  sqrt((p1["x"] - p2["x"])^2 + (p1["y"] - p2["y"])^2)
}
```
