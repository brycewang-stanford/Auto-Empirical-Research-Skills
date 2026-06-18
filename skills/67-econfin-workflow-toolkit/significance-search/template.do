*==========================================================================
*  控制变量组合搜索 — 多Stata实例并行版
*  自动生成，请勿手动修改
*  功能：穷举可选控制变量组合，找到使X的|t|最大的组合
*==========================================================================

clear all
set more off

*=================================================
*              用户设置区
*=================================================

global N_WORKERS  <<N_WORKERS>>
global STATA_EXE `"<<STATA_EXE>>"'
global PROJ_DIR `"<<PROJ_DIR>>"'
global TEMP_DIR `"${PROJ_DIR}\__parallel_temp"'

global significance "<<SIGNIFICANCE>>"

global dependentVariable        "<<DEP_VAR>>"
global independentVariable      "<<INDEP_VAR>>"
global mandatoryControls        "<<MANDATORY_CONTROLS>>"
global optionalControls         "<<OPTIONAL_CONTROLS>>"

global model_cmd    "<<MODEL_CMD>>"
global model_absorb "<<MODEL_ABSORB>>"
global model_vce    "<<MODEL_VCE>>"

* 心跳停滞判定（秒）
global HEARTBEAT_STALL <<HEARTBEAT_STALL>>

*=================================================
*  第一步  准备tuples
*=================================================

use "${PROJ_DIR}\<<DATA_FILE>>", clear
tuples $optionalControls
local total = `ntuples'
display "可选控制变量组合总数: `total'"

shell mkdir "${TEMP_DIR}" 2>nul

clear
set obs `total'
gen int tuple_id = _n
gen str244 combo = ""
forvalues i = 1/`total' {
    qui replace combo = `"`tuple`i''"' in `i'
}
save "${TEMP_DIR}\tuples_list.dta", replace

*=================================================
*  第二步  生成worker do文件并启动
*=================================================

local base_chunk = floor(`total' / ${N_WORKERS})
local remainder  = mod(`total', ${N_WORKERS})
local actual_workers = min(${N_WORKERS}, `total')

local cursor = 1
forvalues w = 1/`actual_workers' {
    local this_chunk = `base_chunk' + (`w' <= `remainder')
    if `this_chunk' == 0 continue
    local wk_start = `cursor'
    local wk_end   = `cursor' + `this_chunk' - 1
    local cursor   = `wk_end' + 1

    display "Worker `w': 组合 `wk_start' ~ `wk_end' (共 `this_chunk' 个)"

    * 将worker代码写入do文件
    tempname fh
    file open `fh' using "${TEMP_DIR}\worker_`w'.do", write replace

    #delimit ;
    file write `fh'
        `"clear all"' _newline
        `"set more off"' _newline
        _newline
        `"global PROJ_DIR `"${PROJ_DIR}"'"' _newline
        `"global TEMP_DIR `"${TEMP_DIR}"'"' _newline
        `"global dependentVariable  "${dependentVariable}""' _newline
        `"global independentVariable "${independentVariable}""' _newline
        `"global mandatoryControls "${mandatoryControls}""' _newline
        `"global model_cmd "${model_cmd}""' _newline
        `"global model_absorb "${model_absorb}""' _newline
        `"global model_vce "${model_vce}""' _newline
        _newline
    ;
    #delimit cr

    * 加载tuples并读入locals
    file write `fh' `"use "${TEMP_DIR}\tuples_list.dta", clear"' _newline
    file write `fh' `"local n_combos = _N"' _newline
    file write `fh' `"forvalues j = 1/"' _char(96) `"n_combos"' _char(39) `" {"' _newline
    file write `fh' `"    local combo_"' _char(96) `"j"' _char(39) `" = combo["' _char(96) `"j"' _char(39) `"]"' _newline
    file write `fh' `"}"' _newline
    file write `fh' _newline

    * 加载主数据
    file write `fh' `"use "${PROJ_DIR}\<<DATA_FILE>>", clear"' _newline
    file write `fh' _newline

    * 启动心跳（用capture防止文件锁冲突）
    file write `fh' `"cap noisily {"' _newline
    file write `fh' `"    tempname hb_handle"' _newline
    file write `fh' `"    file open "' _char(96) `"hb_handle"' _char(39) `" using "${TEMP_DIR}\heartbeat_`w'.txt", write replace"' _newline
    file write `fh' `"    file write "' _char(96) `"hb_handle"' _char(39) `" "0""' _newline
    file write `fh' `"    file close "' _char(96) `"hb_handle"' _char(39) _newline
    file write `fh' `"}"' _newline
    file write `fh' _newline

    * 用postfile高效收集结果
    file write `fh' `"tempname pf"' _newline
    file write `fh' `"tempfile pf_file"' _newline
    file write `fh' `"postfile "' _char(96) `"pf"' _char(39) `" int(tuple_id) double(t_val b_val se_val) long(n_obs) byte(converged) str244(combo) using "' _char(96) `"pf_file"' _char(39) `""' _newline
    file write `fh' _newline

    * 主循环
    file write `fh' `"local row = 0"' _newline
    file write `fh' `"forvalues i = `wk_start'/`wk_end' {"' _newline
    file write `fh' `"    local row = "' _char(96) `"row"' _char(39) `" + 1"' _newline
    file write `fh' `"    local this_combo ""' _char(96) `"combo_"' _char(96) `"i"' _char(39) _char(39) `"""' _newline
    file write `fh' `"    cap qui ${model_cmd} ${dependentVariable} ${independentVariable} ${mandatoryControls} "' _char(96) `"this_combo"' _char(39) `" , ${model_absorb} ${model_vce}"' _newline
    file write `fh' `"    if _rc == 0 {"' _newline
    file write `fh' `"        local ct = abs(_b[${independentVariable}] / _se[${independentVariable}])"' _newline
    file write `fh' `"        local cb = _b[${independentVariable}]"' _newline
    file write `fh' `"        local cs = _se[${independentVariable}]"' _newline
    file write `fh' `"        local cn = e(N)"' _newline
    file write `fh' `"        post "' _char(96) `"pf"' _char(39) `" ("' _char(96) `"i"' _char(39) `") ("' _char(96) `"ct"' _char(39) `") ("' _char(96) `"cb"' _char(39) `") ("' _char(96) `"cs"' _char(39) `") ("' _char(96) `"cn"' _char(39) `") (1) (""' _char(96) `"this_combo"' _char(39) `"")"' _newline
    file write `fh' `"    }"' _newline
    file write `fh' `"    else {"' _newline
    file write `fh' `"        post "' _char(96) `"pf"' _char(39) `" ("' _char(96) `"i"' _char(39) `") (.) (.) (.) (.) (0) (""' _char(96) `"this_combo"' _char(39) `"")"' _newline
    file write `fh' `"    }"' _newline

    * 心跳更新（用capture防止文件锁冲突）
    file write `fh' `"    cap noisily {"' _newline
    file write `fh' `"        tempname hb_handle"' _newline
    file write `fh' `"        file open "' _char(96) `"hb_handle"' _char(39) `" using "${TEMP_DIR}\heartbeat_`w'.txt", write replace"' _newline
    file write `fh' `"        file write "' _char(96) `"hb_handle"' _char(39) `" ""' _char(96) `"row"' _char(39) `"""' _newline
    file write `fh' `"        file close "' _char(96) `"hb_handle"' _char(39) _newline
    file write `fh' `"    }"' _newline

    file write `fh' `"}"' _newline
    file write `fh' _newline

    * 关闭postfile并保存
    file write `fh' `"postclose "' _char(96) `"pf"' _char(39) _newline
    file write `fh' `"use "' _char(96) `"pf_file"' _char(39) `", clear"' _newline
    file write `fh' `"save "${TEMP_DIR}\result_`w'.dta", replace"' _newline
    file write `fh' _newline

    * 完成标记
    file write `fh' `"tempname done_handle"' _newline
    file write `fh' `"file open "' _char(96) `"done_handle"' _char(39) `" using "${TEMP_DIR}\done_`w'.txt", write replace"' _newline
    file write `fh' `"file write "' _char(96) `"done_handle"' _char(39) `" "done""' _newline
    file write `fh' `"file close "' _char(96) `"done_handle"' _char(39) _newline
    file write `fh' _newline
    file write `fh' `"exit, clear STATA"' _newline

    file close `fh'
}

* ── 清理旧的临时文件（防止残留干扰）──
forvalues w = 1/`actual_workers' {
    cap erase "${TEMP_DIR}\done_`w'.txt"
    cap erase "${TEMP_DIR}\result_`w'.dta"
    cap erase "${TEMP_DIR}\heartbeat_`w'.txt"
}

* ── 启动所有worker ──
display _newline "================================================="
display "正在启动 `actual_workers' 个Stata并行实例..."
display "================================================="

forvalues w = 1/`actual_workers' {
    winexec ${STATA_EXE} /e do "${TEMP_DIR}\worker_`w'.do"
    display "  Worker `w' 已启动"
}

*=================================================
*  第三步  等待worker完成（心跳检测）
*=================================================

display _newline "等待所有worker完成..."

forvalues w = 1/`actual_workers' {
    local hb_progress_`w' = -1
    local hb_stall_`w' = 0
}

local elapsed = 0
local all_done = 0
local last_n_done = 0
while `all_done' == 0 {
    sleep 2000
    local elapsed = `elapsed' + 2
    local all_done = 1
    local n_done = 0

    forvalues w = 1/`actual_workers' {
        cap confirm file "${TEMP_DIR}\done_`w'.txt"
        if _rc == 0 {
            local n_done = `n_done' + 1
            continue
        }
        local all_done = 0

        * 读心跳
        cap file open __hbr using "${TEMP_DIR}\heartbeat_`w'.txt", read
        if _rc == 0 {
            file read __hbr __hb_line
            file close __hbr
            local cur_prog = real("`__hb_line'")
            if `cur_prog' == . local cur_prog = -1

            if `cur_prog' > `hb_progress_`w'' {
                local hb_progress_`w' = `cur_prog'
                local hb_stall_`w' = 0
            }
            else {
                local hb_stall_`w' = `hb_stall_`w'' + 2
            }
        }
        else {
            local hb_stall_`w' = `hb_stall_`w'' + 2
        }

        if `hb_stall_`w'' >= ${HEARTBEAT_STALL} & mod(`hb_stall_`w'', 60) == 0 {
            display as error "【警告】Worker `w' 已 `hb_stall_`w'' 秒无进展（进度停留在 `hb_progress_`w''）"
        }
    }

    * 有新worker完成
    if `n_done' > `last_n_done' {
        display "  [`elapsed's] Worker完成 `n_done'/`actual_workers'"
        preserve
        clear
        local has_any = 0
        forvalues w = 1/`actual_workers' {
            cap confirm file "${TEMP_DIR}\done_`w'.txt"
            if _rc == 0 {
                cap append using "${TEMP_DIR}\result_`w'.dta"
                if _rc == 0 local has_any = 1
            }
        }
        if `has_any' == 1 {
            qui keep if converged == 1
            qui count
            if r(N) > 0 {
                gsort -t_val
                local interim_t : display %9.4f t_val[1]
                local interim_combo = combo[1]
                display "    当前最优 |t| =`interim_t'  组合: `interim_combo'"
            }
        }
        restore
        local last_n_done = `n_done'
    }
    * 每30秒兜底汇报
    else if `all_done' == 0 & mod(`elapsed', 30) == 0 {
        local total_progress = 0
        forvalues w = 1/`actual_workers' {
            cap confirm file "${TEMP_DIR}\done_`w'.txt"
            if _rc == 0 continue
            if `hb_progress_`w'' > 0 {
                local total_progress = `total_progress' + `hb_progress_`w''
            }
        }
        display "  [`elapsed's] 完成 `n_done'/`actual_workers' worker，运行中worker合计已处理 `total_progress' 个组合"
    }

    * 全部停滞才报错
    if `all_done' == 0 & `n_done' < `actual_workers' {
        local all_stalled = 1
        forvalues w = 1/`actual_workers' {
            cap confirm file "${TEMP_DIR}\done_`w'.txt"
            if _rc == 0 continue
            if `hb_stall_`w'' < ${HEARTBEAT_STALL} {
                local all_stalled = 0
            }
        }
        if `all_stalled' == 1 {
            display as error "【错误】所有运行中的worker均已停滞超过 ${HEARTBEAT_STALL} 秒，判定为崩溃。"
            display as error "请检查 ${TEMP_DIR} 下的 worker do/log 文件。"
            error 430
        }
    }
}

display "所有worker已完成！耗时约 `elapsed' 秒"

*=================================================
*  第四步  汇总结果 + 汇报Top 10
*=================================================

clear
forvalues w = 1/`actual_workers' {
    cap confirm file "${TEMP_DIR}\result_`w'.dta"
    if _rc == 0 {
        append using "${TEMP_DIR}\result_`w'.dta"
    }
    else {
        display as error "警告：Worker `w' 结果文件缺失"
    }
}

qui count if converged == 0
local n_failed = r(N)
if `n_failed' > 0 {
    display _newline as error "警告：有 `n_failed' 个组合回归未收敛（已排除）"
}

qui keep if converged == 1
qui count
local n_valid = r(N)

if `n_valid' == 0 {
    display as error "所有组合回归均失败，无法继续。"
    error 498
}

gsort -t_val
save "${PROJ_DIR}\控制变量组合搜索结果.dta", replace

* ── 汇报 Top 10 ──
local approx_nobs = n_obs[1]
local approx_df = `approx_nobs' - 10
local crit_t = invttail(`approx_df', $significance / 2)

display _newline "================================================="
display "并行搜索完毕！共 `n_valid' 个有效组合"
display "显著性水平: $significance （近似临界 |t| ≈ " %6.3f `crit_t' "）"
display "================================================="
display _newline "────────────────────────────────────────────────"
display "排名     |t|        β        SE        N    控制变量组合"
display "────────────────────────────────────────────────"

local show_n = min(10, `n_valid')
forvalues i = 1/`show_n' {
    local r_t  : display %9.4f t_val[`i']
    local r_b  : display %9.4f b_val[`i']
    local r_se : display %9.4f se_val[`i']
    local r_n  : display %7.0f n_obs[`i']
    local r_combo = combo[`i']
    local sig_mark = ""
    if t_val[`i'] >= `crit_t' {
        local sig_mark " ***"
    }
    display " `i'    `r_t'  `r_b'  `r_se'  `r_n'    `r_combo'`sig_mark'"
}
display "────────────────────────────────────────────────"

local global_best_t     = t_val[1]
local global_best_combo = combo[1]
local global_best_id    = tuple_id[1]

display _newline "最优控制变量组合 (第`global_best_id'种):"
display "  控制变量: $mandatoryControls `global_best_combo'"
display "  |t| = " %9.4f `global_best_t'

global controlVariables "${mandatoryControls} `global_best_combo'"
display _newline "完整结果已保存至: ${PROJ_DIR}\控制变量组合搜索结果.dta"

*=================================================
*  第五步  最优组合回归展示
*=================================================

use "${PROJ_DIR}\<<DATA_FILE>>", clear

display _newline "================================================="
display "最优组合回归结果："
display "================================================="
${model_cmd} $dependentVariable $independentVariable $controlVariables , ${model_absorb} ${model_vce}

*=================================================
*  第六步  清理
*=================================================

cap erase "${TEMP_DIR}\tuples_list.dta"
forvalues w = 1/$N_WORKERS {
    cap erase "${TEMP_DIR}\worker_`w'.do"
    cap erase "${TEMP_DIR}\result_`w'.dta"
    cap erase "${TEMP_DIR}\done_`w'.txt"
    cap erase "${TEMP_DIR}\heartbeat_`w'.txt"
}
shell rd /s /q "${TEMP_DIR}" 2>nul

display _newline "================================================="
display "全部完成！临时文件已清理。"
display "最终控制变量: $controlVariables"
display "================================================="
