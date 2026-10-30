# SPSS-side statistics: demographics, item descriptives, Harman, reliability, EFA.
# Formulas follow SPSS so the numbers can be checked line by line against the
# SPSS output (skewness/kurtosis are SPSS's G1/G2, alpha is the raw alpha,
# EFA is principal components + Kaiser-normalised rotation).

spss_skew <- function(x) {
  x <- x[!is.na(x)]; n <- length(x); z <- (x - mean(x)) / stats::sd(x)
  n / ((n - 1) * (n - 2)) * sum(z^3)
}
spss_kurt <- function(x) {
  x <- x[!is.na(x)]; n <- length(x); z <- (x - mean(x)) / stats::sd(x)
  n * (n + 1) / ((n - 1) * (n - 2) * (n - 3)) * sum(z^4) - 3 * (n - 1)^2 / ((n - 2) * (n - 3))
}

demographics_table <- function(df, vars, var_labels = NULL) {
  rows <- lapply(vars, function(v) {
    tab <- table(droplevels(as.factor(df[[v]])), useNA = "no")
    lv <- names(tab)
    data.frame(变量 = var_labels[[v]] %||% v, 类别 = lv, 人数 = as.integer(tab),
               百分比 = round(100 * as.numeric(tab) / sum(tab), 1), stringsAsFactors = FALSE)
  })
  do.call(rbind, rows)
}

item_descriptives <- function(df, items_by_construct, labels, item_labels) {
  rows <- list()
  for (k in names(items_by_construct)) for (it in items_by_construct[[k]]) {
    x <- df[[it]]
    rows[[length(rows) + 1]] <- data.frame(
      构念 = labels[[k]], 题项 = it, 题目 = item_labels[[it]] %||% "",
      N = sum(!is.na(x)), 最小值 = min(x, na.rm = TRUE), 最大值 = max(x, na.rm = TRUE),
      均值 = mean(x, na.rm = TRUE), 标准差 = stats::sd(x, na.rm = TRUE),
      偏度 = spss_skew(x), 峰度 = spss_kurt(x), stringsAsFactors = FALSE)
  }
  do.call(rbind, rows)
}

harman_test <- function(df, items) {
  ev <- eigen(stats::cor(df[items], use = "pairwise.complete.obs"), only.values = TRUE)$values
  list(first_pct = 100 * ev[1] / length(items), n_eigen_gt1 = sum(ev > 1),
       eigen = ev, pct = 100 * ev / length(items))
}

cronbach <- function(m) {
  m <- stats::na.omit(as.matrix(m)); k <- ncol(m)
  k / (k - 1) * (1 - sum(apply(m, 2, stats::var)) / stats::var(rowSums(m)))
}

reliability_table <- function(df, items_by_construct, labels) {
  rows <- list()
  for (k in names(items_by_construct)) {
    it <- items_by_construct[[k]]; m <- stats::na.omit(df[it]); a <- cronbach(m)
    for (j in it) {
      rest <- rowSums(m[setdiff(it, j)])
      rows[[length(rows) + 1]] <- data.frame(
        构念 = labels[[k]], 代码 = k, 题项 = j,
        CITC = stats::cor(m[[j]], rest),
        删除该项后α = if (length(it) > 2) cronbach(m[setdiff(it, j)]) else NA_real_,
        Cronbachα = a, 题项数 = length(it), stringsAsFactors = FALSE)
    }
  }
  do.call(rbind, rows)
}

efa_analysis <- function(df, items_by_construct, labels, rotation = "varimax") {
  items <- unlist(items_by_construct, use.names = FALSE)
  R <- stats::cor(df[items], use = "pairwise.complete.obs")
  n <- nrow(stats::na.omit(df[items]))
  kmo <- psych::KMO(R)
  bart <- psych::cortest.bartlett(R, n = n)
  nf <- length(items_by_construct)
  ev <- eigen(R, only.values = TRUE)$values
  pc <- suppressWarnings(psych::principal(R, nfactors = nf, rotate = rotation, n.obs = n))
  L <- unclass(pc$loadings)
  # name each component after the construct whose items load on it most
  owner <- rep(NA_character_, nf)
  score <- sapply(seq_len(nf), function(f) sapply(items_by_construct, function(it) mean(abs(L[it, f]))))
  score <- matrix(score, nrow = length(items_by_construct), dimnames = list(names(items_by_construct), NULL))
  for (step in seq_len(nf)) {
    idx <- which(score == max(score, na.rm = TRUE), arr.ind = TRUE)[1, ]
    owner[idx[2]] <- rownames(score)[idx[1]]
    score[idx[1], ] <- NA; score[, idx[2]] <- NA
  }
  ord <- match(names(items_by_construct), owner)
  L <- L[, ord, drop = FALSE]
  colnames(L) <- names(items_by_construct)
  ss <- colSums(L^2)
  load_df <- data.frame(题项 = items, 所属构念 = rep(names(items_by_construct), lengths(items_by_construct)),
                        round(L, 3), check.names = FALSE, stringsAsFactors = FALSE)
  flags <- character()
  for (k in names(items_by_construct)) for (it in items_by_construct[[k]]) {
    own <- abs(L[it, k]); other <- abs(L[it, setdiff(colnames(L), k)])
    if (own < 0.5) flags <- c(flags, sprintf("%s 在本构念（%s）上的载荷只有 %.3f（< 0.5）", it, k, own))
    if (length(other) && max(other) > 0.4) flags <- c(flags, sprintf("%s 在 %s 上有交叉载荷 %.3f（> 0.4）", it, names(which.max(other)), max(other)))
    if (length(other) && max(other) > own) flags <- c(flags, sprintf("%s 在 %s 上的载荷高于本构念，可能归错了维度", it, names(which.max(other))))
  }
  list(
    kmo = kmo$MSA, kmo_items = kmo$MSAi,
    bartlett_chisq = bart$chisq, bartlett_df = bart$df, bartlett_p = bart$p.value,
    eigen = ev, n_eigen_gt1 = sum(ev > 1),
    initial = data.frame(成分 = seq_along(ev), 特征值 = ev, 方差百分比 = 100 * ev / length(items),
                         累计百分比 = cumsum(100 * ev / length(items))),
    rotated_ss = ss, rotated_pct = 100 * ss / length(items),
    cum_pct = sum(100 * ss / length(items)),
    loadings = load_df, flags = unique(flags), n = n, rotation = rotation
  )
}

pearson_table <- function(scores, labels, sqrt_ave = NULL) {
  k <- ncol(scores); r <- stats::cor(scores); p <- matrix(NA, k, k)
  for (i in seq_len(k)) for (j in seq_len(k)) if (i != j) p[i, j] <- stats::cor.test(scores[[i]], scores[[j]])$p.value
  list(r = r, p = p, mean = colMeans(scores), sd = apply(scores, 2, stats::sd),
       labels = unlist(labels[colnames(scores)]), sqrt_ave = sqrt_ave)
}
