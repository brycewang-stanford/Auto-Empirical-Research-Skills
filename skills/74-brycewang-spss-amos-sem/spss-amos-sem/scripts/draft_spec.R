#!/usr/bin/env Rscript
# Look at a questionnaire file and draft a spec card from it.
#
#   Rscript scripts/draft_spec.R <data.sav|csv|xlsx|dta> [--out spec.yml]
#
# Prints a variable overview (name, SPSS label, range, missing), groups Likert
# items by name prefix (PU1 PU2 ... -> PU), flags items that correlate
# negatively with the rest of their group (likely reverse-worded), and writes a
# draft spec with TODOs. The draft is a starting point: constructs, structural
# paths and hypotheses come from the user's theory, not from this script.

suppressPackageStartupMessages({ library(haven) })
`%||%` <- function(a, b) if (is.null(a)) b else a

args <- commandArgs(trailingOnly = TRUE)
if (!length(args)) { cat("用法：Rscript scripts/draft_spec.R <数据文件> [--out spec.yml]\n"); quit(status = 1) }
f <- normalizePath(args[1])
out <- if ("--out" %in% args) args[which(args == "--out") + 1] else file.path(dirname(f), "spec_draft.yml")
ext <- tolower(tools::file_ext(f))
d <- switch(ext,
  sav = , zsav = read_sav(f), dta = read_dta(f),
  csv = utils::read.csv(f, fileEncoding = "UTF-8-BOM", check.names = FALSE),
  xlsx = openxlsx::read.xlsx(f), xls = as.data.frame(readxl::read_excel(f)),
  stop("不支持的格式：", ext))
d <- as.data.frame(d)

info <- do.call(rbind, lapply(names(d), function(v) {
  x <- d[[v]]; num <- is.numeric(x)
  xv <- if (num) as.numeric(zap_labels(x)) else NA
  data.frame(变量 = v, 标签 = attr(x, "label") %||% "", 类型 = if (num) "数值" else "文本",
             取值个数 = length(unique(stats::na.omit(x))),
             最小 = if (num) suppressWarnings(min(xv, na.rm = TRUE)) else NA,
             最大 = if (num) suppressWarnings(max(xv, na.rm = TRUE)) else NA,
             缺失 = sum(is.na(x)), 有值标签 = !is.null(attr(x, "labels")), stringsAsFactors = FALSE)
}))
cat(sprintf("数据：%s（%d 行 × %d 列）\n\n", basename(f), nrow(d), ncol(d)))
print(info, row.names = FALSE, right = FALSE)

is_likert <- with(info, 类型 == "数值" & 最小 >= 0 & 最大 <= 11 & 取值个数 >= 3 & 取值个数 <= 11)
m <- regmatches(info$变量, regexec("^([A-Za-z]+[A-Za-z_]*?)_?([0-9]+)$", info$变量))
prefix <- vapply(m, function(z) if (length(z) == 3) z[2] else NA_character_, "")
grp <- split(info$变量[is_likert & !is.na(prefix)], prefix[is_likert & !is.na(prefix)])
grp <- grp[lengths(grp) >= 2]
points <- if (length(grp)) max(info$最大[info$变量 %in% unlist(grp)], na.rm = TRUE) else 5

rev_guess <- character()
for (k in names(grp)) {
  it <- grp[[k]]
  x <- as.data.frame(lapply(d[it], function(v) as.numeric(zap_labels(v))))
  x[x < 1 | x > points] <- NA
  for (j in it) {
    r <- suppressWarnings(stats::cor(x[[j]], rowMeans(x[setdiff(it, j)], na.rm = TRUE), use = "pairwise.complete.obs"))
    if (!is.na(r) && r < 0) rev_guess <- c(rev_guess, j)
  }
}
demo <- info$变量[!is_likert | is.na(prefix)]
demo <- demo[info$类型[match(demo, info$变量)] == "数值" & info$取值个数[match(demo, info$变量)] <= 10 &
               !info$变量[match(demo, info$变量)] %in% unlist(grp)]
id_guess <- info$变量[info$取值个数 == nrow(d) & info$类型 == "数值"][1]

cat("\n按变量名前缀识别出的量表：\n")
for (k in names(grp)) cat(sprintf("  %-8s %s\n", k, paste(grp[[k]], collapse = " ")))
if (length(rev_guess)) cat(sprintf("\n疑似反向题（与同组其他题负相关）：%s —— 请对照问卷原文确认\n", paste(rev_guess, collapse = ", ")))
too_long <- names(grp)[nchar(names(grp)) > 6]
if (length(too_long)) cat(sprintf("\n这些构念代码超过 6 个字符，需要在设定卡里改短：%s\n", paste(too_long, collapse = ", ")))

yl <- function(v) paste0("[", paste(v, collapse = ", "), "]")
L <- c(
  "# 设定卡草稿（由 draft_spec.R 生成）。所有 TODO 都要按研究设计改完再运行 run_sem.R。",
  "project: TODO 研究题目",
  sprintf("data: %s", basename(f)),
  if (!is.na(id_guess)) sprintf("id: %s", id_guess) else "# id: 问卷编号变量（可选）",
  sprintf("scale_points: %d                       # 李克特点数，请核对", as.integer(points)),
  sprintf("reverse_items: %s                 # TODO 对照问卷原文确认反向题", yl(rev_guess)),
  "missing: listwise",
  "drop_straightliners: true",
  sprintf("demographics: %s", yl(demo)),
  "",
  "constructs:                           # TODO label 改成中文构念名；构念代码 ≤ 6 个字母"
)
for (k in names(grp)) L <- c(L, sprintf("  %s: {label: %s, items: %s}", substr(k, 1, 6), k, yl(grp[[k]])))
L <- c(L, "",
  "structural:                           # TODO 因变量: [自变量, ...]，来自你的理论模型",
  "#  Y: [X, M]",
  "#  M: [X]",
  "",
  "# hypotheses:                         # 可选；不写就按 structural 自动编号 H1, H2, ...",
  "#   H1: X -> M",
  "",
  "# indirect:                           # 可选：具体间接效应",
  "#   H5: X -> M -> Y",
  "",
  "# multigroup: gender                  # 可选：多群组比较（2 组）",
  "# process:                            # 可选：PROCESS 模型 1/4/6/7/8/14",
  "#   - {model: 4, x: X, m: [M], y: Y}",
  "",
  "modifications: []                     # 先空着跑一遍，看 模型修正记录.md 再决定",
  "bootstrap: 2000",
  "process_bootstrap: 5000",
  "seed: 20261027")
writeLines(L, out, useBytes = TRUE)
cat(sprintf("\n设定卡草稿已写到：%s\n", out))
