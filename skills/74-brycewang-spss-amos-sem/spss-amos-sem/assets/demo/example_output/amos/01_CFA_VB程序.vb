' ============================================================================
' 移动支付 App 持续使用意愿研究 —— 验证性因子分析 CFA（由 spss-amos-sem 自动生成）
' 用法：开始菜单打开 IBM SPSS Amos Program Editor → File → New VB Program，
'      把模板里 'Your code goes here 那一行整行替换成下面「从 Dim 到 End Try」的全部内容，
'      再把 BeginGroup 里的路径改成你电脑上的文件，File → Run。
' 注意：这份程序没有在真实 AMOS 里跑过，语法照 IBM Amos 28 用户手册的写法；
'      如果报错，以 Amos Graphics 画图（AMOS操作步骤.md）为准。
' ============================================================================
Dim Sem As New AmosEngine
Try
    Sem.TextOutput()
    Sem.Standardized()
    Sem.Smc()
    Sem.Mods(4)

    Sem.BeginGroup("C:\改成你的文件夹路径\questionnaire_demo_cleaned.sav")

    ' 感知易用性
    Sem.AStructure("PEOU1 <--- PEOU (1)")
    Sem.AStructure("PEOU2 <--- PEOU")
    Sem.AStructure("PEOU3 <--- PEOU")
    Sem.AStructure("PEOU4 <--- PEOU")
    Sem.AStructure("PEOU1 <--- e1 (1)")
    Sem.AStructure("PEOU2 <--- e2 (1)")
    Sem.AStructure("PEOU3 <--- e3 (1)")
    Sem.AStructure("PEOU4 <--- e4 (1)")
    ' 感知有用性
    Sem.AStructure("PU1 <--- PU (1)")
    Sem.AStructure("PU2 <--- PU")
    Sem.AStructure("PU3 <--- PU")
    Sem.AStructure("PU4 <--- PU")
    Sem.AStructure("PU1 <--- e5 (1)")
    Sem.AStructure("PU2 <--- e6 (1)")
    Sem.AStructure("PU3 <--- e7 (1)")
    Sem.AStructure("PU4 <--- e8 (1)")
    ' 信任
    Sem.AStructure("TR1 <--- TR (1)")
    Sem.AStructure("TR2 <--- TR")
    Sem.AStructure("TR3 <--- TR")
    Sem.AStructure("TR1 <--- e9 (1)")
    Sem.AStructure("TR2 <--- e10 (1)")
    Sem.AStructure("TR3 <--- e11 (1)")
    ' 满意度
    Sem.AStructure("SAT1 <--- SAT (1)")
    Sem.AStructure("SAT2 <--- SAT")
    Sem.AStructure("SAT3 <--- SAT")
    Sem.AStructure("SAT1 <--- e12 (1)")
    Sem.AStructure("SAT2 <--- e13 (1)")
    Sem.AStructure("SAT3 <--- e14 (1)")
    ' 持续使用意愿
    Sem.AStructure("CI1 <--- CI (1)")
    Sem.AStructure("CI2 <--- CI")
    Sem.AStructure("CI3 <--- CI")
    Sem.AStructure("CI1 <--- e15 (1)")
    Sem.AStructure("CI2 <--- e16 (1)")
    Sem.AStructure("CI3 <--- e17 (1)")

    ' 误差相关（模型修正，理由见 模型修正记录.md）
    Sem.AStructure("e12 <> e13")

    Sem.FitModel()
Finally
    Sem.Dispose()
End Try
