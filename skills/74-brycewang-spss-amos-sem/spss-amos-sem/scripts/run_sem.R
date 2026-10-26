#!/usr/bin/env Rscript
# 问卷数据结构方程全流程（SPSS + AMOS），lavaan 复算 + 自动出 SPSS 语法 / AMOS 程序 / 论文表格。
#
#   Rscript scripts/run_sem.R <spec.yml> [--out DIR] [--quick]
#
#   --out    输出文件夹（默认：设定卡同目录下的 sem_output/）
#   --quick  bootstrap 只跑 200 次，用来先检查设定卡和数据；正式结果不要用

local({
  need <- c("yaml", "lavaan", "semTools", "psych", "GPArotation", "haven", "openxlsx", "officer", "flextable", "jsonlite")
  miss <- need[!vapply(need, requireNamespace, logical(1), quietly = TRUE)]
  if (length(miss)) {
    stop(sprintf("缺少 R 包：%s\n请先运行：install.packages(c(%s))", paste(miss, collapse = ", "),
                 paste0('"', miss, '"', collapse = ", ")), call. = FALSE)
  }
})

script_path <- normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1]))
SKILL_DIR <- dirname(dirname(script_path))
for (f in c("io.R", "measure.R", "cfa_sem.R", "process.R", "gen_spss.R", "gen_amos.R", "report.R"))
  source(file.path(SKILL_DIR, "scripts", "R", f), encoding = "UTF-8")

args <- commandArgs(trailingOnly = TRUE)
if (!length(args) || args[1] %in% c("-h", "--help")) {
  cat("用法：Rscript scripts/run_sem.R <spec.yml> [--out DIR] [--quick]\n"); quit(status = 0)
}
spec <- read_spec(args[1])
out_dir <- if ("--out" %in% args) args[which(args == "--out") + 1] else file.path(spec$.dir, "sem_output")
quick <- "--quick" %in% args
if (quick) { spec$bootstrap <- min(spec$bootstrap, 200); spec$process_bootstrap <- min(spec$process_bootstrap, 200) }
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
say <- function(...) cat(sprintf(...), "\n", sep = "")

say("[1/9] 读取数据：%s", spec$data)
raw <- read_raw(spec)
cl <- clean_data(spec, raw)
df <- cl$data
labels <- lapply(spec$constructs, `[[`, "label")
items <- active_items(spec)
ecs <- error_covs_of(spec$modifications)
edges <- structural_edges(spec)
say("      回收 %d 份 → 有效 %d 份", cl$log$n_raw, cl$log$n_used)

res <- list(labels = labels, items = items, clean_log = cl$log, spec_path = spec$.path, quick = quick)

say("[2/9] 人口统计、描述统计、Harman 单因素")
if (length(spec$demographics)) {
  vl <- setNames(lapply(spec$demographics, function(v) attr(raw[[v]], "label") %||% v), spec$demographics)
  res$demographics <- demographics_table(df, spec$demographics, vl)
}
res$item_desc <- item_descriptives(df, items, labels, cl$item_labels)
res$harman <- harman_test(df, unlist(items))

say("[3/9] 信度（Cronbach's α、CITC）与探索性因子分析")
res$reliability <- reliability_table(df, items, labels)
res$efa <- efa_analysis(df, items, labels, spec$efa_rotation)

say("[4/9] 验证性因子分析（逐步记录模型修正）")
ms <- modification_steps(spec, df)
res$mod_steps <- ms
res$initial_loadings <- loadings_table(ms$initial_fit, labels)
cfa <- fit_cfa(spec, df, items, ecs)
res$cfa_obj <- cfa
res$cfa_fit <- fit_indices(cfa)
res$loadings <- loadings_table(cfa, labels)
res$validity <- validity_table(res$loadings, labels)
res$fornell <- fornell_larcker(cfa, res$validity)
res$htmt <- htmt_matrix(df, items)
res$mod_suggest <- mod_suggestions(cfa, items)
res$cmb <- cmb_single_factor(spec, df, items, ecs, cfa)
scores <- mean_scores(df, items)
res$pearson <- pearson_table(scores, labels, res$validity$sqrtAVE[match(names(items), res$validity$代码)])

if (nrow(edges)) {
  say("[5/9] 结构模型%s", if (length(spec$indirect)) sprintf("（bootstrap %d 次，需要一点时间）", as.integer(spec$bootstrap)) else "")
  sm <- fit_sem(spec, df, items, ecs, edges, boot = if (length(spec$indirect)) spec$bootstrap else 0)
  res$sem_obj <- sm$fit
  res$sem_fit <- fit_indices(sm$fit)
  res$paths <- path_table(sm$fit, spec, edges, labels)
  res$r2 <- r2_table(sm$fit, labels)
  if (length(spec$indirect)) res$effects <- effects_tables(sm, spec, edges, labels)
  res$sem_syntax <- sm$syntax
} else say("[5/9] 设定卡没有 structural，跳过结构模型")

if (!is.null(spec$multigroup)) {
  say("[6/9] 多群组：测量不变性与路径差异（%s）", spec$multigroup)
  res$multigroup <- if (nrow(edges)) multigroup_analysis(spec, df, items, ecs, edges) else NULL
  if (!is.null(res$multigroup$var)) res$multigroup$var_label <- attr(raw[[spec$multigroup]], "label") %||% spec$multigroup
} else say("[6/9] 无多群组分析")

if (length(spec$process)) {
  say("[7/9] PROCESS 模型（%s，bootstrap %d 次）", paste(vapply(spec$process, function(p) as.character(p$model), ""), collapse = "/"), as.integer(spec$process_bootstrap))
  pdata <- process_data(spec, raw, df, scores)
  res$var_labels <- setNames(lapply(process_observed(spec), function(v) attr(raw[[v]], "label") %||% v), process_observed(spec))
  res$process <- lapply(spec$process, function(p) process_model(p, pdata, spec$process_bootstrap, spec$seed))
} else say("[7/9] 无 PROCESS 模型")

say("[8/9] 生成 SPSS 语法、AMOS 程序与清洗后数据")
stem <- tools::file_path_sans_ext(basename(spec$data))
cleaned_name <- paste0(stem, "_cleaned.sav")
exp <- df[c(spec$id, unlist(lapply(spec$constructs, `[[`, "items"), use.names = FALSE))]
for (v in unique(c(spec$demographics, spec$multigroup, spec$controls))) {
  rawv <- raw[[v]]
  if (inherits(rawv, "haven_labelled")) {
    lab <- attr(rawv, "labels"); code <- unname(lab[match(df[[v]], names(lab))])
    exp[[v]] <- haven::labelled(code, lab, label = attr(rawv, "label"))
  } else exp[[v]] <- utils::type.convert(as.character(df[[v]]), as.is = TRUE)
}
for (k in names(items)) exp[[paste0("m_", k)]] <- scores[[k]]
haven::write_sav(exp, file.path(out_dir, cleaned_name))
write_spss_syntax(spec, items, file.path(out_dir, "analysis.sps"), cleaned_name)
write_amos_files(spec, items, ecs, edges, file.path(out_dir, "amos"), cleaned_name, res)
writeLines(c("# lavaan 模型（与 AMOS 设定一致）", "# 测量模型", attr(cfa, "syntax"), "", "# 结构模型", res$sem_syntax %||% ""),
           file.path(out_dir, "lavaan_model.txt"), useBytes = TRUE)

say("[9/9] 输出表格、段落与路径图")
fig <- NULL
if (nrow(edges)) { fig <- file.path(out_dir, "路径图.png"); draw_path_diagram(res, spec, edges, fig) }
res$fit_rows <- fit_rows(res$cfa_fit, res$sem_fit)
build_docx(res, spec, file.path(out_dir, "结果表格.docx"), fig)
write_paragraphs(res, spec, file.path(out_dir, "结果段落.md"))
write_mod_record(res, spec, file.path(out_dir, "模型修正记录.md"))

mod_tab <- do.call(rbind, lapply(ms$steps, function(s) data.frame(步骤 = s$step, 修正内容 = s$detail, 理由 = s$reason, 数据依据 = s$evidence,
  chisq = s$fit$chisq, df = s$fit$df, chisq_df = s$fit$chisq_df, CFI = s$fit$cfi, TLI = s$fit$tli, RMSEA = s$fit$rmsea, SRMR = s$fit$srmr)))
fit_tab <- data.frame(指标 = names(res$cfa_fit), 测量模型 = unlist(res$cfa_fit), 结构模型 = if (!is.null(res$sem_fit)) unlist(res$sem_fit[names(res$cfa_fit)]) else NA)
sheets <- list(
  "01_清洗记录" = data.frame(项目 = c("回收问卷", "超出量表范围的取值（设为缺失）", "规律作答", "存在缺失的问卷", "有效问卷"),
                             数量 = c(cl$log$n_raw, cl$log$out_of_range, cl$log$straightliners, cl$log$incomplete, cl$log$n_used)),
  "02_人口统计" = res$demographics, "03_题项描述统计" = res$item_desc,
  "04_Harman" = data.frame(成分 = seq_along(res$harman$eigen), 特征值 = res$harman$eigen, 方差百分比 = res$harman$pct),
  "05_信度" = res$reliability, "06_EFA_初始特征值" = res$efa$initial, "07_EFA_旋转后载荷" = res$efa$loadings,
  "08_CFA_载荷" = res$loadings, "09_CR_AVE" = res$validity,
  "10_相关与AVE" = data.frame(构念 = names(scores), 均值 = res$pearson$mean, 标准差 = res$pearson$sd, round(res$pearson$r, 4), check.names = FALSE),
  "11_FL准则_潜变量相关" = data.frame(构念 = rownames(res$fornell$matrix), res$fornell$matrix, check.names = FALSE),
  "12_HTMT" = data.frame(构念 = rownames(res$htmt), res$htmt, check.names = FALSE),
  "13_拟合指标" = fit_tab, "14_模型修正步骤" = mod_tab, "15_修正指数" = res$mod_suggest,
  "16_路径系数" = res$paths, "17_R2" = res$r2,
  "18_具体间接效应" = res$effects$specific, "19_效应分解" = res$effects$decomposition,
  "20_测量不变性" = res$multigroup$invariance, "21_路径组间差异" = res$multigroup$paths
)
for (i in seq_along(res$process)) {
  pr <- res$process[[i]]
  sheets[[sprintf("P%d_模型%d_系数", i, pr$model)]] <- pr$coefs
  sheets[[sprintf("P%d_模型%d_效应", i, pr$model)]] <- pr$effects
}
write_xlsx(sheets, file.path(out_dir, "results.xlsx"))

summary_json <- list(
  project = spec$project, generated = format(Sys.time(), "%Y-%m-%d %H:%M"), quick_mode = quick,
  sample = cl$log, harman_first_factor_pct = res$harman$first_pct,
  alpha = setNames(as.list(res$reliability$Cronbachα[!duplicated(res$reliability$代码)]), unique(res$reliability$代码)),
  kmo = res$efa$kmo, efa_cum_pct = res$efa$cum_pct, efa_flags = res$efa$flags,
  cfa_fit = res$cfa_fit, cr_ave = res$validity, fornell_larcker_pass = as.list(res$fornell$pass),
  htmt_max = max(res$htmt[lower.tri(res$htmt)]),
  sem_fit = res$sem_fit, paths = res$paths, r2 = res$r2,
  indirect = res$effects$specific, effect_decomposition = res$effects$decomposition,
  multigroup = res$multigroup[c("invariance", "paths", "skipped")],
  process = lapply(res$process, function(p) list(model = p$model, x = p$x, m = p[["m"]], y = p$y, w = p$w, effects = p$effects)),
  modifications = lapply(ms$steps, function(s) list(step = s$step, detail = s$detail, reason = s$reason, evidence = s$evidence, cfi = s$fit$cfi, rmsea = s$fit$rmsea)),
  files = c("results.xlsx", "结果表格.docx", "结果段落.md", "模型修正记录.md", "路径图.png", "analysis.sps", cleaned_name,
            "amos/AMOS操作步骤.md", "amos/01_CFA_VB程序.vb", "amos/02_SEM_VB程序.vb", "amos/03_自定义估计量.txt", "lavaan_model.txt")
)
jsonlite::write_json(summary_json, file.path(out_dir, "results.json"), auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null")
say("完成 → %s%s", normalizePath(out_dir), if (quick) "（--quick 模式：bootstrap 次数不足，不能当正式结果）" else "")
