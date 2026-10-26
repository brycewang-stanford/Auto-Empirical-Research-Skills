# Write the SPSS syntax (.sps) that reproduces the SPSS half of the pipeline.

sps_list <- function(v, per_line = 8) {
  chunks <- split(v, ceiling(seq_along(v) / per_line))
  paste(vapply(chunks, paste, character(1), collapse = " "), collapse = "\n    ")
}

recode_reverse <- function(v, k) {
  pairs <- paste0("(", seq_len(k), "=", rev(seq_len(k)), ")", collapse = " ")
  sprintf("RECODE %s %s.", v, pairs)
}

write_spss_syntax <- function(spec, items_by_construct, path, cleaned_name) {
  all_items <- unlist(lapply(spec$constructs, `[[`, "items"), use.names = FALSE)
  kept <- unlist(items_by_construct, use.names = FALSE)
  labels <- lapply(spec$constructs, `[[`, "label")
  ms <- paste0("m_", names(items_by_construct))
  L <- c(
    "* Encoding: UTF-8.",
    sprintf("* ============================================================================."),
    sprintf("* %s —— SPSS 部分（由 spss-amos-sem 自动生成）.", spec$project),
    "* 生成依据：设定卡里的构念、反向题、缺失值规则和模型修正。",
    "* 每一步的数字都能和 R 复算结果（results.xlsx）逐项对照。",
    "* ============================================================================.",
    "",
    "* ---- 第 0 步：把下面这一行改成数据所在的文件夹，然后 全选 → 运行 ----.",
    "CD 'C:\\改成你的文件夹路径'.",
    sprintf("GET FILE='%s'.", basename(spec$data)),
    "DATASET NAME raw WINDOW=FRONT.",
    "",
    "* 所有输出表格同时导出到 Excel，方便核对和交给 Claude 读取.",
    "OMS /SELECT TABLES /DESTINATION FORMAT=XLSX OUTFILE='spss_output_tables.xlsx' /TAG='aers_sem'.",
    ""
  )
  L <- c(L, "* ---- 第 1 步：超出量表范围的值（如 9 = 缺失代码）一律设为缺失 ----.",
         sprintf("RECODE %s (%d THRU %d=COPY) (ELSE=SYSMIS).", sps_list(all_items), 1, spec$scale_points),
         "EXECUTE.", "")
  if (isTRUE(spec$drop_straightliners)) {
    L <- c(L, "* ---- 第 2 步：剔除规律作答（所有题目答案完全一样，标准差为 0；必须在反向计分之前判断）----.",
           sprintf("COMPUTE sd_all = SD(%s).", paste(all_items, collapse = ", ")),
           "SELECT IF (MISSING(sd_all) OR sd_all > 0).",
           "EXECUTE.", "")
  }
  if (length(spec$reverse_items)) {
    L <- c(L, "* ---- 第 3 步：反向计分 ----.")
    L <- c(L, vapply(spec$reverse_items, recode_reverse, character(1), k = spec$scale_points), "EXECUTE.", "")
  }
  L <- c(L, "* ---- 第 4 步：缺失值 ----.")
  use_vars <- unique(c(all_items, spec$demographics, spec$controls, spec$multigroup, process_observed(spec)))
  if (spec$missing == "listwise") {
    L <- c(L, "* 列表删除：任何一个分析变量缺失的问卷都剔除（AMOS 默认要求完整数据）.",
           sprintf("COUNT n_miss = %s (MISSING).", sps_list(use_vars)),
           "SELECT IF (n_miss = 0).",
           "EXECUTE.")
  }
  if (!is.null(spec$id)) L <- c(L, "* 清洗后的有效样本量（看 N）.", sprintf("FREQUENCIES VARIABLES=%s /FORMAT=NOTABLE /STATISTICS=MINIMUM MAXIMUM.", spec$id))
  L <- c(L, "")
  if (length(spec$demographics)) {
    L <- c(L, "* ---- 第 5 步：样本人口统计特征 ----.",
           sprintf("FREQUENCIES VARIABLES=%s /ORDER=ANALYSIS.", sps_list(spec$demographics)), "")
  }
  L <- c(L, "* ---- 第 6 步：题项描述统计与正态性（|偏度| < 3、|峰度| < 10 可视为近似正态，Kline 2016）----.",
         sprintf("DESCRIPTIVES VARIABLES=%s\n  /STATISTICS=MEAN STDDEV MIN MAX KURTOSIS SKEWNESS.", sps_list(kept)), "")
  L <- c(L, "* ---- 第 7 步：共同方法偏差 —— Harman 单因素检验（未旋转，看第一个因子的方差解释率）----.",
         sprintf("FACTOR\n  /VARIABLES %s\n  /MISSING LISTWISE\n  /PRINT INITIAL EXTRACTION\n  /CRITERIA MINEIGEN(1) ITERATE(25)\n  /EXTRACTION PC\n  /ROTATION NOROTATE\n  /METHOD=CORRELATION.", sps_list(kept)), "")
  L <- c(L, "* ---- 第 8 步：信度分析（每个构念一次）----.")
  for (k in names(items_by_construct)) {
    L <- c(L, sprintf("RELIABILITY\n  /VARIABLES=%s\n  /SCALE('%s') ALL\n  /MODEL=ALPHA\n  /STATISTICS=DESCRIPTIVE SCALE\n  /SUMMARY=TOTAL.",
                      sps_list(items_by_construct[[k]]), labels[[k]]))
  }
  L <- c(L, "")
  rot <- toupper(spec$efa_rotation)
  if (rot == "PROMAX") rot <- "PROMAX(4)"
  L <- c(L, "* ---- 第 9 步：探索性因子分析（KMO、Bartlett、旋转后载荷）----.",
         sprintf("FACTOR\n  /VARIABLES %s\n  /MISSING LISTWISE\n  /PRINT INITIAL KMO EXTRACTION ROTATION\n  /FORMAT SORT BLANK(.40)\n  /CRITERIA FACTORS(%d) ITERATE(25)\n  /EXTRACTION PC\n  /CRITERIA ITERATE(25)\n  /ROTATION %s\n  /METHOD=CORRELATION.",
                 sps_list(kept), length(items_by_construct), rot), "")
  L <- c(L, "* ---- 第 10 步：计算各构念均值（变量名 m_构念代码，供相关分析和 PROCESS 使用）----.")
  for (i in seq_along(ms)) {
    k <- names(items_by_construct)[i]
    L <- c(L, sprintf("COMPUTE %s = MEAN(%s).", ms[i], paste(items_by_construct[[k]], collapse = ", ")),
           sprintf("VARIABLE LABELS %s '%s'.", ms[i], labels[[k]]))
  }
  L <- c(L, "EXECUTE.", "")
  L <- c(L, "* ---- 第 11 步：描述统计与 Pearson 相关 ----.",
         sprintf("CORRELATIONS\n  /VARIABLES=%s\n  /PRINT=TWOTAIL NOSIG\n  /STATISTICS DESCRIPTIVES\n  /MISSING=PAIRWISE.", sps_list(ms)), "")
  edges <- structural_edges(spec)
  if (nrow(edges)) {
    L <- c(L, "* ---- 第 12 步：多重共线性诊断（VIF < 5，越接近 1 越好）----.")
    for (dv in unique(edges$dv)) {
      ivs <- paste0("m_", edges$iv[edges$dv == dv])
      if (length(ivs) > 1) L <- c(L, sprintf("REGRESSION\n  /STATISTICS COEFF R ANOVA COLLIN TOL\n  /DEPENDENT m_%s\n  /METHOD=ENTER %s.", dv, paste(ivs, collapse = " ")))
    }
    L <- c(L, "")
  }
  L <- c(L, "* ---- 第 13 步：保存清洗后的数据，AMOS 直接读这个文件 ----.",
         sprintf("SAVE OUTFILE='%s'\n  /COMPRESSED.", cleaned_name), "")
  if (length(spec$process)) {
    L <- c(L, "* ---- 第 14 步：PROCESS 中介 / 调节（需要先安装 Hayes 的 PROCESS v4 宏）----.",
           "* 安装：到 processmacro.org 下载，打开 process.sps 全选运行一次（每次打开 SPSS 都要运行一次），",
           "* 或者用 扩展 → 实用程序 → 安装定制对话框 安装 process.spd。下面的命令在宏定义之后才能运行.",
           "* INSERT FILE='process.sps'.")
    pv <- function(v) ifelse(v %in% names(spec$constructs), paste0("m_", v), v)
    for (p in spec$process) {
      opts <- c(sprintf("y=%s", pv(p$y)), sprintf("x=%s", pv(p$x)))
      if (!is.null(p[["m"]])) opts <- c(opts, sprintf("m=%s", paste(pv(unlist(p[["m"]])), collapse = " ")))
      if (!is.null(p$w)) opts <- c(opts, sprintf("w=%s", pv(p$w)))
      if (length(unlist(p$covariates))) opts <- c(opts, sprintf("cov=%s", paste(unlist(p$covariates), collapse = " ")))
      opts <- c(opts, sprintf("model=%s", p$model), sprintf("boot=%d", as.integer(spec$process_bootstrap)), sprintf("seed=%d", as.integer(spec$seed)))
      if (p$model %in% c(4, 6)) opts <- c(opts, "total=1")
      if (p$model %in% c(1, 7, 8, 14) && isTRUE(p$center %||% TRUE)) opts <- c(opts, "center=1")
      if (p$model == 1) opts <- c(opts, "jn=1")
      L <- c(L, paste0("process ", paste(opts, collapse = "/"), "."))
    }
    L <- c(L, "")
  }
  L <- c(L, "OMSEND TAG=['aers_sem'].", "* 完成。接下来按 amos/AMOS操作步骤.md 在 AMOS 里做 CFA 和结构模型.")
  # an SPSS comment runs until a line ends with a period
  L <- unlist(strsplit(L, "\n", fixed = TRUE))
  com <- grepl("^\\*", L) & !grepl("\\.$", L)
  L[com] <- paste0(sub("[。．]$", "", L[com]), ".")
  con <- file(path, open = "w", encoding = "UTF-8")
  on.exit(close(con))
  writeLines(L, con)
  invisible(path)
}
