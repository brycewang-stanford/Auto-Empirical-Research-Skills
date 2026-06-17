# WRDS Data Map — 跨国/美国公司金融研究数据资产

**Source**: WRDS Research Database Overview (June 2020) + 2024-2025 数据库更新
**用途**：Phase 0 数据可行性扫描；Phase 6 最终验证

---

## 0. Geographic Coverage 速查表

### Cross-Country / Global 数据资产

| 数据集 | 内容 | 时间覆盖 | 国别覆盖 | 关键限制 |
|--------|------|---------|---------|---------|
| **Compustat Global** | 公司基本面（资产负债表、利润表、现金流） | 1989+ | 80+ 国 | 中国 2010 后稀疏；新兴市场早期数据缺失多 |
| **WorldScope (TR)** | 公司基本面（替代 Compustat Global） | 1980+ | 60+ 国 | 与 Compustat Global 互补但 firm-id 不同 |
| **Orbis (Bureau van Dijk)** | 全球公开 + 私募公司 | 1990s+ | 200+ 国 | 私募公司数据质量不一；财务报表完整性差 |
| **FactSet Fundamentals** | 公司基本面 + segment | 1990s+ | 100+ 国 | 与 Compustat 互补 |
| **I/B/E/S International** | 分析师预测 / Guidance / Actual | **1987+** | 60+ 国 | 美国 1975+，国际从 1987 |
| **BoardEx** | 高管 + 董事 + 股权结构 | **1999+** US, 2000s+ Global | US + Global | 早期非美国数据稀疏 |
| **TR Global Ownership (OP feed)** | 机构 + 共同基金持股（type 2 / 3） | 1999+ | 全球 | US + 非 US 集中度有差异 |
| **Compustat Global Pricing** | 股价、回报、市值 | 1989+ | 80+ 国 | 与 Compustat Global 同步 |
| **Markit CDS** | CDS 利差 | 2003+ | 主要 OECD | 中国 / 印度等覆盖差 |
| **Markit Security Finance** | 卖空数据 | 2002+ | 全球主要市场 | |
| **Preqin** | PE / VC / 私募信贷 | 1990s+ | 全球 | LP-GP 关系；交易细节不全 |
| **Sustainalytics** | ESG 评分 | 2009+ | 全球 | |
| **RepRisk** | ESG 事件 / 媒体监测 | 2007+ | 全球 | |
| **MSCI ESG KLD** | ESG 评分 | 1991+ (KLD legacy) | US + Global | 跨厂商不一致（Berg-Koelbel-Rigobon 2022） |
| **Capital IQ** | 公司基本面 + key developments | 1990s+ | 100+ 国 | |
| **Capital IQ People Intelligence** | 高管 + 私募合伙人 + R&D 中心 | 2000s+ | 全球 | |
| **TR SDC Platinum** | 跨境 M&A + IPO + SEO | 1980+ | 全球 | M&A target/acquirer 国别清晰 |
| **TR DealScan** | 商业贷款 | 1981+ | 全球（美国主导） | 银团贷款全球覆盖 |
| **Mergent FISD** | 公司债特征 + 评级 | 1990+ | 全球 | |
| **Lipper Hedge Fund (TASS)** | 对冲基金 | 1990+ | 全球 | 报告偏差 |
| **EurekaHedge Indices** | 对冲基金指数 | 1999+ | 亚太重点 | |
| **Revelio Labs** | 全球员工 panel + 简历 + 跳槽 | 2008+ | **180+ 国** | 2025-03 launches Employee-Linked Patents |

### US-Only 数据资产

| 数据集 | 内容 | 时间覆盖 | 关键限制 |
|--------|------|---------|---------|
| **CRSP** | 美股价 / 回报 / 成交量 / 市值（日 + 月） | 1925/1962+ | 美国 only |
| **TAQ** | 高频交易（日内） | 1993+ | 美国 only |
| **Compustat NA** | 美国 + 加拿大公司基本面 | 1950+ | 加拿大覆盖较薄 |
| **Compustat ExecuComp** | S&P 1500 高管薪酬 | **1992+** | S&P 1500 only |
| **TRACE** | 公司债成交 | 2002+ | 美国 only |
| **MSRB** | 市政债成交 | 2005+ | 美国 only |
| **WRDS Bond Returns** | 预算公司债回报 | 2002+ | 美国 only |
| **WRDS-SEC Insider** | 内部人交易 | 2003+ | 美国 only |
| **TR Insider** | 内部人交易（legacy） | 1986+ | 美国 only |
| **TR 13F (legacy SP feed)** | 美国机构持股 | 1980+ | 美国 only |
| **WRDS-SEC 13F** | 美国 13F + 修订 | 2013+ | 美国 only |
| **CRSP Mutual Fund Database** | 美国 MF 回报 / NAV / fee | 1960s+ | 美国 only |
| **MFLINKS** | CRSP MFDB ⇄ TR SP 链接 | 1960s+ | 美国 only |
| **WRDS SEC Analytics** | 10-K / 10-Q / 8-K 文本 | 1994+ | 美国 only |
| **OptionMetrics (US/Europe)** | 期权价格 + IV + greeks | 1996+ | 美国 + 欧洲 |
| **ISS (formerly RiskMetrics, IRRC)** | 公司治理 + 董事会 | 1996+ | 美国主导 |
| **Audit Analytics** | 审计 + 重述 + 股东行为 | 2000+ | 美国主导 |
| **Zacks** | 美国分析师预测 | 1980+ | 美国 only |
| **TR Mutual Fund (legacy SP feed)** | 美国 MF holdings | 1980+ | 美国 only |
| **Markit Security Finance** | 卖空 | 2002+ | 全球但美国数据最完整 |
| **NBER Patent Data / USPTO PatentsView** | 美国专利（2025 起 USPTO 停 PatentsView） | 1976+ | 美国 only（USPTO） |

---

## 1. 按研究主题快速匹配

### 跨国主题（cross-country）→ 推荐数据组合

| 主题 | 数据组合 | 适合的 Y |
|------|---------|---------|
| **Cross-border M&A** | Compustat Global + SDC + BoardEx + WorldScope | M&A CAR、撤资、整合后绩效 |
| **跨国 ESG/CSR** | Compustat Global + Sustainalytics/RepRisk + I/B/E/S Intl | 公司估值、信贷利差、披露 |
| **跨国劳动力（含 AI/绿色技能）** | Revelio Labs + Compustat Global + BoardEx | 招聘速度、技能分布、性别 |
| **跨国治理** | BoardEx Global + ISS + Compustat Global | CEO 替换、薪酬、风险承担 |
| **跨国地缘政治 / 贸易** | Compustat Global + RavenPack + SDC + DealScan | 跨境投融资、利率溢价 |
| **跨国 PE / 私募信贷** | Preqin + Compustat Global + DealScan + Revelio | LBO 后果、信贷市场份额 |
| **跨国税务规避** | Compustat Global + WorldScope + ExecuComp + OECD CbCR | ETR、profit shifting |
| **跨国创新与发明者** | Compustat Global + USPTO/EPO + Revelio + BoardEx | R&D 重新部署、专利质量 |
| **跨国监管套利** | Compustat Global + RepRisk + BoardEx | 公司迁徙、合规成本 |

### 美国主题（US-only）→ 推荐数据组合

| 主题 | 数据组合 | 适合的 Y |
|------|---------|---------|
| **美国公司治理** | ExecuComp + ISS + BoardEx + CRSP | CEO 薪酬、turnover-perf 敏感 |
| **美国披露与盈余** | WRDS SEC Analytics + Audit Analytics + I/B/E/S | 自愿披露、conference call |
| **美国机构投资者** | TR 13F + CRSP MFDB + MFLINKS + Insider | 共同所有权、stewardship |
| **美国债务市场** | TRACE + Mergent FISD + DealScan | 信贷利差、契约 |
| **美国劳动力金融** | Revelio + Compustat NA + ExecuComp + Audit Analytics | 工人福利、tax avoidance |
| **美国 PE / Buyout** | Preqin + Compustat NA + DealScan + Revelio | 员工保留、创新 |
| **美国创新** | NBER/USPTO + Compustat NA + ExecuComp | 专利质量、R&D |
| **美国 ESG** | MSCI ESG KLD + Sustainalytics + RepRisk + Audit Analytics | ESG 处罚、绿色资本 |
| **美国 IPO/SEO** | SDC + CRSP + Compustat NA + ExecuComp | IPO 后果、员工激励 |

---

## 2. WRDS 链接表（Linking Suite）

### 关键链接桥
- **CRSP ⇄ Compustat NA**：CCM (CRSP-Compustat Merged) — 美国 PERMNO ⇄ GVKEY
- **CRSP ⇄ TR Mutual Fund**：MFLINKS
- **Compustat Global ⇄ WorldScope**：Datastream/WorldScope ID 桥
- **Compustat Global ⇄ Capital IQ ⇄ Orbis**：ISIN / SEDOL
- **PATSTAT ⇄ Compustat**：通过 firm name fuzzy matching（误差 5-10%）
- **Revelio Worker_ID ⇄ USPTO Inventor_ID**：**2025-03 起** Revelio Employee-Linked Patents 直接提供
- **BoardEx Director_ID ⇄ Capital IQ People**：通过 name + role + tenure 桥

### 跨国研究关键链接
- **Country code**：Compustat Global 用 SIC + ISO + currency；WorldScope 用 country name
- **Industry code**：跨国推荐用 NAICS 4-digit 或 GICS（避免国别 SIC 不一致）

---

## 3. 不在 WRDS 但可补充的关键数据集

| 数据 | 来源 | 用途 |
|------|------|------|
| **OECD EPL Index** | OECD.org | 跨国劳动保护强度 |
| **Hofstede Cultural Dimensions** | Hofstede Insights | 文化距离 |
| **OECD CbCR (Country-by-Country Reporting)** | OECD | 跨国 profit shifting |
| **Hassan-Hollander-van Lent-Tahoun firm-level political risk** | 作者网站 / SSRN | 公司层面政治风险 |
| **Caldara-Iacoviello GPR Index** | Federal Reserve | 国家地缘政治风险 |
| **Sautner climate exposure** | 作者网站 | 公司层面气候风险 |
| **EM-DAT disasters** | EM-DAT.be | 自然灾害事件 |
| **GDELT** | gdeltproject.org | 全球新闻事件 |
| **Bilateral visa policies** | 各国移民部门 | 跨境流动 IV |
| **EU AI Act, CSDDD, UFLPA, Lieferkettengesetz** | EU/各国官方 | 政策事件研究 |
| **Pillar Two implementation** | OECD | 跨国 tax 政策 |

---

## 4. 数据可行性 Risk Levels

### LOW Risk（数据 WRDS 直接可用）
- 标准的 Compustat Global + I/B/E/S Intl + BoardEx 三件套覆盖的题目
- 标准的 CRSP + Compustat NA + ExecuComp 三件套覆盖的美国题目

### MEDIUM Risk（需额外采购或链接工作）
- 需要 Revelio Labs（WRDS 提供但需单独订阅）
- 需要 Preqin（WRDS 提供但 LP/GP 关系细节有限）
- 需要 PATSTAT (USPTO/EPO)（公开但 firm 链接需 fuzzy matching）
- 需要 OECD CbCR（公开但需独立处理）
- 需要 RavenPack（WRDS 提供但 query 限制）

### HIGH Risk（数据不全或不可行）
- 跨国私募公司（Orbis 数据质量不一致）
- 中国公司 + Markit CDS（CDS 在中国覆盖差）
- 跨国 individual-level 工资（除了 Revelio 没有好数据）
- 跨国 ESG 处罚事件（无统一数据库，需手工收集）
- 私募信贷的具体借款人（PitchBook 单独购买，WRDS 不全）

---

## 5. Phase 0 扫描决策树

```
用户方向
   ↓
是否 cross-country？
   ├ Yes → 检查 Compustat Global + WorldScope + I/B/E/S Intl + BoardEx Global 是否覆盖
   │         ├ All Yes → LOW risk
   │         ├ Some No → 检查能否用 Orbis / FactSet 替代
   │         └ Most No → 改 focus 到部分国家或转 US-only
   └ No (US) → 检查 CRSP + Compustat NA + ExecuComp + WRDS SEC + I/B/E/S US
              ├ All Yes → LOW risk
              ├ Need Revelio → MEDIUM risk
              └ Need PATSTAT/USPTO → MEDIUM risk
```
