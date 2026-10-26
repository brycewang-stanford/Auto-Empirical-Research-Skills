#!/usr/bin/env Rscript
# End-to-end check on the bundled demo: runs the pipeline in --quick mode and
# verifies the numbers against independent implementations (psych, lm) and the
# known generating model, then checks the generated SPSS / AMOS files.
#
#   Rscript tests/test_demo.R

here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
SKILL_DIR <- dirname(here)
for (f in c("io.R", "measure.R", "cfa_sem.R", "process.R", "gen_spss.R", "gen_amos.R", "report.R"))
  source(file.path(SKILL_DIR, "scripts", "R", f), encoding = "UTF-8")

fails <- 0
check <- function(ok, what) {
  cat(if (isTRUE(ok)) "  ok   " else { fails <<- fails + 1; "  FAIL " }, what, "\n", sep = "")
}

out <- file.path(tempdir(), "sem_demo_test")
unlink(out, recursive = TRUE)
spec_path <- file.path(SKILL_DIR, "assets", "demo", "spec_demo.yml")
status <- system2("Rscript", c(shQuote(file.path(SKILL_DIR, "scripts", "run_sem.R")), shQuote(spec_path), "--out", shQuote(out), "--quick"),
                  stdout = FALSE, stderr = FALSE)
check(status == 0, "pipeline exits 0 on the demo")

cat("\n[outputs]\n")
for (f in c("results.xlsx", "结果表格.docx", "结果段落.md", "模型修正记录.md", "路径图.png", "analysis.sps",
            "questionnaire_demo_cleaned.sav", "lavaan_model.txt", "results.json",
            "amos/AMOS操作步骤.md", "amos/01_CFA_VB程序.vb", "amos/02_SEM_VB程序.vb", "amos/03_自定义估计量.txt"))
  check(file.exists(file.path(out, f)), f)
js <- jsonlite::fromJSON(file.path(out, "results.json"))

cat("\n[cleaning]\n")
check(js$sample$straightliners == 8, "all 8 planted straight-liners found (judged before reverse coding)")
check(js$sample$out_of_range == 0, "SPSS user-missing code 9 already read as missing")
check(js$sample$n_used == js$sample$n_raw - 8 - js$sample$incomplete, "listwise N adds up")

cat("\n[independent re-computation]\n")
spec <- read_spec(spec_path)
raw <- read_raw(spec); cl <- clean_data(spec, raw); df <- cl$data
items <- active_items(spec)
for (k in names(items)) {
  a_psych <- suppressWarnings(psych::alpha(df[items[[k]]], warnings = FALSE)$total$raw_alpha)
  check(abs(js$alpha[[k]] - a_psych) < 1e-8, sprintf("Cronbach alpha %s matches psych::alpha", k))
}
R <- cor(df[unlist(items)])
check(abs(js$kmo - psych::KMO(R)$MSA) < 1e-10, "KMO matches psych::KMO")
x <- df$PU1; n <- length(x)
check(abs(spss_skew(x) - (sqrt(n * (n - 1)) / (n - 2)) * mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5) < 1e-10,
      "skewness is SPSS's adjusted G1")

cfa <- fit_cfa(spec, df, items, error_covs_of(spec$modifications))
cfa_n <- lavaan::cfa(attr(cfa, "syntax"), data = df, estimator = "ML", likelihood = "normal")
N <- nrow(df)
check(abs(js$cfa_fit$chisq / lavaan::fitMeasures(cfa_n, "chisq") - (N - 1) / N) < 1e-6, "chi-square uses (N - 1) * F like AMOS")

sc <- mean_scores(df, items)
a <- coef(lm(SAT ~ PU, sc))[["PU"]]; b <- coef(lm(CI ~ PU + SAT, sc))[["SAT"]]
p4 <- js$process$effects[[1]]
check(abs(p4$Effect[1] - a * b) < 1e-10, "PROCESS model 4 indirect = a*b from lm()")
tr_c <- sc$TR - mean(sc$TR); pu_c <- sc$PU - mean(sc$PU)
a3 <- coef(lm(sc$SAT ~ pu_c + tr_c + I(pu_c * tr_c)))[[4]]
b7 <- coef(lm(sc$CI ~ pu_c + sc$SAT))[[3]]
p7 <- js$process$effects[[2]]
check(abs(p7$Effect[grepl("有调节的中介指数", p7$效应)] - a3 * b7) < 1e-10, "PROCESS model 7 index of moderated mediation = a3*b")

cat("\n[recovers the generating model]\n")
paths <- js$paths
check(all(paths$结论[paths$假设 %in% paste0("H", 1:6)] == "支持"), "H1-H6 (true non-zero paths) supported")
check(paths$结论[paths$假设 == "H7"] == "不支持", "H7 (true zero path TR -> CI) not supported")
check(abs(paths$标准化系数β[paths$假设 == "H1"] - 0.45) < 0.1, "PEOU -> PU beta near the generating 0.45")
mods <- js$modifications
check(grepl("TR4", mods$detail[2]) && grepl("0\\.[0-4]", mods$evidence[2]), "TR4 flagged by its low loading before it is dropped")
check(all(js$cr_ave$CR > 0.7) && all(js$cr_ave$AVE > 0.5), "CR > .7 and AVE > .5 after modification")

cat("\n[generated SPSS / AMOS files]\n")
sps <- readLines(file.path(out, "analysis.sps"), encoding = "UTF-8")
check(sps[1] == "* Encoding: UTF-8.", "syntax declares UTF-8")
check(!any(grepl("^\\*", sps) & !grepl("\\.$", sps)), "every SPSS comment line ends with a period")
check(sum(grepl("^RELIABILITY", sps)) == length(items), "one RELIABILITY per construct")
check(which(grepl("SD\\(", sps)) < which(grepl("^RECODE PEOU4", sps)), "straight-lining checked before reverse coding")
check(sum(grepl("^process ", sps)) == 2, "two PROCESS calls")
vb <- readLines(file.path(out, "amos", "02_SEM_VB程序.vb"), encoding = "UTF-8")
n_items <- length(unlist(items)); edges <- structural_edges(spec)
n_ast <- 2 * n_items + nrow(edges) + length(unique(edges$dv)) + length(error_covs_of(spec$modifications))
check(sum(grepl("Sem.AStructure", vb)) == n_ast, sprintf("SEM program has %d AStructure lines", n_ast))
check(any(grepl("Sem.AStructure\\(\"e[0-9]+ <> e[0-9]+\"\\)", vb)), "error covariance written as e <> e")
est <- readLines(file.path(out, "amos", "03_自定义估计量.txt"), encoding = "UTF-8")
check(length(est) == length(spec$indirect) && all(grepl("^H[0-9]+ = p\\.P[0-9]+( \\* p\\.P[0-9]+)+$", est)), "estimands in `Name = p.A * p.B` form")

cat("\n[spec validation]\n")
bad <- function(edit, pattern) {
  s <- yaml::read_yaml(spec_path, handlers = YAML_HANDLERS); s <- edit(s)
  f <- tempfile(fileext = ".yml"); yaml::write_yaml(s, f)
  file.copy(file.path(SKILL_DIR, "assets", "demo", "questionnaire_demo.sav"), dirname(f), overwrite = TRUE)
  msg <- tryCatch({ read_spec(f); "" }, error = function(e) conditionMessage(e))
  grepl(pattern, msg)
}
check(bad(function(s) { s$hypotheses$H99 <- "CI -> PEOU"; s }, "没有对应路径"), "hypothesis without a structural path is rejected")
check(bad(function(s) { s$modifications[[1]]$reason <- ""; s }, "reason"), "modification without a reason is rejected")
check(bad(function(s) { s$structural$PEOU <- list("CI"); s }, "有环"), "non-recursive model is rejected")
check(bad(function(s) { names(s$constructs)[1] <- "PERCEIVED"; s }, "6 个字符"), "construct code longer than 6 chars is rejected")

cat("\n[other PROCESS models, observed moderator, FIML, no multigroup]\n")
s2 <- yaml::read_yaml(spec_path, handlers = YAML_HANDLERS)
s2$missing <- "fiml"; s2$multigroup <- NULL; s2$indirect <- NULL; s2$controls <- list("use_years")
s2$process <- list(list(model = 1L, x = "PU", y = "CI", w = "TR"),
                   list(model = 6L, x = "PEOU", m = list("PU", "SAT"), y = "CI"),
                   list(model = 14L, x = "PU", m = list("SAT"), y = "CI", w = "gender"))
d2 <- file.path(tempdir(), "sem_spec2"); dir.create(d2, showWarnings = FALSE)
invisible(file.copy(file.path(SKILL_DIR, "assets", "demo", "questionnaire_demo.sav"), d2, overwrite = TRUE))
yaml::write_yaml(s2, file.path(d2, "spec2.yml"))
out2 <- file.path(d2, "out")
st2 <- system2("Rscript", c(shQuote(file.path(SKILL_DIR, "scripts", "run_sem.R")), shQuote(file.path(d2, "spec2.yml")), "--out", shQuote(out2), "--quick"),
               stdout = FALSE, stderr = FALSE)
check(st2 == 0, "pipeline exits 0 with models 1/6/14, FIML and a control variable")
if (st2 == 0) {
  js2 <- jsonlite::fromJSON(file.path(out2, "results.json"), simplifyVector = FALSE)
  e6 <- vapply(js2$process[[2]]$effects, `[[`, "", "效应")
  check(sum(grepl("^PEOU → ", e6)) == 3, "model 6 with two mediators reports three chains")
  sps2 <- readLines(file.path(out2, "analysis.sps"), encoding = "UTF-8")
  check(any(grepl("^process .*w=gender/model=14", sps2)), "observed moderator keeps its own name in the PROCESS call")
  check(!any(grepl("^process .*model=1/", sps2) & grepl("/m=", sps2)), "model 1 call has no m= (no $-partial-match of `model`)")
}

cat(sprintf("\n%s\n", if (fails) sprintf("%d check(s) FAILED", fails) else "all checks passed"))
quit(status = if (fails) 1 else 0)
