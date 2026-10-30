# AMOS-side statistics, computed with lavaan set up to reproduce AMOS defaults:
# ML estimation, first loading fixed to 1, chi-square = (N - 1) * F_min
# (lavaan likelihood = "wishart"), bias-corrected bootstrap CIs for indirect
# effects (AMOS "Bias-corrected confidence intervals" = lavaan "bca.simple").

FIT_KEYS <- c("chisq", "df", "pvalue", "cfi", "tli", "rmsea", "rmsea.ci.lower",
              "rmsea.ci.upper", "srmr", "gfi", "agfi", "nfi", "ifi", "aic", "bic")

lav_args <- function(spec) {
  if (spec$missing == "fiml") list(estimator = "ML", missing = "fiml", likelihood = "normal")
  else list(estimator = "ML", missing = "listwise", likelihood = "wishart")
}

error_covs_of <- function(mods) {
  lapply(Filter(function(m) m$type == "error_cov", mods), function(m) unlist(m[["items"]]))
}

measurement_syntax <- function(items_by_construct, error_covs = list()) {
  lines <- vapply(names(items_by_construct), function(k)
    paste(k, "=~", paste(items_by_construct[[k]], collapse = " + ")), character(1))
  ec <- vapply(error_covs, function(p) paste(p[1], "~~", p[2]), character(1))
  paste(c(lines, ec), collapse = "\n")
}

structural_syntax <- function(edges, controls_by_dv = list(), labelled = TRUE) {
  dvs <- unique(edges$dv)
  lines <- vapply(dvs, function(dv) {
    e <- edges[edges$dv == dv, ]
    rhs <- if (labelled) paste0(e$label, "*", e$iv) else e$iv
    rhs <- c(rhs, controls_by_dv[[dv]])
    paste(dv, "~", paste(rhs, collapse = " + "))
  }, character(1))
  paste(lines, collapse = "\n")
}

indirect_syntax <- function(spec, edges) {
  out <- character()
  for (h in names(spec$indirect)) {
    p <- parse_arrow(spec$indirect[[h]])
    labs <- vapply(seq_len(length(p) - 1), function(i) edges$label[edges$iv == p[i] & edges$dv == p[i + 1]], character(1))
    out <- c(out, sprintf("%s := %s", h, paste(labs, collapse = "*")))
  }
  for (pr in effect_pairs(spec)) {
    chains <- all_chains(edges, pr[1], pr[2])
    ind <- Filter(function(ch) length(ch) > 2, chains)
    terms <- vapply(ind, function(ch) paste(vapply(seq_len(length(ch) - 1), function(i)
      edges$label[edges$iv == ch[i] & edges$dv == ch[i + 1]], character(1)), collapse = "*"), character(1))
    direct <- edges$label[edges$iv == pr[1] & edges$dv == pr[2]]
    tag <- paste0(pr[1], "_", pr[2])
    out <- c(out, sprintf("TI_%s := %s", tag, paste(terms, collapse = " + ")))
    out <- c(out, sprintf("TOT_%s := %s", tag, paste(c(direct, terms), collapse = " + ")))
  }
  paste(out, collapse = "\n")
}

effect_pairs <- function(spec) {
  prs <- lapply(spec$indirect, function(s) { p <- parse_arrow(s); c(p[1], p[length(p)]) })
  unique(prs)
}

fit_cfa <- function(spec, df, items_by_construct, error_covs = list()) {
  model <- measurement_syntax(items_by_construct, error_covs)
  fit <- do.call(lavaan::cfa, c(list(model = model, data = df), lav_args(spec)))
  attr(fit, "syntax") <- model
  fit
}

fit_indices <- function(fit) {
  fm <- lavaan::fitMeasures(fit, FIT_KEYS)
  out <- as.list(unclass(fm))
  out$chisq_df <- out$chisq / out$df
  out$n <- lavaan::lavInspect(fit, "ntotal")
  out
}

fit_verdicts <- function(f) {
  j <- function(ok, good) if (is.na(ok)) "—" else if (good) "良好" else if (ok) "可接受" else "未达标"
  c(chisq_df = j(f$chisq_df < 5, f$chisq_df < 3),
    cfi = j(f$cfi > 0.90, f$cfi >= 0.95), tli = j(f$tli > 0.90, f$tli >= 0.95),
    rmsea = j(f$rmsea < 0.08, f$rmsea <= 0.06), srmr = j(f$srmr < 0.08, f$srmr <= 0.05),
    gfi = j(f$gfi > 0.80, f$gfi >= 0.90), agfi = j(f$agfi > 0.80, f$agfi >= 0.90),
    nfi = j(f$nfi > 0.90, f$nfi >= 0.95), ifi = j(f$ifi > 0.90, f$ifi >= 0.95))
}

loadings_table <- function(fit, labels) {
  pe <- lavaan::parameterEstimates(fit, standardized = TRUE)
  pe <- pe[pe$op == "=~", ]
  fixed <- is.na(pe$se) | pe$se == 0
  data.frame(
    构念 = unlist(labels[pe$lhs]), 代码 = pe$lhs, 题项 = pe$rhs,
    非标准化载荷 = pe$est, SE = ifelse(fixed, NA, pe$se), CR_z = ifelse(fixed, NA, pe$z),
    p = ifelse(fixed, NA, pe$pvalue), 标准化载荷 = pe$std.all, SMC = pe$std.all^2,
    stringsAsFactors = FALSE)
}

validity_table <- function(ld, labels) {
  out <- lapply(split(ld, factor(ld$代码, levels = unique(ld$代码))), function(d) {
    l <- d$标准化载荷
    cr <- sum(l)^2 / (sum(l)^2 + sum(1 - l^2))
    data.frame(构念 = d$构念[1], 代码 = d$代码[1], 题项数 = nrow(d),
               最小载荷 = min(l), 最大载荷 = max(l), CR = cr, AVE = mean(l^2), sqrtAVE = sqrt(mean(l^2)))
  })
  do.call(rbind, out)
}

fornell_larcker <- function(fit, val) {
  phi <- lavaan::lavInspect(fit, "cor.lv")
  if (is.list(phi) && !is.matrix(phi)) phi <- phi[[1]]
  phi <- phi[val$代码, val$代码, drop = FALSE]
  m <- phi; diag(m) <- val$sqrtAVE
  ok <- vapply(seq_len(nrow(m)), function(i) all(val$sqrtAVE[i] > abs(phi[i, -i])), logical(1))
  list(matrix = m, latent_cor = phi, pass = setNames(ok, val$代码))
}

htmt_matrix <- function(df, items_by_construct) {
  model <- measurement_syntax(items_by_construct)
  h <- semTools::htmt(model, data = df[unlist(items_by_construct)])
  as.matrix(h)
}

mod_suggestions <- function(fit, items_by_construct, top = 10) {
  mi <- tryCatch(lavaan::modindices(fit, sort. = TRUE, minimum.value = 4), error = function(e) NULL)
  if (is.null(mi) || !nrow(mi)) return(data.frame())
  owner <- setNames(rep(names(items_by_construct), lengths(items_by_construct)), unlist(items_by_construct))
  mi <- mi[mi$op %in% c("~~", "=~"), ]
  mi$类型 <- ifelse(mi$op == "=~", "交叉载荷", ifelse(mi$lhs %in% names(owner) & mi$rhs %in% names(owner), "误差相关", "其他"))
  mi$建议 <- ifelse(mi$类型 == "误差相关" & owner[mi$lhs] == owner[mi$rhs],
                   "同一构念内的误差相关：只有题干确实相似时才可考虑，必须写理由",
                   "跨构念 / 交叉载荷：不建议按此修正（会破坏区分效度）")
  mi$建议[mi$类型 == "其他"] <- "不建议"
  head(data.frame(参数 = paste(mi$lhs, mi$op, mi$rhs), 类型 = mi$类型, MI = mi$mi, 预期改变EPC = mi$epc,
                  建议 = mi$建议, stringsAsFactors = FALSE), top)
}

modification_steps <- function(spec, df) {
  base_items <- lapply(spec$constructs, `[[`, "items")
  mods <- spec$modifications
  steps <- list()
  cur_items <- base_items; cur_ec <- list()
  fit0 <- fit_cfa(spec, df, cur_items, cur_ec)
  steps[[1]] <- list(step = "初始模型", detail = "按设定卡的题项，无任何修正", reason = "", evidence = "", fit = fit_indices(fit0))
  prev <- fit0
  for (m in mods) {
    # evidence is read off the model *before* this modification
    if (m$type == "drop_item") {
      ss <- lavaan::standardizedSolution(prev)
      l <- ss$est.std[ss$op == "=~" & ss$rhs == m[["item"]]][1]
      ev <- sprintf("上一步模型中 %s 的标准化载荷 = %.3f", m[["item"]], l)
      cur_items <- lapply(cur_items, function(it) setdiff(it, m[["item"]]))
      desc <- sprintf("删除题项 %s", m[["item"]])
    } else {
      p <- unlist(m[["items"]])
      mi <- lavaan::modindices(prev, sort. = TRUE)
      mi <- mi[mi$op == "~~" & mi$lhs != mi$rhs, ]
      hit <- which((mi$lhs == p[1] & mi$rhs == p[2]) | (mi$lhs == p[2] & mi$rhs == p[1]))
      ev <- if (length(hit)) sprintf("上一步模型中该误差相关的 MI = %.2f（在所有误差相关里排第 %d）", mi$mi[hit[1]], hit[1]) else "上一步模型中没有这项 MI"
      if (length(hit) && grepl("最大", m$reason) && hit[1] != 1) ev <- paste0(ev, "。⚠ 理由写的是「MI 最大」，与数据不符，请改理由")
      if (!length(hit) || mi$mi[hit[1]] < 4) ev <- paste0(ev, "。⚠ MI < 4，数据并不支持这项修正")
      cur_ec <- c(cur_ec, list(p))
      desc <- sprintf("增加误差相关 %s ↔ %s", p[1], p[2])
    }
    f <- fit_cfa(spec, df, cur_items, cur_ec)
    steps[[length(steps) + 1]] <- list(step = sprintf("修正 %d", length(steps)), detail = desc, reason = m$reason, evidence = ev, fit = fit_indices(f))
    prev <- f
  }
  list(steps = steps, initial_fit = fit0)
}

cmb_single_factor <- function(spec, df, items_by_construct, error_covs, cfa_fit) {
  items <- unlist(items_by_construct)
  model <- paste("CMB =~", paste(items, collapse = " + "))
  one <- do.call(lavaan::cfa, c(list(model = model, data = df), lav_args(spec)))
  lrt <- lavaan::lavTestLRT(one, cfa_fit)
  list(fit = fit_indices(one), delta_chisq = lrt[2, "Chisq diff"], delta_df = lrt[2, "Df diff"], p = lrt[2, "Pr(>Chisq)"])
}

controls_by_dv <- function(spec) {
  if (!length(spec$controls)) return(list())
  setNames(rep(list(spec$controls), length(names(spec$structural))), names(spec$structural))
}

sem_syntax <- function(spec, items_by_construct, error_covs, edges) {
  paste(measurement_syntax(items_by_construct, error_covs),
        structural_syntax(edges, controls_by_dv(spec)),
        indirect_syntax(spec, edges), sep = "\n")
}

fit_sem <- function(spec, df, items_by_construct, error_covs, edges, boot = 0) {
  model <- sem_syntax(spec, items_by_construct, error_covs, edges)
  args <- c(list(model = model, data = df), lav_args(spec))
  fit <- do.call(lavaan::sem, args)
  bfit <- NULL
  if (boot > 0 && length(spec$indirect)) {
    set.seed(spec$seed)
    par <- if (.Platform$OS.type == "windows") "no" else "multicore"
    ncpus <- max(1L, min(8L, parallel::detectCores() - 1L))
    bfit <- tryCatch(
      do.call(lavaan::sem, c(args, list(se = "bootstrap", bootstrap = boot, parallel = par, ncpus = ncpus, iseed = spec$seed))),
      error = function(e) { set.seed(spec$seed); do.call(lavaan::sem, c(args, list(se = "bootstrap", bootstrap = boot))) })
  }
  list(fit = fit, boot = bfit, syntax = model)
}

path_table <- function(fit, spec, edges, labels) {
  pe <- lavaan::parameterEstimates(fit, standardized = TRUE)
  rows <- lapply(names(spec$hypotheses), function(h) {
    p <- parse_arrow(spec$hypotheses[[h]])
    lab <- edges$label[edges$iv == p[1] & edges$dv == p[2]]
    r <- pe[pe$label == lab & pe$op == "~", ][1, ]
    data.frame(假设 = h, 路径 = sprintf("%s → %s", labels[[p[1]]], labels[[p[2]]]), 代码 = sprintf("%s → %s", p[1], p[2]),
               参数标签 = lab, 标准化系数β = r$std.all, 非标准化系数 = r$est, SE = r$se, CR_z = r$z, p = r$pvalue,
               结论 = if (r$pvalue < 0.05) "支持" else "不支持", stringsAsFactors = FALSE)
  })
  do.call(rbind, rows)
}

r2_table <- function(fit, labels) {
  r2 <- lavaan::lavInspect(fit, "r2")
  r2 <- r2[names(r2) %in% names(labels)]
  data.frame(构念 = unlist(labels[names(r2)]), 代码 = names(r2), R2 = as.numeric(r2), stringsAsFactors = FALSE)
}

effects_tables <- function(sem_res, spec, edges, labels) {
  fit <- sem_res$fit; b <- sem_res$boot
  std <- lavaan::standardizedSolution(fit)
  std <- std[std$op == ":=", c("lhs", "op", "est.std")]
  if (!is.null(b)) {
    bc <- lavaan::parameterEstimates(b, boot.ci.type = "bca.simple", level = 0.95)
    pc <- lavaan::parameterEstimates(b, boot.ci.type = "perc", level = 0.95)
  } else {
    bc <- pc <- lavaan::parameterEstimates(fit)
  }
  get <- function(tab, name, col) { v <- tab[tab$lhs == name & tab$op == ":=", col]; if (length(v)) v[1] else NA_real_ }
  pe <- lavaan::parameterEstimates(fit)
  one <- function(name, what, chain_txt) {
    est <- get(pe, name, "est")
    data.frame(编号 = what, 效应 = chain_txt, 效应值 = est,
               BootSE = get(bc, name, "se"),
               BC下限 = get(bc, name, "ci.lower"), BC上限 = get(bc, name, "ci.upper"),
               百分位下限 = get(pc, name, "ci.lower"), 百分位上限 = get(pc, name, "ci.upper"),
               标准化效应 = get(std, name, "est.std"), stringsAsFactors = FALSE)
  }
  specific <- do.call(rbind, lapply(names(spec$indirect), function(h) {
    p <- parse_arrow(spec$indirect[[h]])
    one(h, h, paste(unlist(labels[p]), collapse = " → "))
  }))
  specific$显著 <- with(specific, ifelse(BC下限 * BC上限 > 0, "是", "否"))

  pairs <- effect_pairs(spec)
  dec <- do.call(rbind, lapply(pairs, function(pr) {
    tag <- paste0(pr[1], "_", pr[2])
    dl <- edges$label[edges$iv == pr[1] & edges$dv == pr[2]]
    d <- if (length(dl)) {
      r <- pe[pe$label == dl & pe$op == "~", ][1, ]
      rb <- bc[bc$label == dl & bc$op == "~", ][1, ]
      data.frame(编号 = "直接效应", 效应 = sprintf("%s → %s", labels[[pr[1]]], labels[[pr[2]]]), 效应值 = r$est, BootSE = rb$se,
                 BC下限 = rb$ci.lower, BC上限 = rb$ci.upper, 百分位下限 = NA, 百分位上限 = NA,
                 标准化效应 = lavaan::standardizedSolution(fit)[lavaan::standardizedSolution(fit)$label == dl, "est.std"][1])
    } else data.frame(编号 = "直接效应", 效应 = sprintf("%s → %s（模型中无直接路径）", labels[[pr[1]]], labels[[pr[2]]]),
                      效应值 = 0, BootSE = NA, BC下限 = NA, BC上限 = NA, 百分位下限 = NA, 百分位上限 = NA, 标准化效应 = 0)
    ti <- one(paste0("TI_", tag), "总间接效应", sprintf("%s ⇒ %s 的全部间接路径之和", labels[[pr[1]]], labels[[pr[2]]]))
    to <- one(paste0("TOT_", tag), "总效应", sprintf("%s ⇒ %s", labels[[pr[1]]], labels[[pr[2]]]))
    out <- rbind(d, ti, to)
    out$配对 <- sprintf("%s → %s", pr[1], pr[2])
    out
  }))
  dec$显著 <- with(dec, ifelse(is.na(BC下限), "—", ifelse(BC下限 * BC上限 > 0, "是", "否")))

  # Zhao, Lynch & Chen (2010) mediation typology per specific indirect effect
  specific$中介类型 <- vapply(seq_len(nrow(specific)), function(i) {
    p <- parse_arrow(spec$indirect[[specific$编号[i]]])
    d <- dec[dec$配对 == sprintf("%s → %s", p[1], p[length(p)]) & dec$编号 == "直接效应", ]
    dl <- edges$label[edges$iv == p[1] & edges$dv == p[length(p)]]
    ind_sig <- specific$显著[i] == "是"
    # direct effect judged by the same ML z-test as the hypothesis table
    dir_sig <- length(dl) > 0 && pe$pvalue[pe$label == dl & pe$op == "~"][1] < 0.05
    if (!ind_sig && dir_sig) "仅直接效应（无中介）"
    else if (!ind_sig) "无效应（无中介）"
    else if (!length(dl)) "仅间接效应（模型未设直接路径）"
    else if (!dir_sig) "仅间接效应（完全中介）"
    else if (sign(d$效应值) == sign(specific$效应值[i])) "互补型部分中介"
    else "竞争型部分中介"
  }, character(1))
  list(specific = specific, decomposition = dec)
}

multigroup_analysis <- function(spec, df, items_by_construct, error_covs, edges) {
  g <- spec$multigroup
  lv <- sort(unique(df[[g]]))
  if (length(lv) != 2) return(list(skipped = sprintf("分组变量 %s 有 %d 个水平，多群组比较目前只支持 2 组", g, length(lv))))
  meas <- measurement_syntax(items_by_construct, error_covs)
  a <- lav_args(spec)
  fitg <- function(eq) do.call(lavaan::cfa, c(list(model = meas, data = df, group = g, group.equal = eq), a))
  conf <- fitg(character()); metr <- fitg("loadings"); scal <- fitg(c("loadings", "intercepts"))
  rows <- list(conf, metr, scal); nm <- c("形态等价", "弱等价（载荷相等）", "强等价（载荷 + 截距相等）")
  tab <- do.call(rbind, lapply(seq_along(rows), function(i) {
    f <- fit_indices(rows[[i]])
    data.frame(模型 = nm[i], chisq = f$chisq, df = f$df, CFI = f$cfi, TLI = f$tli, RMSEA = f$rmsea, SRMR = f$srmr)
  }))
  tab$Δchisq <- c(NA, diff(tab$chisq)); tab$Δdf <- c(NA, diff(tab$df))
  tab$p <- c(NA, stats::pchisq(tab$Δchisq[-1], tab$Δdf[-1], lower.tail = FALSE))
  tab$ΔCFI <- c(NA, diff(tab$CFI)); tab$ΔRMSEA <- c(NA, diff(tab$RMSEA))
  tab$判断 <- c("基准", ifelse(abs(tab$ΔCFI[-1]) <= 0.01 & abs(tab$ΔRMSEA[-1]) <= 0.015, "成立", "不成立"))

  # structural paths by group (loadings held equal so paths are comparable)
  # unlabelled: a shared label would force the path equal across groups
  full <- paste(meas, structural_syntax(edges, controls_by_dv(spec), labelled = FALSE), sep = "\n")
  sg <- do.call(lavaan::sem, c(list(model = full, data = df, group = g, group.equal = "loadings"), a))
  pe <- lavaan::parameterEstimates(sg, standardized = TRUE)
  pe <- pe[pe$op == "~" & pe$lhs %in% names(items_by_construct) & pe$rhs %in% names(items_by_construct), ]
  gl <- lavaan::lavInspect(sg, "group.label")
  paths <- do.call(rbind, lapply(seq_len(nrow(edges)), function(i) {
    r1 <- pe[pe$lhs == edges$dv[i] & pe$rhs == edges$iv[i] & pe$group == 1, ]
    r2 <- pe[pe$lhs == edges$dv[i] & pe$rhs == edges$iv[i] & pe$group == 2, ]
    z <- (r2$est - r1$est) / sqrt(r1$se^2 + r2$se^2)
    data.frame(路径 = sprintf("%s → %s", edges$iv[i], edges$dv[i]),
               b_组1 = r1$est, β_组1 = r1$std.all, p_组1 = r1$pvalue,
               b_组2 = r2$est, β_组2 = r2$std.all, p_组2 = r2$pvalue,
               差异临界比z = z, p_差异 = 2 * stats::pnorm(-abs(z)))
  }))
  names(paths) <- sub("组1", gl[1], sub("组2", gl[2], names(paths)))
  list(invariance = tab, paths = paths, groups = gl, var = g, var_label = g, n = table(df[[g]]))
}
