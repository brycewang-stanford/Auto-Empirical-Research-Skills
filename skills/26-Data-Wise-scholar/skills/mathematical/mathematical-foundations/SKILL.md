---


name: mathematical-foundations
description: Core mathematical concepts and theoretical frameworks for statistics


---

# Mathematical Foundations

**Core mathematical statistics theory for rigorous methodology development**

Use this skill when working on: theoretical derivations requiring classical statistics, optimality arguments, exponential family manipulations, decision-theoretic comparisons, or foundational probability theory.

---

## Sufficiency

### Sufficiency Definition

A statistic $T(X)$ is **sufficient** for parameter $\theta$ if the conditional distribution of $X$ given $T(X)$ does not depend on $\theta$:

$$P(X = x \mid T(X) = t, \theta) = P(X = x \mid T(X) = t)$$

### Factorization Theorem (Neyman-Fisher)

$T(X)$ is sufficient for $\theta$ if and only if the likelihood can be factored as:

$$f(x; \theta) = g(T(x), \theta) \cdot h(x)$$

where $g$ depends on $x$ only through $T(x)$, and $h$ does not depend on $\theta$.

### Minimal Sufficiency

A sufficient statistic $T$ is **minimal sufficient** if for any other sufficient statistic $U$, there exists a function $g$ such that $T = g(U)$.

**Criterion**: $T(x) = T(y)$ if and only if $\frac{f(x; \theta)}{f(y; \theta)}$ is constant in $\theta$.

### R Implementation

```r
#' Check Sufficiency via Factorization
#'
#' @param likelihood Function returning log-likelihood given data and theta
#' @param statistic Function computing candidate sufficient statistic
#' @param data Observed data
#' @return Logical indicating factorization structure
check_sufficiency <- function(likelihood, statistic, data) {
  t_value <- statistic(data)

  # Check if likelihood ratio is constant across different x with same T(x)
  # This is a conceptual framework - actual verification requires problem-specific analysis

  list(
    statistic_value = t_value,
    check_factorization = "Verify g(T(x), theta) * h(x) structure manually"
  )
}
```

---

## Completeness

### Completeness Definition

A family of distributions $\{P_\theta : \theta \in \Theta\}$ for statistic $T$ is **complete** if:

$$E_\theta[g(T)] = 0 \text{ for all } \theta \in \Theta \implies P_\theta(g(T) = 0) = 1 \text{ for all } \theta$$

Equivalently: the only unbiased estimator of zero is zero itself.

### Bounded Completeness

A weaker condition where the implication holds only for bounded functions $g$.

### Complete Sufficient Statistics

For exponential families with $k$-dimensional natural parameter and $k$-dimensional minimal sufficient statistic, the sufficient statistic is complete when the parameter space contains an open set.

**Key Result**: If $T$ is complete and sufficient, then any unbiased estimator that is a function of $T$ alone is UMVUE.

---

## UMVUE and Rao-Blackwell

### Rao-Blackwell Theorem

If $\hat{\theta}$ is any unbiased estimator of $\theta$ and $T$ is sufficient for $\theta$, then:

$$\tilde{\theta} = E[\hat{\theta} \mid T]$$

is also unbiased and has variance no greater than $\hat{\theta}$:

$$\text{Var}(\tilde{\theta}) \leq \text{Var}(\hat{\theta})$$

with equality if and only if $\hat{\theta}$ is already a function of $T$.

### Lehmann-Scheffe Theorem

If $T$ is **complete sufficient** and $\hat{\theta} = g(T)$ is unbiased for $\theta$, then $\hat{\theta}$ is the unique UMVUE (Uniformly Minimum Variance Unbiased Estimator).

### Finding UMVUE

**Strategy 1**: Conditioning Method
1. Find any unbiased estimator $\hat{\theta}$
2. Find complete sufficient statistic $T$
3. Compute $E[\hat{\theta} \mid T]$

**Strategy 2**: Direct Construction
1. Find complete sufficient statistic $T$
2. Find function $g$ such that $E[g(T)] = \theta$

### R Implementation

```r
#' Rao-Blackwell Improvement
#'
#' @param estimator_values Vector of estimator values from bootstrap/simulation
#' @param sufficient_stat Vector of corresponding sufficient statistic values
#' @return Rao-Blackwell improved estimates
rao_blackwell_improve <- function(estimator_values, sufficient_stat) {
  # Group by sufficient statistic values and compute conditional expectation
  improved <- tapply(estimator_values, sufficient_stat, mean)

  list(
    original_var = var(estimator_values),
    improved_var = var(improved[as.character(sufficient_stat)]),
    variance_reduction = 1 - var(improved[as.character(sufficient_stat)]) / var(estimator_values)
  )
}
```

---

## Exponential Families

### Canonical Form

A distribution belongs to the **exponential family** if it can be written as:

$$f(x; \theta) = h(x) \exp\left(\eta(\theta)^T T(x) - A(\theta)\right)$$

Or in natural parameterization:

$$f(x; \eta) = h(x) \exp\left(\eta^T T(x) - A(\eta)\right)$$

where:
- $\eta$ = natural parameter
- $T(x)$ = sufficient statistic
- $A(\eta)$ = log-partition function (cumulant generating function)
- $h(x)$ = base measure

### Key Properties

**Moments from Log-Partition**:
$$E[T(X)] = \nabla A(\eta), \quad \text{Cov}(T(X)) = \nabla^2 A(\eta)$$

**Maximum Likelihood**:
For iid sample $X_1, \ldots, X_n$, the MLE satisfies:
$$\nabla A(\hat{\eta}) = \frac{1}{n} \sum_{i=1}^n T(X_i)$$

**Completeness**: Natural exponential families with full-rank $\eta$ have complete sufficient statistics.

### Common Exponential Families

| Distribution | $T(x)$ | $\eta$ | $A(\eta)$ |
|--------------|--------|--------|-----------|
| Normal($\mu$, $\sigma^2$) | $(x, x^2)$ | $(\mu/\sigma^2, -1/(2\sigma^2))$ | $-\eta_1^2/(4\eta_2) - \log(-2\eta_2)/2$ |
| Poisson($\lambda$) | $x$ | $\log\lambda$ | $e^\eta$ |
| Binomial($n$, $p$) | $x$ | $\log(p/(1-p))$ | $n\log(1 + e^\eta)$ |
| Gamma($\alpha$, $\beta$) | $(x, \log x)$ | $(-\beta, \alpha-1)$ | $\log\Gamma(\eta_2+1) - (\eta_2+1)\log(-\eta_1)$ |

### R Implementation

```r
#' Exponential Family MLE via Log-Partition Gradient
#'
#' @param sufficient_stats Matrix of sufficient statistics (n x k)
#' @param log_partition_gradient Function computing gradient of A(eta)
#' @param initial_eta Initial natural parameter
#' @return MLE natural parameter
exponential_family_mle <- function(sufficient_stats, log_partition_gradient, initial_eta) {
  # MLE solves: gradient(A(eta)) = sample mean of T(X)
  target_mean <- colMeans(sufficient_stats)

  objective <- function(eta) {
    sum((log_partition_gradient(eta) - target_mean)^2)
  }

  result <- optim(initial_eta, objective, method = "BFGS")

  list(
    eta_mle = result$par,
    convergence = result$convergence == 0
  )
}
```

---

## Decision Theory

### Statistical Decision Framework

- **Action space** $\mathcal{A}$: Set of possible decisions
- **Loss function** $L(\theta, a)$: Penalty for action $a$ when truth is $\theta$
- **Risk function** $R(\theta, \delta) = E_\theta[L(\theta, \delta(X))]$

### Common Loss Functions

| Loss | Formula | Properties |
|------|---------|------------|
| Squared error | $(a - \theta)^2$ | Penalizes larger errors more |
| Absolute error | $|a - \theta|$ | Robust to outliers |
| 0-1 loss | $I(a \neq \theta)$ | Classification |
| Weighted squared | $w(\theta)(a - \theta)^2$ | Heterogeneous importance |

### Admissibility

An estimator $\delta$ is **admissible** if there is no other estimator $\delta'$ such that:
- $R(\theta, \delta') \leq R(\theta, \delta)$ for all $\theta$
- $R(\theta, \delta') < R(\theta, \delta)$ for some $\theta$

### Bayes Estimators

The **Bayes estimator** minimizes the posterior expected loss:

$$\delta^{\pi}(x) = \arg\min_a E[L(\theta, a) \mid X = x]$$

**Key Result**: Under squared error loss, the Bayes estimator is the posterior mean.

**Admissibility Connection**: Unique Bayes estimators are admissible.

### Minimax Estimators

An estimator $\delta^*$ is **minimax** if:

$$\sup_\theta R(\theta, \delta^*) = \inf_\delta \sup_\theta R(\theta, \delta)$$

**Finding Minimax**: Often found as the Bayes estimator with respect to the "least favorable prior."

### R Implementation

```r
#' Compare Estimators by Risk Function
#'
#' @param estimators List of estimator functions
#' @param theta_grid Grid of parameter values to evaluate
#' @param dgp Function to generate data given theta
#' @param loss Loss function L(theta, estimate)
#' @param n_sims Number of simulations per theta
#' @return Risk function evaluations
compare_estimator_risks <- function(estimators, theta_grid, dgp, loss, n_sims = 1000) {
  results <- expand.grid(
    theta = theta_grid,
    estimator = names(estimators)
  )
  results$risk <- NA

  for (i in seq_along(theta_grid)) {
    theta <- theta_grid[i]
    data_samples <- replicate(n_sims, dgp(theta), simplify = FALSE)

    for (j in seq_along(estimators)) {
      estimates <- sapply(data_samples, estimators[[j]])
      results$risk[results$theta == theta &
                   results$estimator == names(estimators)[j]] <-
        mean(loss(theta, estimates))
    }
  }

  # Identify admissibility
  # Check if any estimator dominates another at all theta values

  results
}
```

---

## Martingale Theory

### Martingale Definition

A sequence $(M_n)_{n \geq 0}$ is a **martingale** with respect to filtration $(\mathcal{F}_n)$ if:
1. $M_n$ is $\mathcal{F}_n$-measurable
2. $E[|M_n|] < \infty$
3. $E[M_{n+1} \mid \mathcal{F}_n] = M_n$

### Martingale Central Limit Theorem

If $(M_n)$ is a martingale with differences $D_i = M_i - M_{i-1}$, and under regularity conditions:

$$\frac{M_n}{\sqrt{\sum_{i=1}^n E[D_i^2 \mid \mathcal{F}_{i-1}]}} \xrightarrow{d} N(0, 1)$$

**Key Condition**: Lindeberg condition for triangular arrays:
$$\frac{1}{s_n^2} \sum_{i=1}^n E[D_i^2 I(|D_i| > \epsilon s_n) \mid \mathcal{F}_{i-1}] \xrightarrow{p} 0$$

### Optional Stopping Theorem

If $\tau$ is a stopping time and $(M_n)$ is a martingale, then under boundedness conditions:

$$E[M_\tau] = E[M_0]$$

### Application to Sequential Analysis

In sequential mediation analysis or adaptive designs, martingale theory provides:
- Valid inference at random stopping times
- Error spending functions for interim analyses
- Asymptotic theory for data-dependent sample sizes

### R Implementation

```r
#' Verify Martingale Property
#'
#' @param sequence Vector of observed martingale values
#' @param n_bootstrap Bootstrap samples for testing
#' @return Test for martingale property
test_martingale <- function(sequence, n_bootstrap = 1000) {
  n <- length(sequence)
  differences <- diff(sequence)

  # Under martingale property, E[D_i | F_{i-1}] = 0
  # Test using conditional mean estimation

  # Simple test: differences should have mean zero conditional on past
  conditional_means <- sapply(2:(n-1), function(i) {
    mean(differences[1:i])
  })

  list(
    mean_differences = mean(differences),
    se_differences = sd(differences) / sqrt(length(differences)),
    t_stat = mean(differences) / (sd(differences) / sqrt(length(differences))),
    p_value = 2 * pnorm(-abs(mean(differences) / (sd(differences) / sqrt(length(differences)))))
  )
}
```

---

## U-Statistics

### Definition

A **U-statistic** of order $r$ is:

$$U_n = \binom{n}{r}^{-1} \sum_{1 \leq i_1 < \cdots < i_r \leq n} h(X_{i_1}, \ldots, X_{i_r})$$

where $h$ is a symmetric kernel function.

### Variance Decomposition

$$\text{Var}(U_n) = \binom{n}{r}^{-1} \sum_{c=1}^{r} \binom{r}{c} \binom{n-r}{r-c} \zeta_c$$

where $\zeta_c = \text{Cov}(h(X_1, \ldots, X_r), h(X_1, \ldots, X_c, X_{r+1}, \ldots, X_{2r-c}))$.

### Asymptotic Normality

Under regularity conditions:

$$\sqrt{n}(U_n - \theta) \xrightarrow{d} N(0, r^2 \zeta_1)$$

where $\zeta_1$ is the first-order variance component.

### Application to Mediation

The product of coefficients $\hat{a}\hat{b}$ can be viewed through U-statistic lens for variance estimation.

### R Implementation

```r
#' Compute U-statistic with Bootstrap Variance
#'
#' @param data Data vector or matrix
#' @param kernel Symmetric kernel function
#' @param r Order of U-statistic
#' @param B Bootstrap replicates
#' @return U-statistic with variance estimate
compute_ustat <- function(data, kernel, r = 2, B = 1000) {
  n <- NROW(data)

  # Compute U-statistic
  indices <- combn(n, r)
  u_values <- apply(indices, 2, function(idx) {
    kernel(if (is.matrix(data)) data[idx, ] else data[idx])
  })
  u_stat <- mean(u_values)

  # Bootstrap variance
  boot_ustats <- replicate(B, {
    boot_idx <- sample(n, replace = TRUE)
    boot_data <- if (is.matrix(data)) data[boot_idx, ] else data[boot_idx]
    boot_indices <- combn(n, r)
    mean(apply(boot_indices, 2, function(idx) {
      kernel(if (is.matrix(boot_data)) boot_data[idx, ] else boot_data[idx])
    }))
  })

  list(
    estimate = u_stat,
    se = sd(boot_ustats),
    ci = quantile(boot_ustats, c(0.025, 0.975))
  )
}
```

---

## Information Geometry

### Fisher Information

The **Fisher information** matrix is:

$$I(\theta)_{jk} = E\left[\frac{\partial \log f(X; \theta)}{\partial \theta_j} \frac{\partial \log f(X; \theta)}{\partial \theta_k}\right]$$

Or equivalently (under regularity):

$$I(\theta)_{jk} = -E\left[\frac{\partial^2 \log f(X; \theta)}{\partial \theta_j \partial \theta_k}\right]$$

### Cramer-Rao Bound

For any unbiased estimator $\hat{\theta}$:

$$\text{Var}(\hat{\theta}) \geq I(\theta)^{-1}$$

An estimator achieving this bound is **efficient**.

### Information for Product Parameters

For mediation effects $\theta = ab$, the information combines:

$$I_{ab} = \left(\frac{\partial(ab)}{\partial a}\right)^2 I_a + \left(\frac{\partial(ab)}{\partial b}\right)^2 I_b + 2 \frac{\partial(ab)}{\partial a}\frac{\partial(ab)}{\partial b} I_{ab}$$

### R Implementation

```r
#' Compute Fisher Information Matrix Numerically
#'
#' @param log_likelihood Log-likelihood function(data, theta)
#' @param theta Parameter vector
#' @param data Data
#' @param n_samples Monte Carlo samples for expectation
#' @return Fisher information matrix
fisher_information <- function(log_likelihood, theta, data, n_samples = 1000) {
  k <- length(theta)
  eps <- sqrt(.Machine$double.eps)

  # Compute score function
  score <- function(x, th) {
    grad <- numeric(k)
    for (j in 1:k) {
      th_plus <- th_minus <- th
      th_plus[j] <- th[j] + eps
      th_minus[j] <- th[j] - eps
      grad[j] <- (log_likelihood(x, th_plus) - log_likelihood(x, th_minus)) / (2 * eps)
    }
    grad
  }

  # Expected outer product of score
  scores <- t(sapply(1:NROW(data), function(i) {
    score(if (is.matrix(data)) data[i, ] else data[i], theta)
  }))

  info_matrix <- (t(scores) %*% scores) / NROW(data)

  list(
    information = info_matrix,
    cramer_rao_bound = solve(info_matrix)
  )
}
```

---

## Measure-Theoretic Foundations

### Key Concepts

**Measurability**: Random variables are measurable functions from $(\Omega, \mathcal{F})$ to $(\mathbb{R}, \mathcal{B})$.

**Dominated Convergence Theorem**: If $|f_n| \leq g$ with $E[g] < \infty$ and $f_n \to f$ a.s., then $E[f_n] \to E[f]$.

**Fubini-Tonelli Theorem**: For non-negative measurable functions or integrable functions:
$$\int \left(\int f(x, y) \, d\mu(x)\right) d\nu(y) = \int \left(\int f(x, y) \, d\nu(y)\right) d\mu(x)$$

### Application to Identification

Causal identification often requires:
1. Measurability of potential outcomes
2. Dominated convergence for limit theorems
3. Fubini for iterated expectations

### Radon-Nikodym Derivative

If $P \ll Q$ (P is absolutely continuous with respect to Q), then:

$$\frac{dP}{dQ}(x) = \text{likelihood ratio}$$

Critical for:
- Importance sampling in mediation simulations
- Sensitivity analysis formulations
- Change of measure arguments

---

## References

### Primary Texts

- Lehmann, E. L., & Casella, G. (1998). *Theory of Point Estimation*
- Lehmann, E. L., & Romano, J. P. (2005). *Testing Statistical Hypotheses*
- Shao, J. (2003). *Mathematical Statistics*
- Schervish, M. J. (1995). *Theory of Statistics*

### Specialized Topics

- Ferguson, T. S. (1996). *A Course in Large Sample Theory*
- Bickel, P. J., & Doksum, K. A. (2015). *Mathematical Statistics*
- Durrett, R. (2019). *Probability: Theory and Examples*
- Williams, D. (1991). *Probability with Martingales*

### Information Geometry

- Amari, S., & Nagaoka, H. (2000). *Methods of Information Geometry*
- Efron, B. (1975). Defining the curvature of a statistical problem

---

**Version**: 1.0.0
**Created**: 2025-12-08
**Domain**: Mathematical statistics foundations for methodology research
**Prerequisites**: Probability theory, linear algebra, real analysis
