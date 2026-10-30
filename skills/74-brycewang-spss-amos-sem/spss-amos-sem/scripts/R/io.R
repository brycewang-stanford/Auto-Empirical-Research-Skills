# Spec card + data loading + questionnaire cleaning.

`%||%` <- function(a, b) if (is.null(a)) b else a

SPEC_DEFAULTS <- list(
  project = "问卷数据结构方程分析",
  id = NULL,
  scale_points = 5,
  reverse_items = character(),
  missing = "listwise",
  drop_straightliners = FALSE,
  demographics = character(),
  controls = character(),
  structural = list(),
  hypotheses = list(),
  indirect = list(),
  multigroup = NULL,
  process = list(),
  modifications = list(),
  bootstrap = 2000,
  process_bootstrap = 5000,
  seed = 20261027,
  efa_rotation = "varimax",
  loading_cutoff = 0.5
)

ident_ok <- function(x) grepl("^[A-Za-z][A-Za-z0-9_]*$", x)

parse_arrow <- function(s) trimws(strsplit(s, "->", fixed = TRUE)[[1]])

# YAML 1.1 reads y / n / yes / no / on / off as booleans, which would turn the
# PROCESS key `y:` (or a construct coded ON) into TRUE. Only true/false count.
YAML_HANDLERS <- list(
  "bool#yes" = function(x) if (tolower(x) == "true") TRUE else x,
  "bool#no" = function(x) if (tolower(x) == "false") FALSE else x
)

read_spec <- function(path) {
  spec <- yaml::read_yaml(path, fileEncoding = "UTF-8", handlers = YAML_HANDLERS)
  spec$.path <- normalizePath(path)
  spec$.dir <- dirname(spec$.path)
  for (k in names(SPEC_DEFAULTS)) if (is.null(spec[[k]])) spec[k] <- list(SPEC_DEFAULTS[[k]])
  spec$reverse_items <- unlist(spec$reverse_items) %||% character()
  spec$demographics <- unlist(spec$demographics) %||% character()
  spec$controls <- unlist(spec$controls) %||% character()
  for (k in names(spec$constructs)) {
    spec$constructs[[k]]$items <- unlist(spec$constructs[[k]]$items)
    spec$constructs[[k]]$label <- spec$constructs[[k]]$label %||% k
  }
  spec$structural <- lapply(spec$structural, unlist)
  if (!length(spec$hypotheses)) {
    h <- list(); i <- 0
    for (dv in names(spec$structural)) for (iv in spec$structural[[dv]]) {
      i <- i + 1; h[[paste0("H", i)]] <- paste(iv, "->", dv)
    }
    spec$hypotheses <- h
  }
  validate_spec(spec)
  spec
}

validate_spec <- function(spec) {
  err <- character()
  if (is.null(spec$data)) err <- c(err, "缺少 data：数据文件路径")
  cons <- names(spec$constructs)
  if (!length(cons)) err <- c(err, "constructs 为空：至少要有一个构念")
  bad <- cons[!ident_ok(cons) | nchar(cons) > 6]
  if (length(bad)) err <- c(err, sprintf("构念代码必须是字母开头、只含字母数字下划线、不超过 6 个字符（AMOS 变量名 + PROCESS 的 8 字符限制）：%s", paste(bad, collapse = ", ")))
  all_items <- unlist(lapply(spec$constructs, `[[`, "items"))
  dup <- unique(all_items[duplicated(all_items)])
  if (length(dup)) err <- c(err, sprintf("题项同时出现在多个构念里：%s", paste(dup, collapse = ", ")))
  if (any(all_items %in% cons)) err <- c(err, "题项名不能和构念代码重名（AMOS 会把它当成观测变量）")
  for (k in cons) if (length(spec$constructs[[k]]$items) < 2)
    err <- c(err, sprintf("构念 %s 少于 2 个题项，无法识别", k))
  endo <- names(spec$structural)
  for (dv in endo) {
    if (!dv %in% cons) err <- c(err, sprintf("structural 的因变量 %s 不是构念", dv))
    for (iv in spec$structural[[dv]]) if (!iv %in% c(cons, spec$controls))
      err <- c(err, sprintf("structural 里 %s 的自变量 %s 既不是构念也不在 controls 里", dv, iv))
  }
  if (length(endo) && has_cycle(spec$structural)) err <- c(err, "结构模型有环（非递归模型），本流程只支持递归模型")
  edges <- structural_edges(spec)
  for (h in names(spec$hypotheses)) {
    p <- parse_arrow(spec$hypotheses[[h]])
    if (length(p) != 2 || !any(edges$iv == p[1] & edges$dv == p[2]))
      err <- c(err, sprintf("假设 %s「%s」在 structural 里没有对应路径", h, spec$hypotheses[[h]]))
  }
  for (h in names(spec$indirect)) {
    p <- parse_arrow(spec$indirect[[h]])
    if (length(p) < 3) err <- c(err, sprintf("间接效应 %s 至少要三个构念（X -> M -> Y）", h))
    for (i in seq_len(length(p) - 1)) if (!any(edges$iv == p[i] & edges$dv == p[i + 1]))
      err <- c(err, sprintf("间接效应 %s：%s -> %s 不是结构路径", h, p[i], p[i + 1]))
  }
  for (m in spec$modifications) {
    if (!m$type %in% c("drop_item", "error_cov")) err <- c(err, sprintf("未知的修正类型 %s（只支持 drop_item / error_cov）", m$type))
    if (is.null(m$reason) || !nzchar(trimws(m$reason))) err <- c(err, "每条 modifications 都必须写 reason（修正理由）")
    its <- unlist(c(m[["item"]], m[["items"]]))
    if (!all(its %in% all_items)) err <- c(err, sprintf("修正里的题项不存在：%s", paste(setdiff(its, all_items), collapse = ", ")))
  }
  for (p in spec$process) {
    if (!p$model %in% c(1, 4, 6, 7, 8, 14)) err <- c(err, sprintf("PROCESS 模型 %s 暂不支持（支持 1/4/6/7/8/14）", p$model))
    need_w <- p$model %in% c(1, 7, 8, 14)
    if (need_w && is.null(p$w)) err <- c(err, sprintf("PROCESS 模型 %s 需要 w（调节变量）", p$model))
    if (p$model != 1 && is.null(p[["m"]])) err <- c(err, sprintf("PROCESS 模型 %s 需要 m（中介变量）", p$model))
    if (p$model == 6 && !length(unlist(p[["m"]])) %in% 2:4) err <- c(err, "PROCESS 模型 6 需要 2–4 个按顺序排列的中介变量")
  }
  if (!spec$missing %in% c("listwise", "fiml")) err <- c(err, "missing 只能是 listwise 或 fiml")
  if (length(err)) stop(paste0("设定卡有问题：\n  - ", paste(err, collapse = "\n  - ")), call. = FALSE)
  invisible(TRUE)
}

structural_edges <- function(spec) {
  rows <- lapply(names(spec$structural), function(dv)
    data.frame(iv = spec$structural[[dv]], dv = dv, stringsAsFactors = FALSE))
  e <- do.call(rbind, rows)
  if (is.null(e)) e <- data.frame(iv = character(), dv = character())
  e <- e[e$iv %in% names(spec$constructs), , drop = FALSE]
  if (nrow(e)) e$label <- paste0("P", seq_len(nrow(e)))
  else e$label <- character()
  rownames(e) <- NULL
  e
}

has_cycle <- function(structural) {
  nodes <- unique(c(names(structural), unlist(structural)))
  state <- setNames(rep(0, length(nodes)), nodes)
  visit <- function(v) {
    if (state[[v]] == 1) return(TRUE)
    if (state[[v]] == 2) return(FALSE)
    state[[v]] <<- 1
    kids <- names(structural)[vapply(structural, function(ivs) v %in% ivs, logical(1))]
    for (k in kids) if (visit(k)) return(TRUE)
    state[[v]] <<- 2
    FALSE
  }
  any(vapply(nodes, visit, logical(1)))
}

# Every directed path from x to y in the structural DAG, as character vectors.
all_chains <- function(edges, x, y) {
  out <- list()
  walk <- function(node, path) {
    if (node == y) { out[[length(out) + 1]] <<- path; return(invisible()) }
    for (nx in edges$dv[edges$iv == node]) walk(nx, c(path, nx))
  }
  walk(x, x)
  out
}

active_items <- function(spec) {
  dropped <- unlist(lapply(Filter(function(m) m$type == "drop_item", spec$modifications), `[[`, "item"))
  lapply(spec$constructs, function(k) setdiff(k$items, dropped))
}

read_raw <- function(spec) {
  f <- file.path(spec$.dir, spec$data)
  if (!file.exists(f)) stop(sprintf("找不到数据文件：%s", f), call. = FALSE)
  ext <- tolower(tools::file_ext(f))
  df <- switch(ext,
    sav = , zsav = haven::read_sav(f),
    dta = haven::read_dta(f),
    csv = utils::read.csv(f, fileEncoding = "UTF-8-BOM", check.names = FALSE),
    xlsx = openxlsx::read.xlsx(f),
    xls = as.data.frame(readxl::read_excel(f)),
    stop(sprintf("不支持的数据格式 .%s（支持 sav/zsav/dta/csv/xlsx/xls）", ext), call. = FALSE)
  )
  as.data.frame(df)
}

clean_data <- function(spec, raw) {
  log <- list()
  items <- unlist(lapply(spec$constructs, `[[`, "items"))
  need <- unique(c(items, spec$demographics, spec$controls, spec$multigroup, spec$id, process_observed(spec)))
  miss_vars <- setdiff(need, names(raw))
  if (length(miss_vars)) stop(sprintf("数据里找不到这些变量：%s", paste(miss_vars, collapse = ", ")), call. = FALSE)

  item_labels <- vapply(items, function(v) attr(raw[[v]], "label") %||% "", character(1))
  demo_levels <- list()
  df <- raw
  df$.row <- seq_len(nrow(df))
  for (v in unique(c(spec$demographics, spec$multigroup))) {
    lab <- attr(raw[[v]], "labels")
    demo_levels[[v]] <- if (!is.null(lab)) lab else NULL
    # factor in value-label order, so tables list 男/女 or age groups as coded
    df[[v]] <- droplevels(if (inherits(raw[[v]], "haven_labelled")) haven::as_factor(raw[[v]], levels = "labels") else factor(raw[[v]]))
  }
  for (v in c(items, spec$controls)) df[[v]] <- as.numeric(haven::zap_labels(raw[[v]]))

  n_raw <- nrow(df)
  # out-of-range Likert codes (e.g. 9 not declared as SPSS user-missing)
  oor <- 0
  for (v in items) {
    bad <- !is.na(df[[v]]) & (df[[v]] < 1 | df[[v]] > spec$scale_points | df[[v]] != round(df[[v]]))
    oor <- oor + sum(bad); df[[v]][bad] <- NA
  }
  log$out_of_range <- oor

  # straight-lining is judged on the raw answers, before reverse coding turns
  # "all 5s" into a mix; same rule as the SPSS syntax (SD of answered items = 0)
  sl <- apply(df[items], 1, function(r) { r <- r[!is.na(r)]; length(r) >= 2 && length(unique(r)) == 1 })
  log$straightliners <- sum(sl)
  if (isTRUE(spec$drop_straightliners)) df <- df[!sl, , drop = FALSE]
  n_after_sl <- nrow(df)

  for (v in spec$reverse_items) df[[v]] <- spec$scale_points + 1 - df[[v]]
  log$reversed <- spec$reverse_items

  use_vars <- unique(c(items, spec$demographics, spec$controls, spec$multigroup, process_observed(spec)))
  cc <- stats::complete.cases(df[use_vars])
  log$incomplete <- sum(!cc)
  if (spec$missing == "listwise") df <- df[cc, , drop = FALSE]
  else df <- df[stats::complete.cases(df[unique(c(spec$demographics, spec$controls, spec$multigroup))]), , drop = FALSE]
  rownames(df) <- NULL

  log$n_raw <- n_raw
  log$n_after_straightliners <- n_after_sl
  log$n_used <- nrow(df)
  list(data = df, log = log, item_labels = item_labels, demo_levels = demo_levels)
}

# variables PROCESS models use that are not constructs (observed W / covariates)
process_observed <- function(spec) {
  v <- unlist(lapply(spec$process, function(p) c(p$x, p$y, unlist(p[["m"]]), p$w, unlist(p$covariates))))
  setdiff(unique(v), names(spec$constructs))
}

process_data <- function(spec, raw, df, scores) {
  out <- scores
  for (v in process_observed(spec)) {
    x <- suppressWarnings(as.numeric(haven::zap_labels(raw[[v]])))[df$.row]
    if (all(is.na(x))) stop(sprintf("PROCESS 用到的变量 %s 不是数值型，无法进入回归", v), call. = FALSE)
    out[[v]] <- x
  }
  out
}

mean_scores <- function(df, items_by_construct) {
  as.data.frame(lapply(items_by_construct, function(it) rowMeans(df[it], na.rm = TRUE)))
}
