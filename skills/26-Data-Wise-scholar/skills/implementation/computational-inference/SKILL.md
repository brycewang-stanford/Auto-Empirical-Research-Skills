---


name: computational-inference
description: Computational methods for statistical inference and optimization


---

# Computational Inference

**Advanced computational methods for statistical inference in complex models**

Use this skill when working on: MCMC algorithms, importance sampling, Bayesian inference, parallel computing for statistics, GPU acceleration, or computationally intensive inference procedures.

---

## Monte Carlo Methods

### Fundamental Principle

Monte Carlo methods approximate expectations via random sampling:

$$E[g(X)] \approx \frac{1}{N} \sum_{i=1}^{N} g(X_i), \quad X_i \sim P$$

**Monte Carlo Standard Error**:
$$\text{MCSE} = \frac{\hat{\sigma}}{\sqrt{N}}$$

### Variance Reduction Techniques

| Technique | Idea | Variance Reduction |
|-----------|------|-------------------|
| Antithetic variates | Use negatively correlated pairs | Up to 50% |
| Control variates | Subtract known expectation | Depends on correlation |
| Importance sampling | Sample from better distribution | Can be dramatic |
| Stratified sampling | Sample from strata separately | Reduces variance |

### R Implementation

```r
#' Monte Carlo Integration with Variance Reduction
#'
#' @param g Function to integrate
#' @param sampler Function that generates samples
#' @param n Number of samples
#' @param method Variance reduction method
#' @return Estimate with standard error
monte_carlo_integrate <- function(g, sampler, n = 10000,
                                   method = c("naive", "antithetic", "control")) {
  method <- match.arg(method)

  if (method == "naive") {
    samples <- sampler(n)
    values <- g(samples)
    estimate <- mean(values)
    se <- sd(values) / sqrt(n)

  } else if (method == "antithetic") {
    # Generate n/2 samples and their antithetic pairs
    u <- runif(n/2)
    samples1 <- qnorm(u)
    samples2 <- qnorm(1 - u)  # Antithetic

    values1 <- g(samples1)
    values2 <- g(samples2)
    paired_means <- (values1 + values2) / 2

    estimate <- mean(paired_means)
    se <- sd(paired_means) / sqrt(n/2)

  } else if (method == "control") {
    samples <- sampler(n)
    values <- g(samples)

    # Use sample mean as control (known E[X] = 0 for standard normal)
    control <- samples
    c_star <- -cov(values, control) / var(control)

    adjusted <- values + c_star * (control - 0)
    estimate <- mean(adjusted)
    se <- sd(adjusted) / sqrt(n)
  }

  list(
    estimate = estimate,
    se = se,
    ci = estimate + c(-1.96, 1.96) * se,
    n = n,
    method = method
  )
}
```

---

## Importance Sampling

### Theory

To estimate $E_P[g(X)]$ when sampling from $P$ is difficult, sample from proposal $Q$:

$$E_P[g(X)] = E_Q\left[g(X) \frac{p(X)}{q(X)}\right] = E_Q[g(X) w(X)]$$

where $w(X) = p(X)/q(X)$ are importance weights.

### Self-Normalized Importance Sampling

When normalizing constants are unknown:

$$\hat{\mu} = \frac{\sum_{i=1}^N w_i g(X_i)}{\sum_{i=1}^N w_i}$$

### Effective Sample Size

$$\text{ESS} = \frac{(\sum_i w_i)^2}{\sum_i w_i^2}$$

Rule of thumb: ESS > N/2 indicates reasonable proposal.

### R Implementation

```r
#' Importance Sampling Estimator
#'
#' @param g Function to evaluate
#' @param log_target Log of target density (unnormalized OK)
#' @param log_proposal Log of proposal density
#' @param proposal_sampler Function to sample from proposal
#' @param n Number of samples
#' @return Importance sampling estimate
importance_sampling <- function(g, log_target, log_proposal,
                                 proposal_sampler, n = 10000) {

  # Sample from proposal
  samples <- proposal_sampler(n)

  # Compute log importance weights
  log_weights <- log_target(samples) - log_proposal(samples)

  # Stabilize: subtract max for numerical stability
  log_weights <- log_weights - max(log_weights)
  weights <- exp(log_weights)

  # Normalize weights
  normalized_weights <- weights / sum(weights)

  # Compute estimate
  g_values <- g(samples)
  estimate <- sum(normalized_weights * g_values)

  # Effective sample size
  ess <- 1 / sum(normalized_weights^2)

  # Variance estimate (using delta method approximation)
  var_estimate <- sum(normalized_weights^2 * (g_values - estimate)^2)

  list(
    estimate = estimate,
    se = sqrt(var_estimate),
    ess = ess,
    ess_ratio = ess / n,
    max_weight = max(normalized_weights),
    weights = normalized_weights
  )
}
```

---

## MCMC Methods

### Metropolis-Hastings Algorithm

**Algorithm**:
1. Initialize $\theta^{(0)}$
2. For $t = 1, \ldots, T$:
   - Propose $\theta^* \sim q(\cdot | \theta^{(t-1)})$
   - Compute acceptance probability:
     $$\alpha = \min\left(1, \frac{p(\theta^*) q(\theta^{(t-1)} | \theta^*)}{p(\theta^{(t-1)}) q(\theta^* | \theta^{(t-1)})}\right)$$
   - Accept with probability $\alpha$

### Gibbs Sampling

For multivariate targets, sample each component from its full conditional:

$$\theta_j^{(t)} \sim p(\theta_j | \theta_{-j}^{(t-1)}, \text{data})$$

### MCMC Diagnostics

| Diagnostic | Purpose | Target |
|------------|---------|--------|
| Trace plots | Visual convergence check | Stationary appearance |
| $\hat{R}$ (Gelman-Rubin) | Between/within chain variance | < 1.01 |
| ESS | Effective independent samples | > 400 per parameter |
| Autocorrelation | Mixing assessment | Quick decay |

### R Implementation

```r
#' Metropolis-Hastings MCMC
#'
#' @param log_posterior Log posterior function
#' @param init Initial parameter values
#' @param proposal_sd Proposal standard deviation
#' @param n_iter Number of iterations
#' @param n_warmup Warmup iterations to discard
#' @return MCMC samples and diagnostics
metropolis_hastings <- function(log_posterior, init, proposal_sd,
                                 n_iter = 10000, n_warmup = 1000) {

  n_params <- length(init)
  samples <- matrix(NA, nrow = n_iter, ncol = n_params)
  samples[1, ] <- init
  accepted <- 0

  current_lp <- log_posterior(init)

  for (i in 2:n_iter) {
    # Propose
    proposal <- samples[i-1, ] + rnorm(n_params, 0, proposal_sd)

    # Compute acceptance probability
    proposed_lp <- log_posterior(proposal)
    log_alpha <- proposed_lp - current_lp

    # Accept/reject
    if (log(runif(1)) < log_alpha) {
      samples[i, ] <- proposal
      current_lp <- proposed_lp
      if (i > n_warmup) accepted <- accepted + 1
    } else {
      samples[i, ] <- samples[i-1, ]
    }
  }

  # Remove warmup
  samples <- samples[(n_warmup + 1):n_iter, ]

  # Compute ESS
  ess <- apply(samples, 2, function(x) {
    acf_vals <- acf(x, plot = FALSE, lag.max = 100)$acf
    n <- length(x)
    tau <- 1 + 2 * sum(acf_vals[-1])
    n / tau
  })

  list(
    samples = samples,
    acceptance_rate = accepted / (n_iter - n_warmup),
    ess = ess,
    summary = data.frame(
      mean = colMeans(samples),
      sd = apply(samples, 2, sd),
      q025 = apply(samples, 2, quantile, 0.025),
      q975 = apply(samples, 2, quantile, 0.975),
      ess = ess
    )
  )
}
```

---

## Hamiltonian Monte Carlo

### Theory

HMC uses Hamiltonian dynamics to propose distant moves with high acceptance:

$$H(\theta, p) = -\log p(\theta | y) + \frac{1}{2}p^T M^{-1} p$$

**Leapfrog integrator**:
1. $p \leftarrow p - \frac{\epsilon}{2} \nabla_\theta U(\theta)$
2. $\theta \leftarrow \theta + \epsilon M^{-1} p$
3. $p \leftarrow p - \frac{\epsilon}{2} \nabla_\theta U(\theta)$

### Key Parameters

| Parameter | Description | Tuning |
|-----------|-------------|--------|
| $\epsilon$ | Step size | Target ~65% acceptance |
| $L$ | Number of leapfrog steps | Balance ESS vs. computation |
| $M$ | Mass matrix | Approximate posterior covariance |

### Stan Integration

```r
#' Fit Bayesian Mediation Model with Stan
#'
#' @param data List with y, m, x, covariates
#' @return Stan fit object
fit_mediation_stan <- function(data) {
  stan_code <- "
  data {
    int<lower=0> N;
    vector[N] y;
    vector[N] m;
    vector[N] x;
  }
  parameters {
    real a;           // X -> M path
    real b;           // M -> Y path
    real c_prime;     // X -> Y direct
    real alpha_m;     // M intercept
    real alpha_y;     // Y intercept
    real<lower=0> sigma_m;
    real<lower=0> sigma_y;
  }
  model {
    // Priors
    a ~ normal(0, 1);
    b ~ normal(0, 1);
    c_prime ~ normal(0, 1);

    // Likelihoods
    m ~ normal(alpha_m + a * x, sigma_m);
    y ~ normal(alpha_y + b * m + c_prime * x, sigma_y);
  }
  generated quantities {
    real indirect = a * b;
    real total = a * b + c_prime;
  }
  "

  stan_fit <- rstan::stan(
    model_code = stan_code,
    data = data,
    chains = 4,
    iter = 2000,
    warmup = 1000,
    cores = parallel::detectCores()
  )

  stan_fit
}
```

---

## Parallel Computing

### Embarrassingly Parallel Tasks

Bootstrap, cross-validation, and simulation studies parallelize easily:

```r
#' Parallel Bootstrap for Mediation
#'
#' @param data Dataset
#' @param statistic Function computing indirect effect
#' @param R Number of bootstrap replicates
#' @return Bootstrap distribution
parallel_bootstrap <- function(data, statistic, R = 2000) {
  library(parallel)

  n <- nrow(data)
  n_cores <- detectCores() - 1

  # Create cluster
  cl <- makeCluster(n_cores)
  clusterExport(cl, c("data", "statistic", "n"), envir = environment())

  # Parallel bootstrap
  boot_results <- parSapply(cl, 1:R, function(i) {
    boot_idx <- sample(n, replace = TRUE)
    boot_data <- data[boot_idx, ]
    statistic(boot_data)
  })

  stopCluster(cl)

  list(
    estimate = statistic(data),
    boot_se = sd(boot_results),
    boot_ci = quantile(boot_results, c(0.025, 0.975)),
    boot_dist = boot_results
  )
}
```

### Future Package for Flexible Parallelism

```r
#' Parallel Simulation Study with future
#'
#' @param dgp Data generating process function
#' @param estimator Estimation function
#' @param n_sims Number of simulations
#' @param params Parameter grid
#' @return Simulation results
parallel_simulation <- function(dgp, estimator, n_sims = 1000, params) {
  library(future)
  library(future.apply)

  # Set up parallel backend
  plan(multisession, workers = parallel::detectCores() - 1)

  results <- future_lapply(1:n_sims, function(sim) {
    data <- dgp(params)
    est <- estimator(data)
    c(sim = sim, est)
  }, future.seed = TRUE)

  plan(sequential)  # Clean up

  do.call(rbind, results)
}
```

---

## GPU Acceleration

### When to Use GPU

| Task | CPU | GPU | Recommendation |
|------|-----|-----|----------------|
| Small matrices (<1000) | Fast | Overhead | CPU |
| Large matrices (>5000) | Slow | Fast | GPU |
| Element-wise operations | Moderate | Very fast | GPU if large |
| MCMC (sequential) | Fast | Overhead | CPU |
| Parallel MCMC chains | Moderate | Fast | GPU |

### R GPU Computing with torch

```r
#' GPU-Accelerated Matrix Operations
#'
#' @param X Design matrix
#' @param y Response vector
#' @return OLS coefficients computed on GPU
gpu_ols <- function(X, y) {
  library(torch)

  # Move to GPU
  X_gpu <- torch_tensor(X, device = "cuda")
  y_gpu <- torch_tensor(y, device = "cuda")

  # Solve normal equations on GPU
  XtX <- torch_mm(torch_t(X_gpu), X_gpu)
  Xty <- torch_mm(torch_t(X_gpu), y_gpu)

  # Solve system
  beta <- torch_linalg_solve(XtX, Xty)

  # Move back to CPU
  as.numeric(beta$cpu())
}
```

---

## Approximate Bayesian Computation

### ABC Rejection Algorithm

When likelihood is intractable but simulation is possible:

1. Sample $\theta^* \sim \pi(\theta)$ (prior)
2. Simulate $y^* \sim p(y | \theta^*)$
3. Accept if $d(S(y^*), S(y_{obs})) < \epsilon$

### ABC for Mediation

```r
#' ABC for Complex Mediation Model
#'
#' @param y_obs Observed outcome
#' @param m_obs Observed mediator
#' @param x_obs Observed treatment
#' @param prior_sampler Function to sample from prior
#' @param simulator Function to simulate data given parameters
#' @param summary_stats Function to compute summary statistics
#' @param epsilon Acceptance threshold
#' @param n_samples Target number of accepted samples
#' @return ABC posterior samples
abc_mediation <- function(y_obs, m_obs, x_obs,
                           prior_sampler, simulator, summary_stats,
                           epsilon = 0.1, n_samples = 1000) {

  obs_stats <- summary_stats(y_obs, m_obs, x_obs)
  accepted <- list()
  n_tried <- 0

  while (length(accepted) < n_samples) {
    # Sample from prior
    theta <- prior_sampler()

    # Simulate
    sim_data <- simulator(theta, length(y_obs))
    sim_stats <- summary_stats(sim_data$y, sim_data$m, x_obs)

    # Check acceptance
    distance <- sqrt(sum((sim_stats - obs_stats)^2))
    if (distance < epsilon) {
      accepted[[length(accepted) + 1]] <- theta
    }

    n_tried <- n_tried + 1
  }

  list(
    samples = do.call(rbind, accepted),
    acceptance_rate = n_samples / n_tried,
    epsilon = epsilon
  )
}
```

---

## Convergence Diagnostics

### Diagnostic Checklist

- [ ] Multiple chains started from dispersed initial values
- [ ] $\hat{R} < 1.01$ for all parameters
- [ ] ESS > 400 for all parameters
- [ ] Trace plots show stationarity
- [ ] No divergent transitions (HMC)
- [ ] Energy diagnostics pass (HMC)

### R Diagnostic Functions

```r
#' Comprehensive MCMC Diagnostics
#'
#' @param samples Matrix of MCMC samples (iterations x parameters)
#' @param n_chains Number of chains (samples split equally)
#' @return Diagnostic summary
mcmc_diagnostics <- function(samples, n_chains = 4) {

  n_iter <- nrow(samples) / n_chains
  n_params <- ncol(samples)

  # Split into chains
  chains <- lapply(1:n_chains, function(i) {
    idx <- ((i-1) * n_iter + 1):(i * n_iter)
    samples[idx, , drop = FALSE]
  })

  # R-hat (Gelman-Rubin)
  compute_rhat <- function(param_idx) {
    chain_means <- sapply(chains, function(c) mean(c[, param_idx]))
    chain_vars <- sapply(chains, function(c) var(c[, param_idx]))

    W <- mean(chain_vars)
    B <- var(chain_means) * n_iter

    var_hat <- (n_iter - 1) / n_iter * W + B / n_iter
    sqrt(var_hat / W)
  }

  rhat <- sapply(1:n_params, compute_rhat)

  # ESS
  compute_ess <- function(x) {
    n <- length(x)
    acf_vals <- acf(x, plot = FALSE, lag.max = min(n-1, 100))$acf
    tau <- 1 + 2 * sum(acf_vals[-1])
    max(1, n / tau)
  }

  ess <- apply(samples, 2, compute_ess)

  list(
    rhat = rhat,
    ess = ess,
    all_converged = all(rhat < 1.01) && all(ess > 400),
    summary = data.frame(
      parameter = 1:n_params,
      rhat = rhat,
      ess = ess,
      converged = rhat < 1.01 & ess > 400
    )
  )
}
```

---

## References

### Monte Carlo Methods

- Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods*
- Owen, A. B. (2013). *Monte Carlo theory, methods and examples*

### MCMC

- Brooks, S., et al. (2011). *Handbook of Markov Chain Monte Carlo*
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.)

### Computational Statistics

- Gentle, J. E. (2009). *Computational Statistics*
- Givens, G. H., & Hoeting, J. A. (2012). *Computational Statistics*

### Software

- Stan Development Team. *Stan User's Guide*
- R Core Team. *parallel* package documentation

---

**Version**: 1.0.0
**Created**: 2025-12-09
**Domain**: Computational methods for statistical inference
**Prerequisites**: Probability theory, Bayesian statistics, R programming
