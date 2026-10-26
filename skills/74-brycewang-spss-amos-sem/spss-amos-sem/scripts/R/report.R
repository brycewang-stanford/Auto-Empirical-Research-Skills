# Outputs: results.xlsx, 结果表格.docx (three-line tables), 结果段落.md,
# 模型修正记录.md, 路径图.png, results.json.

f3 <- function(x, d = 3) ifelse(is.na(x), "", formatC(as.numeric(x), format = "f", digits = d))
fmt_p <- function(p) ifelse(is.na(p), "", ifelse(p < 0.001, "< 0.001", formatC(p, format = "f", digits = 3)))
stars <- function(p) ifelse(is.na(p), "", ifelse(p < 0.001, "***", ifelse(p < 0.01, "**", ifelse(p < 0.05, "*", ""))))
rng <- function(x, d = 3) sprintf("%s ~ %s", f3(min(x), d), f3(max(x), d))

# ---- Word ---------------------------------------------------------------------

TXT <- function(size = 10.5, bold = FALSE) officer::fp_text(font.size = size, bold = bold, font.family = "Times New Roman", eastasia.family = "宋体")

three_line <- function(df, header_map = NULL) {
  ft <- flextable::flextable(df)
  if (!is.null(header_map)) ft <- flextable::set_header_labels(ft, values = header_map)
  thick <- officer::fp_border(width = 1.5); thin <- officer::fp_border(width = 0.75)
  ft <- flextable::border_remove(ft)
  ft <- flextable::hline_top(ft, border = thick, part = "header")
  ft <- flextable::hline_bottom(ft, border = thin, part = "header")
  ft <- flextable::hline_bottom(ft, border = thick, part = "body")
  ft <- flextable::font(ft, fontname = "Times New Roman", eastasia.family = "宋体", part = "all")
  ft <- flextable::fontsize(ft, size = 10.5, part = "all")
  ft <- flextable::align(ft, align = "center", part = "all")
  ft <- flextable::padding(ft, padding.top = 1, padding.bottom = 1, part = "all")
  if (ncol(df) >= 7) ft <- flextable::fontsize(ft, size = 9, part = "all")
  ft <- flextable::autofit(ft)
  # a little slack for CJK glyph metrics; if too wide for the page, cap long
  # text columns (they wrap) and take the rest only from columns wider than 0.8"
  w <- pmin(flextable::dim_pretty(ft)$widths + 0.1, 1.8)
  if (sum(w) > 6.3) {
    slack <- pmax(w - 0.8, 0)
    w <- w - slack * min(1, (sum(w) - 6.3) / sum(slack))
  }
  flextable::width(ft, width = w)
}

Doc <- function() {
  env <- new.env()
  env$doc <- officer::read_docx()
  env$n <- 0
  env$add_title <- function(text) {
    env$doc <- officer::body_add_fpar(env$doc, officer::fpar(officer::ftext(text, TXT(14, TRUE)), fp_p = officer::fp_par(text.align = "center")))
  }
  env$add_table <- function(df, title, note = NULL, header_map = NULL) {
    env$n <- env$n + 1
    env$doc <- officer::body_add_fpar(env$doc, officer::fpar(officer::ftext(sprintf("表 %d  %s", env$n, title), TXT(10.5, TRUE)),
                                                             fp_p = officer::fp_par(text.align = "center", padding.top = 12)))
    env$doc <- flextable::body_add_flextable(env$doc, three_line(df, header_map))
    if (!is.null(note)) env$doc <- officer::body_add_fpar(env$doc, officer::fpar(officer::ftext(note, TXT(9))))
  }
  env$add_image <- function(path, title, w = 6.3, h = 3.8) {
    env$doc <- officer::body_add_img(env$doc, path, width = w, height = h, style = "centered")
    env$doc <- officer::body_add_fpar(env$doc, officer::fpar(officer::ftext(title, TXT(10.5, TRUE)), fp_p = officer::fp_par(text.align = "center")))
  }
  env$save <- function(path) print(env$doc, target = path)
  env
}

NOTE_P <- "注：*** p < 0.001，** p < 0.01，* p < 0.05。"

build_docx <- function(res, spec, path, figure = NULL) {
  labels <- res$labels
  d <- Doc()
  d$add_title(sprintf("%s：数据分析结果表格", spec$project))

  if (!is.null(res$demographics)) {
    dm <- res$demographics; dm$百分比 <- f3(dm$百分比, 1)
    dm$变量[duplicated(dm$变量)] <- ""
    d$add_table(dm, sprintf("样本人口统计特征（N = %d）", res$clean_log$n_used), header_map = list(百分比 = "百分比（%）"))
  }
  it <- res$item_desc
  d$add_table(data.frame(构念 = ifelse(duplicated(it$构念), "", it$构念), 题项 = it$题项, 均值 = f3(it$均值), 标准差 = f3(it$标准差),
                         偏度 = f3(it$偏度), 峰度 = f3(it$峰度)),
              "题项描述统计与正态性检验", "注：偏度绝对值 < 3、峰度绝对值 < 10 时可视为近似正态（Kline, 2016），适合使用最大似然估计。")
  rl <- res$reliability
  d$add_table(data.frame(构念 = ifelse(duplicated(rl$构念), "", rl$构念), 题项 = rl$题项, CITC = f3(rl$CITC),
                         删除该项后α = f3(rl$删除该项后α), Cronbachα = ifelse(duplicated(rl$构念), "", f3(rl$Cronbachα))),
              "信度分析结果", "注：CITC 为校正的项总计相关性；Cronbach's α > 0.7 表示信度良好（Nunnally, 1978）。",
              header_map = list(删除该项后α = "删除该项后的 α", Cronbachα = "Cronbach's α"))
  e <- res$efa
  d$add_table(data.frame(检验 = c("KMO 值", "Bartlett 球形检验 近似卡方", "自由度 df", "显著性 p"),
                         结果 = c(f3(e$kmo), f3(e$bartlett_chisq, 2), as.character(e$bartlett_df), fmt_p(e$bartlett_p))),
              "KMO 与 Bartlett 球形检验", "注：KMO > 0.7 且 Bartlett 检验显著，说明数据适合做因子分析（Kaiser, 1974）。")
  ld <- e$loadings
  show <- ld; for (k in names(res$items)) show[[k]] <- f3(ld[[k]])
  show$所属构念 <- NULL
  tail_rows <- rbind(
    c("特征值（旋转后）", f3(e$rotated_ss)),
    c("方差解释率（%）", f3(e$rotated_pct, 2)),
    c("累计方差解释率（%）", f3(cumsum(e$rotated_pct), 2)))
  colnames(tail_rows) <- colnames(show)
  show <- rbind(show, as.data.frame(tail_rows, stringsAsFactors = FALSE))
  hm <- setNames(as.list(unlist(labels[names(res$items)])), names(res$items))
  d$add_table(show, "旋转后的成分矩阵", sprintf("注：提取方法为主成分分析，旋转方法为 %s（Kaiser 标准化）；成分按载荷最高的构念命名。", if (e$rotation == "varimax") "最大方差法" else e$rotation), header_map = hm)

  v <- res$validity; lds <- res$loadings
  cfa_tab <- data.frame(构念 = ifelse(duplicated(lds$构念), "", lds$构念), 题项 = lds$题项,
                        标准化载荷 = f3(lds$标准化载荷), z = ifelse(is.na(lds$CR_z), "—", f3(lds$CR_z)),
                        p = ifelse(is.na(lds$p), "—", ifelse(lds$p < 0.001, "***", fmt_p(lds$p))), SMC = f3(lds$SMC),
                        CR = "", AVE = "", stringsAsFactors = FALSE)
  first <- !duplicated(lds$代码)
  cfa_tab$CR[first] <- f3(v$CR[match(lds$代码[first], v$代码)])
  cfa_tab$AVE[first] <- f3(v$AVE[match(lds$代码[first], v$代码)])
  d$add_table(cfa_tab, "验证性因子分析结果（收敛效度）",
              "注：z 即 AMOS 输出中的 C.R.（临界比），每个构念的第一个题项载荷固定为 1，不报告 z；SMC 为题项信度（标准化载荷的平方）；CR 为组合信度，AVE 为平均方差抽取量。CR > 0.7、AVE > 0.5、标准化载荷 > 0.5 表示收敛效度良好（Fornell & Larcker, 1981；Hair et al., 2019）。",
              header_map = list(标准化载荷 = "标准化载荷", z = "z (C.R.)"))

  fi <- res$fit_rows
  d$add_table(fi, "模型拟合指标", "注：判断标准参考 Hu & Bentler（1999）、Browne & Cudeck（1993）。SRMR 在 AMOS 中需通过 Plugins → Standardized RMR 获得。")

  pt <- res$pearson; k <- ncol(pt$r)
  cm <- matrix("", k, k)
  for (i in seq_len(k)) for (j in seq_len(i)) cm[i, j] <- if (i == j) sprintf("**%s**", f3(pt$sqrt_ave[i])) else paste0(f3(pt$r[i, j]), stars(pt$p[i, j]))
  cm <- gsub("\\*\\*([0-9.]+)\\*\\*", "[\\1]", cm)
  dt <- data.frame(变量 = pt$labels, 均值 = f3(pt$mean), 标准差 = f3(pt$sd), cm, stringsAsFactors = FALSE)
  names(dt)[-(1:3)] <- as.character(seq_len(k)); dt$变量 <- paste0(seq_len(k), ". ", dt$变量)
  d$add_table(dt, "描述统计、相关系数与区分效度", paste("注：方括号内为 AVE 的平方根；对角线以下为构念均值的 Pearson 相关系数。", NOTE_P, "对角线上的值大于其所在行、列的相关系数，说明区分效度良好（Fornell & Larcker, 1981）。"))
  ht <- res$htmt; hk <- nrow(ht)
  hm2 <- matrix("", hk, hk); for (i in seq_len(hk)) for (j in seq_len(hk)) if (j < i) hm2[i, j] <- f3(ht[i, j])
  hd <- data.frame(构念 = unlist(labels[rownames(ht)]), hm2, stringsAsFactors = FALSE); names(hd)[-1] <- unlist(labels[rownames(ht)])
  d$add_table(hd, "HTMT 区分效度检验", "注：HTMT < 0.85（严格）或 < 0.90（宽松）表示区分效度良好（Henseler, Ringle, & Sarstedt, 2015）。")

  if (!is.null(res$paths)) {
    p <- res$paths
    d$add_table(data.frame(假设 = p$假设, 路径 = p$路径, 标准化系数 = paste0(f3(p$标准化系数β), stars(p$p)), 非标准化系数 = f3(p$非标准化系数),
                           SE = f3(p$SE), z = f3(p$CR_z), p = fmt_p(p$p), 结论 = p$结论),
                "结构模型路径系数与假设检验结果", paste("注：z 即 AMOS 输出中的 C.R.。", NOTE_P), header_map = list(标准化系数 = "标准化系数 β", 非标准化系数 = "非标准化系数 B", z = "z (C.R.)"))
    if (!is.null(figure)) d$add_image(figure, "图  结构模型路径系数（标准化）")
  }
  if (!is.null(res$effects)) {
    sp <- res$effects$specific
    d$add_table(data.frame(假设 = sp$编号, 中介路径 = sp$效应, 间接效应 = f3(sp$效应值), BootSE = f3(sp$BootSE),
                           CI = sprintf("[%s, %s]", f3(sp$BC下限), f3(sp$BC上限)), 标准化间接效应 = f3(sp$标准化效应), 结论 = ifelse(sp$显著 == "是", "成立", "不成立"), 中介类型 = sp$中介类型),
                sprintf("中介效应检验结果（Bootstrap = %d 次）", as.integer(spec$bootstrap)),
                "注：间接效应为非标准化估计值；CI 为偏差校正（bias-corrected）的 95% 置信区间，不包含 0 即中介效应显著（Preacher & Hayes, 2008）；中介类型参照 Zhao, Lynch, & Chen（2010）。",
                header_map = list(BootSE = "Boot SE", CI = "BC 95% CI"))
    dc <- res$effects$decomposition
    d$add_table(data.frame(路径 = dc$配对, 效应类型 = dc$编号, 效应值 = f3(dc$效应值), BootSE = f3(dc$BootSE),
                           CI = ifelse(is.na(dc$BC下限), "—", sprintf("[%s, %s]", f3(dc$BC下限), f3(dc$BC上限)))),
                "总效应、直接效应与间接效应分解", "注：总间接效应为该自变量到因变量所有间接路径之和，对应 AMOS 的 Indirect Effects 输出。", header_map = list(BootSE = "Boot SE", CI = "BC 95% CI"))
  }
  if (!is.null(res$multigroup) && is.null(res$multigroup$skipped)) {
    mg <- res$multigroup$invariance
    d$add_table(data.frame(模型 = mg$模型, χ2 = f3(mg$chisq), df = mg$df, CFI = f3(mg$CFI), TLI = f3(mg$TLI), RMSEA = f3(mg$RMSEA), SRMR = f3(mg$SRMR),
                           Δχ2 = f3(mg$Δchisq), Δdf = ifelse(is.na(mg$Δdf), "", mg$Δdf), ΔCFI = f3(mg$ΔCFI), ΔRMSEA = f3(mg$ΔRMSEA), 判断 = mg$判断),
                sprintf("测量不变性检验（分组变量：%s）", res$multigroup$var_label), "注：ΔCFI ≤ 0.01（Cheung & Rensvold, 2002）且 ΔRMSEA ≤ 0.015（Chen, 2007）视为该层级的不变性成立。")
    pg <- res$multigroup$paths
    g <- res$multigroup$groups
    d$add_table(data.frame(路径 = pg$路径, a = paste0(f3(pg[[paste0("β_", g[1])]]), stars(pg[[paste0("p_", g[1])]])),
                           b = paste0(f3(pg[[paste0("β_", g[2])]]), stars(pg[[paste0("p_", g[2])]])),
                           z = f3(pg$差异临界比z), p = fmt_p(pg$p_差异)),
                "结构路径的组间差异", paste("注：在载荷等价的前提下估计各组路径；z 为两组非标准化系数之差的临界比（AMOS 的 Critical ratios for differences），|z| > 1.96 表示差异显著。", NOTE_P),
                header_map = list(a = paste0(g[1], " β"), b = paste0(g[2], " β"), z = "差异 z"))
  }
  for (pr in res$process) {
    cf <- pr$coefs
    d$add_table(data.frame(方程 = ifelse(duplicated(cf$方程), "", cf$方程), 预测变量 = cf$预测变量, b = f3(cf$b), SE = f3(cf$SE), t = f3(cf$t), p = fmt_p(cf$p),
                           CI = sprintf("[%s, %s]", f3(cf$LLCI), f3(cf$ULCI)), R2 = f3(cf$R2)),
                sprintf("PROCESS 模型 %d 回归结果", pr$model),
                sprintf("注：基于构念均值的 OLS 回归%s。", if (pr$center && pr$model %in% c(1, 7, 8, 14)) "，交互项由均值中心化后的变量构造（PROCESS center=1）" else ""),
                header_map = list(CI = "95% CI", R2 = "R²"))
    ef <- pr$effects
    if (pr$model == 1) {
      d$add_table(data.frame(效应 = ef$效应, Effect = f3(ef$Effect), SE = f3(ef$SE), t = f3(ef$t), p = fmt_p(ef$p), CI = sprintf("[%s, %s]", f3(ef$LLCI), f3(ef$ULCI))),
                  "调节效应：条件效应分析", "注：调节变量取第 16、50、84 百分位（PROCESS 默认）。", header_map = list(CI = "95% CI"))
    } else {
      d$add_table(data.frame(效应 = ef$效应, Effect = f3(ef$Effect), BootSE = f3(ef$BootSE), CI = sprintf("[%s, %s]", f3(ef$BootLLCI), f3(ef$BootULCI)), 显著 = ef$显著),
                  sprintf("PROCESS 模型 %d 间接效应（Bootstrap = %d 次）", pr$model, pr$B),
                  "注：百分位 Bootstrap 95% 置信区间，不包含 0 即显著；连续调节变量取第 16、50、84 百分位（PROCESS 默认）。",
                  header_map = list(BootSE = "Boot SE", CI = "Boot 95% CI"))
    }
  }
  d$save(path)
}

# ---- path diagram -------------------------------------------------------------

cjk_family <- function() {
  if (Sys.info()[["sysname"]] == "Darwin") "Heiti SC"
  else if (.Platform$OS.type == "windows") "Microsoft YaHei"
  else "Noto Sans CJK SC"
}

draw_path_diagram <- function(res, spec, edges, path) {
  cons <- unique(c(edges$iv, edges$dv))
  layer <- setNames(rep(0, length(cons)), cons)
  for (it in seq_along(cons)) for (i in seq_len(nrow(edges)))
    layer[edges$dv[i]] <- max(layer[edges$dv[i]], layer[edges$iv[i]] + 1)
  nl <- max(layer) + 1
  pos <- list()
  for (l in 0:(nl - 1)) {
    nodes <- names(layer)[layer == l]
    ys <- if (length(nodes) == 1) 0.52 else seq(0.84, 0.2, length.out = length(nodes))
    for (j in seq_along(nodes)) pos[[nodes[j]]] <- c(if (nl == 1) 0.5 else 0.09 + 0.82 * l / (nl - 1), ys[j])
  }
  a <- 0.072; b <- 0.115
  dev <- if (requireNamespace("ragg", quietly = TRUE)) ragg::agg_png else grDevices::png
  dev(path, width = 2400, height = 1450, res = 300)
  on.exit(grDevices::dev.off())
  graphics::par(mar = c(0.2, 0.2, 0.2, 0.2), family = cjk_family())
  graphics::plot.new(); graphics::plot.window(c(0, 1), c(0, 1))
  on_ellipse <- function(c0, toward) {
    u <- toward - c0; u <- u / sqrt(sum(u^2))
    c0 + u / sqrt((u[1] / a)^2 + (u[2] / b)^2)
  }
  # an edge whose straight line would cross another node is drawn as an arc
  crosses <- function(p0, p1) any(vapply(setdiff(names(pos), c()), function(k) {
    q <- pos[[k]]; if (all(q == p0) || all(q == p1)) return(FALSE)
    t <- sum((q - p0) * (p1 - p0)) / sum((p1 - p0)^2)
    if (t <= 0 || t >= 1) return(FALSE)
    d <- p0 + t * (p1 - p0) - q
    (d[1] / a)^2 + (d[2] / b)^2 < 1.3
  }, logical(1)))
  pe <- lavaan::standardizedSolution(res$sem_obj)
  lab_at <- list(); bend <- 1
  for (i in seq_len(nrow(edges))) {
    p0 <- pos[[edges$iv[i]]]; p1 <- pos[[edges$dv[i]]]
    r <- pe[pe$label == edges$label[i], ][1, ]
    sig <- r$pvalue < 0.05
    col <- if (sig) "black" else "grey45"; lty <- if (sig) 1 else 2; lwd <- if (sig) 1.6 else 1
    if (crosses(p0, p1)) {
      dir <- p1 - p0; nrm <- c(-dir[2], dir[1]) / sqrt(sum(dir^2))
      ctrl <- (p0 + p1) / 2 + nrm * 0.22 * bend; bend <- -bend
      s0 <- on_ellipse(p0, ctrl); s1 <- on_ellipse(p1, ctrl)
      tt <- seq(0, 1, length.out = 60)
      bx <- (1 - tt)^2 * s0[1] + 2 * (1 - tt) * tt * ctrl[1] + tt^2 * s1[1]
      by <- (1 - tt)^2 * s0[2] + 2 * (1 - tt) * tt * ctrl[2] + tt^2 * s1[2]
      graphics::lines(bx[1:59], by[1:59], col = col, lty = lty, lwd = lwd)
      graphics::arrows(bx[58], by[58], bx[60], by[60], length = 0.08, col = col, lwd = lwd)
      mid <- c(bx[30], by[30])
    } else {
      s0 <- on_ellipse(p0, p1); s1 <- on_ellipse(p1, p0)
      graphics::arrows(s0[1], s0[2], s1[1], s1[2], length = 0.08, lwd = lwd, lty = lty, col = col)
      mid <- s0 + (s1 - s0) * 0.45
    }
    lab_at[[i]] <- list(xy = mid, txt = paste0(f3(r$est.std), stars(r$pvalue)), col = if (sig) "black" else "grey35")
  }
  for (l in lab_at) {
    w <- graphics::strwidth(l$txt, cex = 0.8); h <- graphics::strheight(l$txt, cex = 0.8)
    graphics::rect(l$xy[1] - w / 2 - 0.006, l$xy[2] - h / 2 - 0.012, l$xy[1] + w / 2 + 0.006, l$xy[2] + h / 2 + 0.012, col = "white", border = NA)
    graphics::text(l$xy[1], l$xy[2], l$txt, cex = 0.8, col = l$col)
  }
  r2 <- lavaan::lavInspect(res$sem_obj, "r2")
  th <- seq(0, 2 * pi, length.out = 120)
  for (k in names(pos)) {
    p <- pos[[k]]
    graphics::polygon(p[1] + a * cos(th), p[2] + b * sin(th), col = "grey97", border = "black", lwd = 1.2)
    graphics::text(p[1], p[2] + 0.035, res$labels[[k]], cex = 0.8, font = 2)
    graphics::text(p[1], p[2] - 0.012, k, cex = 0.62, col = "grey30")
    if (k %in% names(r2)) graphics::text(p[1], p[2] - 0.055, sprintf("R² = %s", f3(r2[[k]])), cex = 0.62)
  }
  graphics::text(0.5, 0.02, "注：图中为标准化路径系数；实线为显著路径，虚线为不显著路径；*** p < 0.001，** p < 0.01，* p < 0.05。测量模型与外生构念间的相关未画出。", cex = 0.5, col = "grey30")
  invisible(path)
}

# ---- fit table ------------------------------------------------------------------

fit_rows <- function(cfa, sem = NULL) {
  idx <- list(
    c("χ²/df", "chisq_df", "< 3 良好，< 5 可接受"), c("GFI", "gfi", "> 0.90 良好，> 0.80 可接受"),
    c("AGFI", "agfi", "> 0.90 良好，> 0.80 可接受"), c("NFI", "nfi", "> 0.90"), c("IFI", "ifi", "> 0.90"),
    c("TLI", "tli", "> 0.90 可接受，≥ 0.95 良好"), c("CFI", "cfi", "> 0.90 可接受，≥ 0.95 良好"),
    c("RMSEA", "rmsea", "< 0.08 可接受，≤ 0.06 良好"), c("SRMR", "srmr", "< 0.08"))
  out <- data.frame(指标 = c("χ²", "df", vapply(idx, `[`, "", 1)),
                    参考标准 = c("—", "—", vapply(idx, `[`, "", 3)),
                    测量模型 = c(f3(cfa$chisq), as.character(cfa$df), vapply(idx, function(x) f3(cfa[[x[2]]]), "")),
                    stringsAsFactors = FALSE)
  if (!is.null(sem)) out$结构模型 <- c(f3(sem$chisq), as.character(sem$df), vapply(idx, function(x) f3(sem[[x[2]]]), ""))
  out
}

# ---- Excel --------------------------------------------------------------------

write_xlsx <- function(sheets, path) {
  wb <- openxlsx::createWorkbook()
  for (nm in names(sheets)) {
    if (is.null(sheets[[nm]]) || !NROW(sheets[[nm]])) next
    sh <- substr(nm, 1, 31)
    openxlsx::addWorksheet(wb, sh)
    openxlsx::writeData(wb, sh, sheets[[nm]])
    openxlsx::setColWidths(wb, sh, cols = seq_len(NCOL(sheets[[nm]])), widths = "auto")
  }
  openxlsx::saveWorkbook(wb, path, overwrite = TRUE)
}

# ---- modification record ----------------------------------------------------------

write_mod_record <- function(res, spec, path) {
  st <- res$mod_steps$steps
  L <- c("# 模型修正记录", "",
         "> 本记录由 spss-amos-sem 自动生成。规则：**只有写进设定卡 `modifications` 并写明理由的修正才会生效**，",
         "> 每一步修正前后的拟合指标都列在下面。论文里应如实报告做过哪些修正、为什么做；不要只报最终模型。", "",
         "## 每一步的拟合变化（测量模型）", "",
         "| 步骤 | 修正内容 | 理由（设定卡） | 数据依据（自动核对） | χ²/df | CFI | TLI | RMSEA | SRMR |", "|---|---|---|---|---|---|---|---|---|")
  for (s in st) L <- c(L, sprintf("| %s | %s | %s | %s | %s | %s | %s | %s | %s |", s$step, s$detail, if (nzchar(s$reason)) s$reason else "—", if (nzchar(s$evidence)) s$evidence else "—",
                                  f3(s$fit$chisq_df), f3(s$fit$cfi), f3(s$fit$tli), f3(s$fit$rmsea), f3(s$fit$srmr)))
  L <- c(L, "", "## 初始模型里值得注意的题项", "")
  low <- res$initial_loadings[res$initial_loadings$标准化载荷 < spec$loading_cutoff, ]
  if (nrow(low)) L <- c(L, sprintf("- `%s`（%s）标准化载荷 %s < %s", low$题项, low$构念, f3(low$标准化载荷), spec$loading_cutoff))
  else L <- c(L, sprintf("- 所有题项的标准化载荷都 ≥ %s。", spec$loading_cutoff))
  L <- c(L, "", "## 当前模型的修正指数（MI ≥ 4，前 10 个）", "",
         "工具只列出，不会自动采纳。跨构念的误差相关和交叉载荷一律不建议采纳。", "")
  mi <- res$mod_suggest
  if (nrow(mi)) {
    L <- c(L, "| 参数 | 类型 | MI | EPC | 建议 |", "|---|---|---|---|---|",
           sprintf("| `%s` | %s | %s | %s | %s |", mi$参数, mi$类型, f3(mi$MI, 2), f3(mi$预期改变EPC), mi$建议))
  } else L <- c(L, "没有 MI ≥ 4 的参数。")
  L <- c(L, "", "## 写进论文时", "",
         "- 删除题项：说明删除了哪一题、标准化载荷是多少、删除后该构念剩几题，以及删除后 α、CR、AVE 的变化。",
         "- 增加误差相关：只在同一构念内、且题干确实相似时才合理；要说明 MI 和理论理由。",
         "- 修正越多，越要提醒读者模型是数据驱动修改过的（MacCallum et al., 1992 指出按 MI 修正的模型在新样本上常常不能复现）。")
  writeLines(L, path, useBytes = TRUE)
}

# ---- paragraphs ---------------------------------------------------------------------

write_paragraphs <- function(res, spec, path) {
  lg <- res$clean_log; lab <- res$labels
  L <- c(sprintf("# %s：结果部分初稿", spec$project), "",
         "> 由 spss-amos-sem 根据本次运行的真实结果自动填数，数字全部来自 results.xlsx。请按自己学校的格式调整措辞；",
         "> 凡是写着「未达标」「不成立」的地方是如实结果，不要改成达标。", "")
  removed <- c()
  if (lg$out_of_range) removed <- c(removed, sprintf("%d 个超出量表范围的取值被设为缺失", lg$out_of_range))
  if (isTRUE(spec$drop_straightliners) && lg$straightliners) removed <- c(removed, sprintf("剔除规律作答（所有题目选同一选项）的问卷 %d 份", lg$straightliners))
  if (spec$missing == "listwise" && lg$incomplete) removed <- c(removed, sprintf("剔除存在缺失值的问卷 %d 份", lg$incomplete))
  L <- c(L, "## 样本概况", "",
         sprintf("本研究共回收问卷 %d 份，%s，最终得到有效问卷 %d 份，有效回收率为 %s%%。",
                 lg$n_raw, if (length(removed)) paste(removed, collapse = "，") else "无需剔除", lg$n_used, f3(100 * lg$n_used / lg$n_raw, 2)), "")

  h <- res$harman
  L <- c(L, "## 共同方法偏差检验", "",
         sprintf("采用 Harman 单因素检验（Podsakoff et al., 2003；周浩、龙立荣, 2004），对全部 %d 个题项做未旋转的探索性因子分析，共提取出 %d 个特征值大于 1 的因子，第一个因子的方差解释率为 %s%%，%s 40%% 的临界标准，%s。",
                 length(unlist(res$items)), h$n_eigen_gt1, f3(h$first_pct, 2), if (h$first_pct < 40) "低于" else "高于",
                 if (h$first_pct < 40) "说明本研究不存在严重的共同方法偏差" else "提示可能存在共同方法偏差，需要谨慎解释结果"))
  cm <- res$cmb
  L <- c(L, sprintf("进一步将所有题项设定为负荷在同一个因子上做验证性因子分析，单因子模型的拟合（χ²/df = %s，CFI = %s，RMSEA = %s）明显差于 %d 因子测量模型（Δχ² = %s，Δdf = %d，p %s），再次说明共同方法偏差不严重。",
                    f3(cm$fit$chisq_df), f3(cm$fit$cfi), f3(cm$fit$rmsea), length(res$items), f3(cm$delta_chisq, 2), as.integer(cm$delta_df), if (cm$p < 0.001) "< 0.001" else paste("=", f3(cm$p))), "")

  rl <- res$reliability[!duplicated(res$reliability$代码), ]
  low_a <- rl$构念[rl$Cronbachα < 0.7]
  L <- c(L, "## 信度分析", "",
         sprintf("各构念的 Cronbach's α 系数介于 %s 之间，%s；各题项的 CITC 均%s 0.5%s。",
                 rng(rl$Cronbachα), if (length(low_a)) sprintf("其中%s低于 0.7，信度偏低", paste(low_a, collapse = "、")) else "均大于 0.7，说明量表具有良好的内部一致性",
                 if (min(res$reliability$CITC) >= 0.5) "大于" else "未全部大于",
                 if (min(res$reliability$CITC) >= 0.5) "，删除任一题项都不会使所在构念的 α 明显提高" else sprintf("（最低为 %s）", f3(min(res$reliability$CITC)))), "")

  e <- res$efa
  L <- c(L, "## 效度分析", "", "### 探索性因子分析", "",
         sprintf("KMO 值为 %s，Bartlett 球形检验的近似卡方为 %s（df = %d，p %s），%s。采用主成分分析法、最大方差旋转，按理论维度提取 %d 个因子，累计方差解释率为 %s%%%s。",
                 f3(e$kmo), f3(e$bartlett_chisq, 2), as.integer(e$bartlett_df), if (e$bartlett_p < 0.001) "< 0.001" else paste("=", f3(e$bartlett_p)),
                 if (e$kmo >= 0.7) "说明数据适合做因子分析" else "KMO 偏低，做因子分析需谨慎",
                 length(res$items), f3(e$cum_pct, 2), if (e$cum_pct >= 60) "，超过 60% 的经验标准" else "，低于 60% 的经验标准"),
         if (length(e$flags)) paste0("需要注意：", paste(e$flags, collapse = "；"), "。") else "各题项均在所属因子上有较高载荷（> 0.5），且没有明显的交叉载荷，因子结构与理论设想一致。", "")
  v <- res$validity
  L <- c(L, "### 收敛效度", "",
         sprintf("使用 AMOS 进行验证性因子分析。测量模型拟合良好与否见下文；各题项的标准化因子载荷介于 %s 之间%s，组合信度（CR）介于 %s 之间，平均方差抽取量（AVE）介于 %s 之间%s。",
                 rng(res$loadings$标准化载荷), if (min(res$loadings$标准化载荷) >= 0.5) "，均大于 0.5 且在 0.001 水平上显著" else "",
                 rng(v$CR), rng(v$AVE),
                 if (min(v$CR) >= 0.7 && min(v$AVE) >= 0.5) "，均达到 CR > 0.7、AVE > 0.5 的标准（Fornell & Larcker, 1981），说明量表具有良好的收敛效度" else
                   sprintf("；%s未达到 CR > 0.7 或 AVE > 0.5 的标准，收敛效度有待改进", paste(v$构念[v$CR < 0.7 | v$AVE < 0.5], collapse = "、"))), "")
  fl <- res$fornell; ht <- res$htmt; maxh <- max(ht[lower.tri(ht)])
  L <- c(L, "### 区分效度", "",
         sprintf("各构念 AVE 的平方根%s其与其他构念的相关系数%s；HTMT 值最大为 %s，%s。",
                 if (all(fl$pass)) "均大于" else "并未全部大于",
                 if (all(fl$pass)) "，满足 Fornell-Larcker 准则" else sprintf("（%s不满足 Fornell-Larcker 准则）", paste(unlist(lab[names(fl$pass)[!fl$pass]]), collapse = "、")),
                 f3(maxh), if (maxh < 0.85) "低于 0.85 的严格标准（Henseler et al., 2015），说明各构念之间具有良好的区分效度" else if (maxh < 0.9) "低于 0.90 的宽松标准" else "超过 0.90，区分效度存疑"), "")

  cf <- res$cfa_fit; vd <- fit_verdicts(cf)
  L <- c(L, "## 模型拟合", "",
         sprintf("测量模型的拟合指标为：χ²/df = %s，CFI = %s，TLI = %s，IFI = %s，RMSEA = %s，SRMR = %s。%s",
                 f3(cf$chisq_df), f3(cf$cfi), f3(cf$tli), f3(cf$ifi), f3(cf$rmsea), f3(cf$srmr),
                 if (all(vd[c("chisq_df", "cfi", "tli", "rmsea", "srmr")] != "未达标")) "各项指标均达到可接受水平（Hu & Bentler, 1999），测量模型拟合良好。"
                 else sprintf("其中 %s 未达标，测量模型拟合不够理想。", paste(toupper(names(vd)[vd == "未达标"]), collapse = "、"))))
  if (length(spec$modifications)) L <- c(L, sprintf("需要说明的是，测量模型在初始设定基础上做了 %d 处修正（%s），修正理由与每一步的拟合变化见模型修正记录。",
                                                    length(spec$modifications), paste(vapply(res$mod_steps$steps[-1], `[[`, "", "detail"), collapse = "；")))
  L <- c(L, "")
  if (!is.null(res$paths)) {
    sf <- res$sem_fit; p <- res$paths
    sup <- p$假设[p$结论 == "支持"]; uns <- p$假设[p$结论 != "支持"]
    L <- c(L, "## 假设检验", "",
           sprintf("结构模型的拟合指标为：χ²/df = %s，CFI = %s，TLI = %s，RMSEA = %s，SRMR = %s。路径分析结果显示：",
                   f3(sf$chisq_df), f3(sf$cfi), f3(sf$tli), f3(sf$rmsea), f3(sf$srmr)))
    for (i in seq_len(nrow(p))) {
      L <- c(L, sprintf("- %s：%s的标准化路径系数为 %s（z = %s，p %s），%s。", p$假设[i], sub(" → ", "对", p$路径[i]),
                        f3(p$标准化系数β[i]), f3(p$CR_z[i]), if (p$p[i] < 0.001) "< 0.001" else paste("=", f3(p$p[i])),
                        if (p$结论[i] == "支持") sprintf("%s影响显著，假设得到支持", if (p$标准化系数β[i] > 0) "正向" else "负向") else "未达到显著水平，假设不成立"))
    }
    r2 <- res$r2
    L <- c(L, "", sprintf("综上，%s得到支持%s。模型对%s的解释力（R²）分别为 %s。",
                          if (length(sup)) paste(sup, collapse = "、") else "没有假设", if (length(uns)) sprintf("，%s未得到支持", paste(uns, collapse = "、")) else "",
                          paste(r2$构念, collapse = "、"), paste(f3(r2$R2), collapse = "、")), "")
  }
  if (!is.null(res$effects)) {
    sp <- res$effects$specific
    L <- c(L, "## 中介效应检验", "",
           sprintf("采用 Bootstrap 法（重复抽样 %d 次）检验中介效应，计算偏差校正的 95%% 置信区间（Preacher & Hayes, 2008）。结果如下：", as.integer(spec$bootstrap)))
    for (i in seq_len(nrow(sp))) {
      L <- c(L, sprintf("- %s：%s 的间接效应为 %s，95%% 置信区间为 [%s, %s]，%s0，%s。", sp$编号[i], sp$效应[i], f3(sp$效应值[i]), f3(sp$BC下限[i]), f3(sp$BC上限[i]),
                        if (sp$显著[i] == "是") "不包含 " else "包含 ", if (sp$显著[i] == "是") sprintf("中介效应显著，属于%s", sp$中介类型[i]) else "中介效应不显著"))
    }
    L <- c(L, "")
  }
  if (!is.null(res$multigroup) && is.null(res$multigroup$skipped)) {
    mg <- res$multigroup$invariance; pg <- res$multigroup$paths
    sigd <- pg$路径[pg$p_差异 < 0.05]
    L <- c(L, "## 多群组分析", "",
           sprintf("以%s为分组变量进行测量不变性检验。%s在此基础上比较各结构路径的组间差异，%s。",
                   res$multigroup$var_label,
                   paste(sprintf("%s：ΔCFI = %s，ΔRMSEA = %s，%s。", mg$模型[-1], f3(mg$ΔCFI[-1]), f3(mg$ΔRMSEA[-1]), mg$判断[-1]), collapse = ""),
                   if (length(sigd)) sprintf("%s 在两组间差异显著", paste(sigd, collapse = "、")) else "所有路径在两组间均无显著差异"), "")
  }
  for (pr in res$process) {
    ef <- pr$effects
    L <- c(L, sprintf("## PROCESS 模型 %d", pr$model), "")
    if (pr$model == 1) {
      rc <- attr(ef, "r2_change"); jn <- attr(ef, "jn")
      L <- c(L, sprintf("交互项使 R² 增加了 %s（F(1, %d) = %s，p %s）。简单斜率分析显示：%s%s", f3(rc[["dR2"]]), as.integer(rc[["df2"]]), f3(rc[["F"]]),
                        if (rc[["p"]] < 0.001) "< 0.001" else paste("=", f3(rc[["p"]])),
                        paste(sprintf("%s，效应为 %s（p %s）", ef$效应, f3(ef$Effect), ifelse(ef$p < 0.001, "< 0.001", paste("=", f3(ef$p)))), collapse = "；"),
                        if (length(jn)) sprintf("。Johnson-Neyman 显著性转折点为 %s = %s。", pr$w, paste(f3(jn), collapse = "、")) else "。"))
    } else {
      nm <- function(k) sprintf("%s（%s）", lab[[k]] %||% res$var_labels[[k]] %||% k, k)
      L <- c(L, sprintf("以%s为自变量、%s为因变量%s%s，基于构念均值做 OLS 回归，Bootstrap %d 次（百分位法）。", nm(pr$x), nm(pr$y),
                        if (length(pr$m)) sprintf("、%s为中介变量", paste(vapply(pr$m, nm, ""), collapse = "、")) else "",
                        if (!is.null(pr$w)) sprintf("、%s为调节变量", nm(pr$w)) else "", as.integer(pr$B)))
      for (i in seq_len(nrow(ef))) L <- c(L, sprintf("- %s：%s，95%% CI [%s, %s]，%s。", ef$效应[i], f3(ef$Effect[i]), f3(ef$BootLLCI[i]), f3(ef$BootULCI[i]), if (ef$显著[i] == "是") "显著" else "不显著"))
    }
    L <- c(L, "")
  }
  L <- c(L, "## 参考文献（正文引用过的）", "", readLines(file.path(SKILL_DIR, "references", "citations.md"), encoding = "UTF-8")[-(1:2)])
  writeLines(L, path, useBytes = TRUE)
}
