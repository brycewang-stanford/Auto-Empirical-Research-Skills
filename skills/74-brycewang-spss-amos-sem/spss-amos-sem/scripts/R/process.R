# PROCESS (Hayes) models 1, 4, 6, 7, 8, 14 on construct mean scores, the way
# the SPSS macro computes them: OLS equations, percentile bootstrap CIs,
# products built from mean-centred components (PROCESS `center=1`), and
# continuous moderators probed at the 16th / 50th / 84th percentiles.

ols <- function(y, X) {
  fit <- stats::lm.fit(X, y)
  b <- fit$coefficients
  n <- length(y); k <- ncol(X)
  res <- fit$residuals
  s2 <- sum(res^2) / (n - k)
  XtXi <- chol2inv(qr.R(fit$qr))[order(fit$qr$pivot), order(fit$qr$pivot)]
  V <- s2 * XtXi
  dimnames(V) <- list(colnames(X), colnames(X))
  r2 <- 1 - sum(res^2) / sum((y - mean(y))^2)
  list(b = setNames(b, colnames(X)), V = V, n = n, k = k, r2 = r2, df = n - k)
}

coef_rows <- function(eq_name, o) {
  se <- sqrt(diag(o$V)); t <- o$b / se; tc <- stats::qt(0.975, o$df)
  data.frame(方程 = eq_name, 预测变量 = names(o$b), b = o$b, SE = se, t = t,
             p = 2 * stats::pt(-abs(t), o$df), LLCI = o$b - tc * se, ULCI = o$b + tc * se,
             R2 = c(o$r2, rep(NA, length(o$b) - 1)), stringsAsFactors = FALSE, row.names = NULL)
}

# `d`: construct mean scores plus any observed variable the model names
# (e.g. gender as W, age as a covariate), all numeric.
process_model <- function(p, d, B, seed) {
  model <- as.integer(p$model); x <- p$x; y <- p$y
  m <- unlist(p[["m"]]); w <- p$w; covs <- unlist(p$covariates)
  center <- isTRUE(p$center %||% TRUE)
  cen <- function(v) if (center) v - mean(v) else v
  xv <- if (model %in% c(1, 7, 8)) cen(d[[x]]) else d[[x]]
  wv <- if (!is.null(w)) cen(d[[w]]) else NULL
  mv <- lapply(m, function(k) if (model == 14) cen(d[[k]]) else d[[k]])
  names(mv) <- m
  n <- nrow(d)
  cv <- if (length(covs)) as.matrix(d[covs]) else NULL

  # moderator probe values (in the analysed metric)
  wvals <- NULL
  if (!is.null(wv)) {
    u <- sort(unique(wv))
    wvals <- if (length(u) == 2) u else stats::quantile(wv, c(0.16, 0.50, 0.84), names = FALSE)
  }
  wshift <- if (!is.null(w) && center) mean(d[[w]]) else 0

  design <- function(idx) {
    X1 <- function(...) { cols <- list(...); M <- cbind(1, do.call(cbind, cols)); if (!is.null(cv)) M <- cbind(M, cv[idx, , drop = FALSE]); M }
    xi <- xv[idx]; wi <- if (!is.null(wv)) wv[idx]; yi <- d[[y]][idx]
    mi <- lapply(mv, function(v) v[idx])
    eq <- list()
    nm_c <- if (length(covs)) covs else character()
    if (model == 1) {
      X <- X1(xi, wi, xi * wi); colnames(X) <- c("常数", x, w, paste0(x, "×", w), nm_c)
      eq[[y]] <- list(y = yi, X = X)
    } else {
      for (j in seq_along(m)) {
        if (model %in% c(4, 14)) { X <- X1(xi); colnames(X) <- c("常数", x, nm_c) }
        else if (model == 6) {
          prev <- if (j > 1) do.call(cbind, mi[seq_len(j - 1)]) else NULL
          X <- if (is.null(prev)) X1(xi) else X1(xi, prev)
          colnames(X) <- c("常数", x, if (j > 1) m[seq_len(j - 1)], nm_c)
        } else { X <- X1(xi, wi, xi * wi); colnames(X) <- c("常数", x, w, paste0(x, "×", w), nm_c) }
        eq[[m[j]]] <- list(y = mi[[j]], X = X)
      }
      Mmat <- do.call(cbind, mi)
      if (model %in% c(4, 6, 7)) { X <- X1(xi, Mmat); colnames(X) <- c("常数", x, m, nm_c) }
      else if (model == 8) { X <- X1(xi, wi, xi * wi, Mmat); colnames(X) <- c("常数", x, w, paste0(x, "×", w), m, nm_c) }
      else { X <- X1(xi, Mmat, wi, Mmat * wi); colnames(X) <- c("常数", x, m, w, paste0(m, "×", w), nm_c) }
      eq[[y]] <- list(y = yi, X = X)
    }
    eq
  }

  effects <- function(fits) {
    out <- c()
    by <- fits[[y]]$b
    if (model == 1) {
      for (k in seq_along(wvals)) out[sprintf("cond|%d", k)] <- by[x] + by[paste0(x, "×", w)] * wvals[k]
      return(out)
    }
    a <- vapply(m, function(k) fits[[k]]$b[x], numeric(1))
    if (model %in% c(4, 6)) {
      if (model == 4) for (k in m) out[sprintf("ind|%s → %s → %s", x, k, y)] <- a[k] * by[k]
      else {
        subsets <- unlist(lapply(seq_along(m), function(s) utils::combn(m, s, simplify = FALSE)), recursive = FALSE)
        for (S in subsets) {
          eff <- fits[[S[1]]]$b[x]
          if (length(S) > 1) for (i in 2:length(S)) eff <- eff * fits[[S[i]]]$b[S[i - 1]]
          out[sprintf("ind|%s → %s → %s", x, paste(S, collapse = " → "), y)] <- eff * by[S[length(S)]]
        }
      }
      if (length(out) > 1) out["ind|总间接效应"] <- sum(out[grepl("^ind\\|", names(out))])
    } else if (model %in% c(7, 8)) {
      for (k in m) {
        a1 <- fits[[k]]$b[x]; a3 <- fits[[k]]$b[paste0(x, "×", w)]
        for (j in seq_along(wvals)) out[sprintf("cind|%s|%d", k, j)] <- (a1 + a3 * wvals[j]) * by[k]
        out[sprintf("imm|%s", k)] <- a3 * by[k]
      }
    } else if (model == 14) {
      for (k in m) {
        b1 <- by[k]; b3 <- by[paste0(k, "×", w)]
        for (j in seq_along(wvals)) out[sprintf("cind|%s|%d", k, j)] <- a[k] * (b1 + b3 * wvals[j])
        out[sprintf("imm|%s", k)] <- a[k] * b3
      }
    }
    out
  }

  fit_all <- function(idx) lapply(design(idx), function(e) ols(e$y, e$X))
  base <- fit_all(seq_len(n))
  est <- effects(base)

  set.seed(seed)
  boots <- matrix(NA_real_, B, length(est), dimnames = list(NULL, names(est)))
  for (r in seq_len(B)) {
    idx <- sample.int(n, n, replace = TRUE)
    boots[r, ] <- tryCatch(effects(lapply(design(idx), function(e) {
      f <- stats::lm.fit(e$X, e$y); list(b = setNames(f$coefficients, colnames(e$X)))
    })), error = function(e) NA)
  }
  ci <- apply(boots, 2, stats::quantile, c(0.025, 0.975), na.rm = TRUE)
  bse <- apply(boots, 2, stats::sd, na.rm = TRUE)

  coefs <- do.call(rbind, lapply(names(base), function(k) coef_rows(sprintf("结果变量：%s", k), base[[k]])))
  total <- NULL
  if (model %in% c(4, 6)) {
    X <- cbind(1, xv, if (!is.null(cv)) cv); colnames(X) <- c("常数", x, covs)
    total <- coef_rows(sprintf("总效应模型：%s", y), ols(d[[y]], X))
    coefs <- rbind(coefs, total)
  }

  w_label <- function(j) {
    raw <- wvals[j] + wshift
    if (length(wvals) == 2) sprintf("%s = %.3f", w, raw) else sprintf("%s = %.3f（第 %s 百分位）", w, raw, c(16, 50, 84)[j])
  }
  eff_rows <- lapply(names(est), function(k) {
    parts <- strsplit(k, "|", fixed = TRUE)[[1]]
    lab <- switch(parts[1],
      ind = parts[2],
      cind = sprintf("%s → %s → %s，%s", x, parts[2], y, w_label(as.integer(parts[3]))),
      imm = sprintf("有调节的中介指数（经 %s）", parts[2]),
      cond = sprintf("%s 对 %s 的条件效应，%s", x, y, w_label(as.integer(parts[2]))))
    data.frame(效应 = lab, Effect = est[[k]], BootSE = bse[[k]], BootLLCI = ci[1, k], BootULCI = ci[2, k],
               显著 = if (ci[1, k] * ci[2, k] > 0) "是" else "否", stringsAsFactors = FALSE)
  })
  effects_df <- do.call(rbind, eff_rows)
  if (model == 1) {
    # conditional effects use analytic SEs (as PROCESS does), not the bootstrap
    o <- base[[y]]; i1 <- x; i3 <- paste0(x, "×", w); tc <- stats::qt(0.975, o$df)
    se <- sqrt(o$V[i1, i1] + wvals^2 * o$V[i3, i3] + 2 * wvals * o$V[i1, i3])
    eff <- o$b[i1] + o$b[i3] * wvals
    effects_df <- data.frame(效应 = vapply(seq_along(wvals), function(j) sprintf("%s 对 %s 的条件效应，%s", x, y, w_label(j)), ""),
                             Effect = eff, SE = se, t = eff / se, p = 2 * stats::pt(-abs(eff / se), o$df),
                             LLCI = eff - tc * se, ULCI = eff + tc * se, stringsAsFactors = FALSE)
    # Johnson-Neyman points: (b1 + b3 w)^2 = t^2 Var(b1 + b3 w)
    A <- o$b[i3]^2 - tc^2 * o$V[i3, i3]; Bq <- 2 * (o$b[i1] * o$b[i3] - tc^2 * o$V[i1, i3]); C <- o$b[i1]^2 - tc^2 * o$V[i1, i1]
    disc <- Bq^2 - 4 * A * C
    jn <- if (disc >= 0 && A != 0) sort((-Bq + c(-1, 1) * sqrt(disc)) / (2 * A)) else numeric()
    jn <- jn[jn >= min(wv) & jn <= max(wv)]
    attr(effects_df, "jn") <- jn + wshift
    # R^2 change for the interaction
    Xr <- base[[y]]; full_r2 <- Xr$r2
    X0 <- cbind(1, xv, wv, if (!is.null(cv)) cv); r0 <- ols(d[[y]], X0)$r2
    df2 <- Xr$df; Fv <- (full_r2 - r0) / ((1 - full_r2) / df2)
    attr(effects_df, "r2_change") <- c(dR2 = full_r2 - r0, F = Fv, df1 = 1, df2 = df2, p = stats::pf(Fv, 1, df2, lower.tail = FALSE))
  }
  list(model = model, x = x, y = y, m = m, w = w, covariates = covs, center = center,
       coefs = coefs, effects = effects_df, B = B, seed = seed, n = n)
}
