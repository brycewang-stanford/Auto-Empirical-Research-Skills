# Write the AMOS side: VB.NET program bodies for the AMOS Program Editor, the
# simple user-defined estimands for specific indirect effects, and a drawing
# checklist for Amos Graphics with the numbers each AMOS table should show.
#
# Syntax follows the IBM SPSS Amos 28 User's Guide: "y <--- F (1)" fixes a
# path, "(label)" after a path names it, "a <> b" is a covariance, unique
# variables need explicit "(1)" paths, and in an Amos *program* (not Amos
# Graphics) exogenous variables other than unique variables are correlated by
# default. Estimands use the Example 38 form: `Name = p.Label * p.Label`.

amos_names <- function(items_by_construct, edges) {
  items <- unlist(items_by_construct, use.names = FALSE)
  err <- setNames(paste0("e", seq_along(items)), items)
  endo <- unique(edges$dv)
  dist <- setNames(paste0("d", seq_along(endo)), endo)
  list(err = err, dist = dist)
}

vb_body <- function(spec, items_by_construct, error_covs, edges, data_file, structural = TRUE) {
  nm <- amos_names(items_by_construct, edges)
  L <- c(
    "' ============================================================================",
    sprintf("' %s —— %s（由 spss-amos-sem 自动生成）", spec$project, if (structural) "结构模型" else "验证性因子分析 CFA"),
    "' 用法：开始菜单打开 IBM SPSS Amos Program Editor → File → New VB Program，",
    "'      把模板里 'Your code goes here 那一行整行替换成下面「从 Dim 到 End Try」的全部内容，",
    "'      再把 BeginGroup 里的路径改成你电脑上的文件，File → Run。",
    "' 注意：这份程序没有在真实 AMOS 里跑过，语法照 IBM Amos 28 用户手册的写法；",
    "'      如果报错，以 Amos Graphics 画图（AMOS操作步骤.md）为准。",
    "' ============================================================================",
    "Dim Sem As New AmosEngine",
    "Try",
    "    Sem.TextOutput()",
    "    Sem.Standardized()",
    "    Sem.Smc()",
    "    Sem.Mods(4)"
  )
  if (structural) {
    L <- c(L, "    Sem.TotalEffects()")
    if (length(spec$indirect)) L <- c(L, sprintf("    Sem.Bootstrap(%d)", as.integer(spec$bootstrap)))
  }
  L <- c(L, "", sprintf("    Sem.BeginGroup(\"C:\\改成你的文件夹路径\\%s\")", data_file), "")
  for (k in names(items_by_construct)) {
    it <- items_by_construct[[k]]
    L <- c(L, sprintf("    ' %s", spec$constructs[[k]]$label))
    for (j in seq_along(it)) {
      fix <- if (j == 1) " (1)" else ""
      L <- c(L, sprintf("    Sem.AStructure(\"%s <--- %s%s\")", it[j], k, fix))
    }
    for (j in seq_along(it)) L <- c(L, sprintf("    Sem.AStructure(\"%s <--- %s (1)\")", it[j], nm$err[[it[j]]]))
  }
  if (length(error_covs)) {
    L <- c(L, "", "    ' 误差相关（模型修正，理由见 模型修正记录.md）")
    for (p in error_covs) L <- c(L, sprintf("    Sem.AStructure(\"%s <> %s\")", nm$err[[p[1]]], nm$err[[p[2]]]))
  }
  if (structural && nrow(edges)) {
    L <- c(L, "", "    ' 结构路径（括号里是参数标签，自定义估计量要用）")
    for (i in seq_len(nrow(edges))) L <- c(L, sprintf("    Sem.AStructure(\"%s <--- %s (%s)\")", edges$dv[i], edges$iv[i], edges$label[i]))
    for (dv in names(nm$dist)) L <- c(L, sprintf("    Sem.AStructure(\"%s <--- %s (1)\")", dv, nm$dist[[dv]]))
    if (length(spec$controls)) {
      L <- c(L, "", "    ' 控制变量")
      for (dv in unique(edges$dv)) for (cv in spec$controls) L <- c(L, sprintf("    Sem.AStructure(\"%s <--- %s\")", dv, cv))
    }
  }
  L <- c(L, "", "    Sem.FitModel()", "Finally", "    Sem.Dispose()", "End Try")
  L
}

estimand_lines <- function(spec, edges) {
  vapply(names(spec$indirect), function(h) {
    p <- parse_arrow(spec$indirect[[h]])
    labs <- vapply(seq_len(length(p) - 1), function(i) edges$label[edges$iv == p[i] & edges$dv == p[i + 1]], character(1))
    sprintf("%s = %s", h, paste0("p.", labs, collapse = " * "))
  }, character(1))
}

write_lines_utf8 <- function(lines, path, bom = FALSE) {
  con <- file(path, open = "wb")
  on.exit(close(con))
  if (bom) writeBin(as.raw(c(0xEF, 0xBB, 0xBF)), con)
  writeBin(charToRaw(enc2utf8(paste0(paste(lines, collapse = "\r\n"), "\r\n"))), con)
}

write_amos_files <- function(spec, items_by_construct, error_covs, edges, dir, data_file, res) {
  dir.create(dir, showWarnings = FALSE, recursive = TRUE)
  write_lines_utf8(vb_body(spec, items_by_construct, error_covs, edges, data_file, structural = FALSE),
                   file.path(dir, "01_CFA_VB程序.vb"), bom = TRUE)
  if (nrow(edges)) {
    write_lines_utf8(vb_body(spec, items_by_construct, error_covs, edges, data_file, structural = TRUE),
                     file.path(dir, "02_SEM_VB程序.vb"), bom = TRUE)
  }
  if (length(spec$indirect)) write_lines_utf8(estimand_lines(spec, edges), file.path(dir, "03_自定义估计量.txt"))
  writeLines(amos_checklist(spec, items_by_construct, error_covs, edges, data_file, res),
             file.path(dir, "AMOS操作步骤.md"), useBytes = TRUE)
}

amos_checklist <- function(spec, items_by_construct, error_covs, edges, data_file, res) {
  nm <- amos_names(items_by_construct, edges)
  labels <- lapply(spec$constructs, `[[`, "label")
  f3 <- function(x) ifelse(is.na(x), "—", formatC(x, format = "f", digits = 3))
  exo <- setdiff(names(items_by_construct), unique(edges$dv))
  L <- c(
    sprintf("# AMOS 操作步骤：%s", spec$project), "",
    "> 由 spss-amos-sem 按你的设定卡生成。照着做完，AMOS 输出里的数字应该和下面「预期结果」一致到小数点后两位左右",
    "> （lavaan 已按 AMOS 的默认设置复算：ML 估计、每个构念第一条载荷固定为 1、卡方 = (N−1)×F）。", "",
    "## 0. 准备", "",
    sprintf("1. 先在 SPSS 里跑完 `analysis.sps`，得到清洗后的数据 `%s`（或直接用本文件夹上一级的同名文件，R 已经生成好了）。", data_file),
    "2. 打开 Amos Graphics → File → Data Files → File Name，选这个 .sav 文件 → OK。",
    "3. 数据里不能有缺失值（列表删除已在清洗步骤完成）；否则 AMOS 会要求勾选 Estimate means and intercepts。", "",
    "## 1. 画测量模型（CFA）", "",
    "用 **Draw a latent variable or add an indicator** 工具（带三个小方框的椭圆图标）：画一个椭圆，在里面点几下就加几个指标。", "",
    "| 构念（椭圆里写的变量名） | 中文名 | 指标（方框，从 List variables in data set 拖进来） | 误差项（小圆） |",
    "|---|---|---|---|"
  )
  for (k in names(items_by_construct)) {
    it <- items_by_construct[[k]]
    L <- c(L, sprintf("| `%s` | %s | %s | %s |", k, labels[[k]], paste0("`", it, "`", collapse = "、"), paste0("`", nm$err[it], "`", collapse = "、")))
  }
  L <- c(L, "",
         "- 每个构念的**第一条**载荷会被 AMOS 自动固定为 1，保持默认即可。",
         "- 误差项命名：Plugins → **Name Unobserved Variables** 会自动命名为 e1、e2……，为了和本文件对上，建议右键误差项 → Object Properties 手动改成上表的名字。",
         "- 椭圆的变量名必须和数据里的任何变量都不同（所以构念用代码，不要和题项同名）。")
  if (length(error_covs)) {
    L <- c(L, "- **模型修正**：用双箭头工具画以下误差相关（理由见 `模型修正记录.md`）：",
           vapply(error_covs, function(p) sprintf("  - `%s` ↔ `%s`（%s 与 %s 的误差）", nm$err[[p[1]]], nm$err[[p[2]]], p[1], p[2]), ""))
  }
  L <- c(L, "- **CFA 模型里所有构念两两之间都要画双箭头（协方差）**。Amos Graphics 不会自动让它们相关（这一点和 VB 程序不同）。", "",
         "## 2. 分析设置（View → Analysis Properties）", "",
         "- Estimation：Maximum likelihood（默认）。",
         "- Output：勾选 **Standardized estimates**、**Squared multiple correlations**、**Modification indices**（Threshold 保持 4）、**Indirect, direct & total effects**。",
         sprintf("- Bootstrap（做结构模型时）：勾选 **Perform bootstrap**，Number of bootstrap samples = **%d**；勾选 **Bias-corrected confidence intervals**，BC confidence level = **95**。", as.integer(spec$bootstrap)),
         "- SRMR：AMOS 默认不报。Plugins → **Standardized RMR**，先把这个小窗口打开放着，再点 Calculate Estimates，它才会显示。", "")
  cfa <- res$cfa_fit
  L <- c(L, "### CFA 的预期结果", "",
         "| 指标 | AMOS 里的位置 | 预期值 |", "|---|---|---|",
         sprintf("| χ² (CMIN) | Model Fit → CMIN | %s |", f3(cfa$chisq)),
         sprintf("| df | Model Fit → CMIN → DF | %d |", as.integer(cfa$df)),
         sprintf("| χ²/df (CMIN/DF) | Model Fit → CMIN | %s |", f3(cfa$chisq_df)),
         sprintf("| GFI / AGFI | Model Fit → RMR, GFI | %s / %s |", f3(cfa$gfi), f3(cfa$agfi)),
         sprintf("| NFI / IFI / TLI / CFI | Model Fit → Baseline Comparisons | %s / %s / %s / %s |", f3(cfa$nfi), f3(cfa$ifi), f3(cfa$tli), f3(cfa$cfi)),
         sprintf("| RMSEA | Model Fit → RMSEA | %s |", f3(cfa$rmsea)),
         sprintf("| SRMR | Standardized RMR 插件窗口 | %s |", f3(cfa$srmr)), "",
         "标准化载荷（Estimates → Scalars → Standardized Regression Weights）：", "",
         "| 题项 | 构念 | 标准化载荷 | C.R.（即 z 值） |", "|---|---|---|---|")
  ld <- res$loadings
  for (i in seq_len(nrow(ld))) L <- c(L, sprintf("| %s | %s | %s | %s |", ld$题项[i], ld$代码[i], f3(ld$标准化载荷[i]), if (is.na(ld$CR_z[i])) "固定为 1，不报" else f3(ld$CR_z[i])))
  L <- c(L, "", "> AMOS 的 **C.R.** 是 critical ratio（估计值 / 标准误，即 z 值），**不是**组合信度 CR。组合信度和 AVE 要用标准化载荷手算，本工具已算好，见 results.xlsx。", "")

  if (nrow(edges)) {
    L <- c(L, "## 3. 画结构模型", "",
           "在 CFA 图的基础上：",
           sprintf("1. **删掉**内生构念（%s）身上的双箭头，只保留外生构念之间的双箭头：%s。",
                   paste0("`", unique(edges$dv), "`", collapse = "、"),
                   if (length(exo) > 1) paste(combn(exo, 2, function(p) sprintf("`%s` ↔ `%s`", p[1], p[2])), collapse = "、") else "（只有一个外生构念，无需双箭头）"),
           "2. 用单箭头画结构路径，并给每条路径命名（右键箭头 → Object Properties → Parameters → Regression weight 填标签）：", "",
           "| 路径 | 参数标签 | 对应假设 |", "|---|---|---|")
    for (i in seq_len(nrow(edges))) {
      h <- names(spec$hypotheses)[vapply(spec$hypotheses, function(s) { p <- parse_arrow(s); p[1] == edges$iv[i] && p[2] == edges$dv[i] }, logical(1))]
      L <- c(L, sprintf("| `%s` → `%s` | `%s` | %s |", edges$iv[i], edges$dv[i], edges$label[i], if (length(h)) paste(h, collapse = "、") else "—"))
    }
    L <- c(L, "",
           sprintf("3. 给每个内生构念加残差项（Add a unique variable 工具），命名为：%s。", paste(sprintf("`%s` 的残差 `%s`", names(nm$dist), nm$dist), collapse = "；")))
    if (length(spec$controls)) L <- c(L, sprintf("4. 控制变量 %s 作为观测变量（方框）画单箭头指向每个内生构念，并和外生构念画双箭头。", paste0("`", spec$controls, "`", collapse = "、")))
    if (length(spec$indirect)) {
      L <- c(L, "", "### 具体间接效应（自定义估计量）", "",
             "AMOS 自带的 Indirect effects 只给「X 到 Y 所有间接路径的总和」。要分别检验每一条中介路径：", "",
             "1. 点 Amos Graphics 左下角状态栏的 **Not estimating any user-defined estimand** → **Define new estimands**。",
             "2. 在弹出的窗口里粘贴 `03_自定义估计量.txt` 的内容（每行一个间接效应，`p.` 表示参数标签）：", "", "```",
             estimand_lines(spec, edges), "```", "",
             "3. 点工具栏的 Check Syntax，看到 Syntax is OK 后关闭窗口并保存。",
             "4. 确认 Bootstrap 设置已勾选（见第 2 步），Calculate Estimates。",
             "5. 结果在 Text Output → Estimates → Scalars → **User-defined estimands**，点 **Bootstrap Confidence → Bias-corrected percentile method** 看 95% 置信区间。")
    }
    sf <- res$sem_fit
    L <- c(L, "", "### 结构模型的预期结果", "",
           sprintf("拟合：χ²/df = %s，CFI = %s，TLI = %s，RMSEA = %s，SRMR = %s。", f3(sf$chisq_df), f3(sf$cfi), f3(sf$tli), f3(sf$rmsea), f3(sf$srmr)), "",
           "| 假设 | 路径 | 标准化 β | 非标准化 b | S.E. | C.R. | P |", "|---|---|---|---|---|---|---|")
    pt <- res$paths
    for (i in seq_len(nrow(pt))) L <- c(L, sprintf("| %s | %s | %s | %s | %s | %s | %s |", pt$假设[i], pt$代码[i], f3(pt$标准化系数β[i]), f3(pt$非标准化系数[i]), f3(pt$SE[i]), f3(pt$CR_z[i]), fmt_p(pt$p[i])))
    if (!is.null(res$effects)) {
      sp <- res$effects$specific
      L <- c(L, "", "| 间接效应 | 估计值 | BC 95% CI |", "|---|---|---|")
      for (i in seq_len(nrow(sp))) L <- c(L, sprintf("| %s | %s | [%s, %s] |", sp$编号[i], f3(sp$效应值[i]), f3(sp$BC下限[i]), f3(sp$BC上限[i])))
      L <- c(L, "", "> Bootstrap 置信区间是随机重抽样得到的，AMOS 和 R 的随机数不同，上下限在第三位小数上有差别是正常的；判断显著与否应该一致。")
    }
  }
  if (!is.null(spec$multigroup)) {
    L <- c(L, "", "## 4. 多群组分析（可选）", "",
           sprintf("1. Analyze → Manage Groups：把 Group number 1 改名为第一组，点 New 建第二组（分组变量 `%s`）。", spec$multigroup),
           sprintf("2. File → Data Files：每一组都选同一个 .sav，点 Grouping Variable 选 `%s`，再点 Group Value 选这一组的取值。", spec$multigroup),
           "3. 点 **Multiple-Group Analysis** 按钮，AMOS 会自动生成 Unconstrained / Measurement weights / Structural weights 等嵌套模型，Model Fit 里比较 CFI 的变化（ΔCFI ≤ 0.01 视为等价成立）。",
           "4. 比较某条路径在两组间是否不同：Analysis Properties → Output 勾选 **Critical ratios for differences**，两组的同一路径命名不同标签后看两者差异的 C.R.（|C.R.| > 1.96 即 p < 0.05）。")
  }
  L
}
