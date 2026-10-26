#!/usr/bin/env Rscript
# Build the bundled demo questionnaire (assets/demo/questionnaire_demo.sav).
#
# A simulated mobile-payment continuance study whose generating values are
# known, so a pipeline run can be checked against the truth. The design
# deliberately plants the problems real questionnaire data has: one reverse-
# worded item, one weak item, one correlated error pair, an SPSS user-missing
# code (9), item non-response and straight-lining respondents.
#
#   Rscript scripts/make_demo_data.R [output_dir]

suppressPackageStartupMessages(library(haven))
`%||%` <- function(a, b) if (is.null(a)) b else a

args <- commandArgs(trailingOnly = TRUE)
out_dir <- if (length(args)) args[[1]] else {
  here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
  file.path(dirname(here), "assets", "demo")
}
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

set.seed(20261027)
n <- 430

# ---- latent model (all latent variances = 1) --------------------------------
peou <- rnorm(n)
tr   <- 0.30 * peou + sqrt(1 - 0.30^2) * rnorm(n)
pu   <- 0.45 * peou + sqrt(1 - 0.45^2) * rnorm(n)
lin_sat <- 0.35 * pu + 0.20 * peou + 0.25 * tr + 0.25 * pu * tr
sat  <- lin_sat + sqrt(max(1 - var(lin_sat), 0.2)) * rnorm(n)
sat  <- as.numeric(scale(sat))
lin_ci <- 0.40 * sat + 0.25 * pu + 0.00 * tr
ci   <- lin_ci + sqrt(1 - var(lin_ci)) * rnorm(n)
ci   <- as.numeric(scale(ci))

lambda <- list(
  PEOU = c(0.78, 0.82, 0.75, 0.80),
  PU   = c(0.80, 0.83, 0.77, 0.81),
  TR   = c(0.76, 0.80, 0.78, 0.35),
  SAT  = c(0.82, 0.85, 0.79),
  CI   = c(0.84, 0.80, 0.83)
)
eta <- list(PEOU = peou, PU = pu, TR = tr, SAT = sat, CI = ci)
cuts <- c(-Inf, -1.8, -0.9, 0.1, 1.1, Inf)   # 5-point Likert, mild ceiling

# Small misspecifications the analysis model does not contain, so the fit is
# realistic (good, not perfect): two cross-loadings and a CI1/CI3 error pair.
cross <- list(PU4 = 0.20 * sat, TR3 = 0.15 * peou)
items <- list()
shared_sat <- rnorm(n)                       # SAT1/SAT2 share wording
shared_ci <- rnorm(n)
for (k in names(lambda)) {
  for (j in seq_along(lambda[[k]])) {
    nm <- paste0(k, j)
    l <- lambda[[k]][j]
    e <- rnorm(n)
    if (k == "SAT" && j <= 2) e <- sqrt(0.6) * e + sqrt(0.4) * shared_sat
    if (nm %in% c("CI1", "CI3")) e <- sqrt(0.8) * e + sqrt(0.2) * shared_ci
    y <- l * eta[[k]] + sqrt(1 - l^2) * e + (cross[[nm]] %||% 0)
    items[[nm]] <- as.integer(cut(y, cuts, labels = FALSE))
  }
}
df <- as.data.frame(items)
df$PEOU4 <- 6L - df$PEOU4                    # stored reverse-worded

# ---- demographics ------------------------------------------------------------
df <- cbind(
  data.frame(
    id = seq_len(n),
    gender = sample(1:2, n, TRUE, c(0.46, 0.54)),
    age = sample(1:4, n, TRUE, c(0.32, 0.38, 0.20, 0.10)),
    edu = sample(1:4, n, TRUE, c(0.12, 0.25, 0.48, 0.15)),
    use_years = sample(1:4, n, TRUE, c(0.15, 0.30, 0.35, 0.20))
  ),
  df
)

# ---- data problems -----------------------------------------------------------
item_names <- names(items)
straight <- sample(n, 8)
for (i in straight) df[i, item_names] <- sample(c(3L, 5L), 1)
miss_rows <- sample(setdiff(seq_len(n), straight), 13)
for (i in miss_rows) df[i, sample(item_names, 1)] <- NA
code9_rows <- sample(setdiff(seq_len(n), c(straight, miss_rows)), 4)
for (i in code9_rows) df[i, sample(item_names, 1)] <- 9L

# ---- SPSS metadata -----------------------------------------------------------
wording <- c(
  PEOU1 = "学会使用该移动支付 App 对我来说很容易",
  PEOU2 = "我觉得该 App 的操作流程清晰易懂",
  PEOU3 = "我能熟练地用该 App 完成付款",
  PEOU4 = "使用该 App 需要花费我很多精力（反向题）",
  PU1 = "使用该 App 提高了我的支付效率",
  PU2 = "该 App 让日常消费更方便",
  PU3 = "使用该 App 帮我节省了时间",
  PU4 = "总体而言该 App 对我很有用",
  TR1 = "我相信该 App 会保护我的个人信息",
  TR2 = "我相信该 App 的资金安全有保障",
  TR3 = "我相信该 App 会信守对用户的承诺",
  TR4 = "我会关注该 App 的新闻报道",
  SAT1 = "我对使用该 App 的体验感到满意",
  SAT2 = "使用该 App 让我感到愉快",
  SAT3 = "该 App 达到了我的预期",
  CI1 = "我打算继续使用该 App",
  CI2 = "未来我会更频繁地使用该 App",
  CI3 = "我不会改用其他支付 App"
)
likert <- c("非常不同意" = 1, "不同意" = 2, "一般" = 3, "同意" = 4, "非常同意" = 5, "缺失" = 9)
for (v in item_names) {
  df[[v]] <- labelled_spss(df[[v]], labels = likert, na_values = 9, label = wording[[v]])
}
df$gender <- labelled(df$gender, c("男" = 1, "女" = 2), label = "性别")
df$age <- labelled(df$age, c("18-25岁" = 1, "26-35岁" = 2, "36-45岁" = 3, "46岁及以上" = 4), label = "年龄")
df$edu <- labelled(df$edu, c("高中及以下" = 1, "大专" = 2, "本科" = 3, "硕士及以上" = 4), label = "学历")
df$use_years <- labelled(df$use_years, c("1年以内" = 1, "1-2年" = 2, "3-5年" = 3, "5年以上" = 4), label = "使用年限")
attr(df$id, "label") <- "问卷编号"

out <- file.path(out_dir, "questionnaire_demo.sav")
write_sav(df, out)
cat("wrote", out, "-", nrow(df), "rows x", ncol(df), "variables\n")
