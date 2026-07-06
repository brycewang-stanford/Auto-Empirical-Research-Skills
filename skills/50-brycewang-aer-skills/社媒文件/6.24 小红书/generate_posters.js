const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
const { pathToFileURL } = require("url");

const OUT_DIR = __dirname;
const REPO_ROOT = path.resolve(OUT_DIR, "../..");
const FONT_DIR = "/Users/brycewang/.codex/skills/canvas-design/canvas-fonts";
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const W = 1080;
const H = 1920;
const REPO_URL = "github.com/brycewang-stanford/AER-Skills";
const COVER_SVG = path.join(REPO_ROOT, "assets", "aer-cover-official.svg");
const COVER_PNG = path.join(REPO_ROOT, "assets", "aer-cover-official.png");
const COVER_FALLBACK = path.join(REPO_ROOT, "assets", "aer-cover.jpg");
const COVER_URL = pathToFileURL(
  fs.existsSync(COVER_SVG) ? COVER_SVG : fs.existsSync(COVER_PNG) ? COVER_PNG : COVER_FALLBACK
).href;

function fontUrl(file) {
  return pathToFileURL(path.join(FONT_DIR, file)).href;
}

function esc(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function writeDesignPhilosophy() {
  const text = `# Editorial Harbor

Editorial Harbor treats the page as a working desk between two dark institutional bands. The header and footer are deep navy, almost archival, while the center is a pale blue field where the argument is assembled with restraint. The design should feel meticulously crafted: every block is aligned to a quiet grid, every label has a defined role, and the page reads like a master-level editorial object rather than a screenshot.

Color carries the repository's logic. AER maroon enters through the opening cover background and small route marks; electric blue marks the active agent layer; warm orange signals the human editorial decision. These accents must be sparse and calibrated with painstaking attention, so the light center remains clean and readable. The final set should look labored over by someone at the top of their field, with no stray decoration and no cheap visual noise.

The AER cover is not a pasted decoration. It is the opening environment: a large institutional artifact behind the first page, giving the poster stack its journal target and severity. After that first page, the series relies on workflow diagrams, scorecards, repository gates, and manuscript-routing surfaces without repeating the cover image. Information is expressed through spatial order first, then short labels; paragraphs are replaced by disciplined fragments.

Typography is phone-first: every headline, node, and command must remain legible in a compressed mobile feed, with fewer words and larger type replacing explanatory density. Chinese headlines carry the argument; English monospace labels pin the repo mechanics to the grid. The result should have the feel of a carefully proofed journal production board, with the craft of a polished social campaign and the restraint of an AER submission checklist.

Across the five pages, variation comes from composition rather than palette drift: an AER journal-information opening page, then four stripped-down title posters carrying only the AER-Skills name. The system must remain unmistakably one set. Every poster should feel like the product of countless small refinements, where hierarchy and margins have been tuned until the visual argument is obvious at a glance.
`;
  fs.writeFileSync(path.join(OUT_DIR, "design-philosophy.md"), text);
}

function coverImg(className = "aer-cover") {
  return `<img class="${className}" src="${COVER_URL}" alt="American Economic Review cover" />`;
}

function baseCss() {
  return `
@font-face { font-family: "Work Sans Local"; src: url("${fontUrl("WorkSans-Regular.ttf")}") format("truetype"); font-weight: 400; }
@font-face { font-family: "Work Sans Local"; src: url("${fontUrl("WorkSans-Bold.ttf")}") format("truetype"); font-weight: 700; }
@font-face { font-family: "Bricolage Local"; src: url("${fontUrl("BricolageGrotesque-Bold.ttf")}") format("truetype"); font-weight: 700; }
@font-face { font-family: "JetBrains Mono Local"; src: url("${fontUrl("JetBrainsMono-Regular.ttf")}") format("truetype"); font-weight: 400; }
@font-face { font-family: "IBM Plex Serif Local"; src: url("${fontUrl("IBMPlexSerif-Bold.ttf")}") format("truetype"); font-weight: 700; }
* { box-sizing: border-box; }
html, body {
  width: ${W}px;
  height: ${H}px;
  margin: 0;
  overflow: hidden;
  background: #061b2d;
}
body {
  font-family: "Work Sans Local", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
}
.poster {
  --navy: #061b2d;
  --navy-2: #0b2439;
  --sky: #e8f6ff;
  --blue: #1594f6;
  --blue-2: #0e79d8;
  --maroon: #751e38;
  --orange: #e87345;
  --gold: #f5c04c;
  --ink: #092034;
  --muted: #527084;
  --line: rgba(9, 32, 52, .16);
  --paper: #fbfdff;
  position: relative;
  width: ${W}px;
  height: ${H}px;
  overflow: hidden;
  color: var(--ink);
  background: var(--navy);
}
.header,
.footer {
  position: absolute;
  left: 0;
  right: 0;
  background: var(--navy);
  color: #f4fbff;
}
.header { top: 0; height: 154px; }
.footer { bottom: 0; height: 178px; }
.stage {
  position: absolute;
  left: 0;
  right: 0;
  top: 154px;
  height: 1588px;
  background:
    linear-gradient(180deg, rgba(255,255,255,.34), rgba(255,255,255,0) 35%),
    var(--sky);
}
.stage::before {
  content: "";
  position: absolute;
  left: 70px;
  right: 70px;
  top: 72px;
  height: 1px;
  background: rgba(9, 32, 52, .08);
}
.brand {
  position: absolute;
  left: 78px;
  top: 43px;
  height: 78px;
  min-width: 330px;
  display: flex;
  align-items: center;
  padding: 0 26px;
  border-radius: 8px;
  background: #101a2c;
  box-shadow: 0 1px 0 rgba(255,255,255,.06) inset;
}
.brand-text {
  font-size: 38px;
  line-height: 1;
  font-weight: 700;
  letter-spacing: 0;
}
.series {
  position: absolute;
  right: 78px;
  top: 52px;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 24px;
  line-height: 1.35;
  color: rgba(244,251,255,.72);
  text-align: right;
}
.series strong {
  display: block;
  color: #f4fbff;
  font-size: 32px;
  font-weight: 400;
}
.footer .url {
  position: absolute;
  left: 78px;
  top: 44px;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 32px;
  line-height: 1.2;
  color: #ffffff;
}
.footer .cmd {
  position: absolute;
  left: 78px;
  top: 95px;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 27px;
  line-height: 1.3;
  color: #b7cede;
}
.footer .mark {
  position: absolute;
  right: 78px;
  top: 48px;
  display: flex;
  gap: 10px;
}
.footer .mark span {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--blue);
}
.footer .mark span:nth-child(2) { background: var(--maroon); }
.footer .mark span:nth-child(3) { background: var(--orange); }
.kicker,
.mono,
.chip,
.small-label,
.node,
.metric-number,
.command,
.skill,
.dimension,
.stack-card {
  font-family: "JetBrains Mono Local", monospace;
  letter-spacing: 0;
}
.wrap {
  position: absolute;
  left: 70px;
  right: 70px;
  top: 86px;
  bottom: 86px;
}
.kicker {
  display: inline-flex;
  align-items: center;
  height: 36px;
  padding: 0 13px;
  border-radius: 8px;
  background: rgba(117, 30, 56, .12);
  color: var(--maroon);
  font-size: 20px;
  text-transform: uppercase;
}
.kicker.blue {
  background: rgba(21, 148, 246, .12);
  color: var(--blue-2);
}
.title {
  margin: 0;
  font-weight: 700;
  letter-spacing: 0;
  color: var(--ink);
}
.title strong {
  color: var(--blue);
  font-weight: 700;
}
.subtitle {
  margin: 0;
  font-size: 40px;
  line-height: 1.34;
  color: #183c55;
  font-weight: 700;
}
.subtitle em {
  color: var(--maroon);
  font-style: normal;
}
.panel {
  border-radius: 8px;
  background: rgba(255, 255, 255, .78);
  border: 2px solid rgba(9, 32, 52, .10);
  box-shadow: 0 18px 36px rgba(6, 27, 45, .08);
}
.blue-panel {
  border-radius: 8px;
  background: var(--blue);
  color: #ffffff;
  box-shadow: 0 22px 45px rgba(21, 148, 246, .28);
}
.maroon-panel {
  border-radius: 8px;
  background: var(--maroon);
  color: #ffffff;
  box-shadow: 0 22px 45px rgba(117, 30, 56, .20);
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.chip {
  height: 58px;
  display: inline-flex;
  align-items: center;
  padding: 0 20px;
  border-radius: 8px;
  background: #ffffff;
  border: 2px solid rgba(21, 148, 246, .35);
  color: #12324b;
  font-size: 21px;
}
.chip.dark {
  background: var(--navy);
  border-color: rgba(255,255,255,.18);
  color: #f4fbff;
}
.rule {
  width: 100%;
  height: 2px;
  background: var(--line);
}
`;
}

function page(title, body, extraCss = "") {
  return `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=${W}, initial-scale=1" />
<title>${esc(title)}</title>
<style>${baseCss()}${extraCss}</style>
</head>
<body>${body}</body>
</html>`;
}

function shell(pageNo, title, body, command = "make preflight") {
  return `<main class="poster">
    <header class="header">
      <div class="brand"><div class="brand-text">AER-Skills</div></div>
      <div class="series">XHS POSTER<strong>${pageNo}/05</strong></div>
    </header>
    <section class="stage">${body}</section>
    <footer class="footer">
      <div class="url">${REPO_URL}</div>
      <div class="cmd">${esc(command)}</div>
      <div class="mark" aria-hidden="true"><span></span><span></span><span></span></div>
    </footer>
  </main>`;
}

function poster01() {
  const css = `
.p1-bg {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  pointer-events: none;
}
.p1-bg::after {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(232,246,255,.88) 0%, rgba(232,246,255,.66) 43%, rgba(232,246,255,.30) 100%),
    linear-gradient(180deg, rgba(232,246,255,.95) 0%, rgba(232,246,255,.38) 48%, rgba(232,246,255,.88) 100%);
}
.p1 .aer-cover-bg {
  width: 1160px;
  height: 1680px;
  object-fit: cover;
  object-position: center;
  opacity: .32;
  transform: translateX(72px) rotate(-1.2deg);
  filter: saturate(.96) contrast(1.08);
}
.p1 .hero {
  display: none;
}
.p1 .title {
  display: none;
}
.p1 .subtitle {
  display: none;
}
.p1 .journal-lockup {
  position: absolute;
  left: 70px;
  top: 720px;
  width: 840px;
  padding: 52px 54px 54px;
  border-radius: 8px;
  background: rgba(117, 30, 56, .92);
  color: #ffffff;
  box-shadow: 0 28px 60px rgba(117, 30, 56, .20);
}
.p1 .journal-name {
  font-family: "IBM Plex Serif Local", serif;
  font-size: 84px;
  line-height: .98;
  letter-spacing: 0;
}
.p1 .journal-meta {
  margin-top: 30px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}
.p1 .journal-meta span {
  min-height: 78px;
  padding: 16px 14px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,.28);
  background: rgba(255,255,255,.12);
  font-family: "JetBrains Mono Local", monospace;
  font-size: 18px;
  line-height: 1.24;
}
.p1 .journal-meta b {
  display: block;
  margin-bottom: 5px;
  font-size: 22px;
  line-height: 1;
  color: #ffffff;
}
.p1 .aer-skills-title {
  position: absolute;
  left: 60px;
  top: 250px;
  width: 960px;
  margin: 0;
  color: var(--blue);
  font-family: "Times New Roman", Times, serif;
  font-size: 168px;
  line-height: .9;
  font-weight: 700;
  letter-spacing: 0;
  white-space: nowrap;
  text-shadow: 0 18px 42px rgba(21, 148, 246, .18), 0 2px 0 rgba(255,255,255,.72);
}
.p1 .question {
  position: absolute;
  left: 66px;
  top: 438px;
  width: 900px;
  margin: 0;
  color: #092034;
  font-family: "Work Sans Local", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 88px;
  line-height: 1.08;
  font-weight: 700;
  letter-spacing: 0;
  text-shadow: 0 2px 0 rgba(255,255,255,.70);
}
`;
  return page(
    "Poster 01 - AER-Skills",
    shell(
      "01",
      "AER-Skills",
      `<div class="p1-bg">${coverImg("aer-cover-bg")}</div>
      <div class="wrap p1">
        <div class="journal-lockup">
          <div class="journal-name">The American<br>Economic Review</div>
          <div class="journal-meta">
            <span><b>1911</b>established</span>
            <span><b>ISSN</b>0002-8282</span>
            <span><b>12</b>issues / year</span>
          </div>
        </div>
        <h1 class="aer-skills-title">AER-Skills</h1>
        <p class="question">如何用 Agent<br>快速发表一篇 AER？</p>
      </div>`,
      "python3 scripts/validate_repo.py"
    ),
    css
  );
}

function poster02() {
  const css = `
.p2 .title {
  position: absolute;
  left: 70px;
  top: 190px;
  width: 920px;
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 138px;
  line-height: .95;
}
.p2 .subtitle {
  position: absolute;
  left: 70px;
  top: 372px;
  width: 780px;
  font-size: 43px;
  line-height: 1.28;
}
.p2 .route {
  display: none;
}
.p2 .route-line {
  position: absolute;
  left: 92px;
  right: 92px;
  top: 156px;
  height: 8px;
  border-radius: 4px;
  background: rgba(255,255,255,.68);
}
.p2 .node {
  position: relative;
  z-index: 2;
  width: 176px;
  height: 176px;
  border-radius: 50%;
  background: #ffffff;
  color: var(--ink);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 24px;
  line-height: 1.18;
  font-weight: 400;
}
.p2 .nodes {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.p2 .node:nth-child(2) { background: var(--gold); }
.p2 .node:nth-child(3) { background: var(--maroon); color: #ffffff; }
.p2 .node:nth-child(4) { background: #ffffff; box-shadow: inset 0 0 0 6px var(--blue); }
.p2 .method-grid {
  display: none;
}
.p2 .method {
  display: none;
}
.p2 .method b {
  display: block;
  font-size: 29px;
  line-height: 1.15;
  color: var(--ink);
}
.p2 .method span {
  display: block;
  margin-top: 10px;
  font-size: 21px;
  line-height: 1.3;
  color: var(--muted);
}
.p2 .warning {
  display: none;
}
.p2 .stage-mark {
  display: none;
}
.p2 .linear-flow {
  position: absolute;
  left: 70px;
  right: 70px;
  top: 650px;
  height: 360px;
  display: grid;
  grid-template-columns: 1fr 66px 1fr 66px 1fr 66px 1fr;
  align-items: center;
}
.p2 .flow-node {
  height: 200px;
  border-radius: 8px;
  background: rgba(255,255,255,.88);
  border: 2px solid rgba(9,32,52,.12);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 38px;
  line-height: 1.12;
  font-weight: 700;
  box-shadow: 0 18px 34px rgba(6,27,45,.08);
}
.p2 .flow-node.primary {
  background: var(--maroon);
  color: #ffffff;
}
.p2 .flow-arrow {
  text-align: center;
  color: var(--blue);
  font-size: 62px;
  font-weight: 700;
}
.p2 .flow-node.route-choice {
  font-size: 34px;
  line-height: 1.04;
}
.p2 .constraint-grid {
  position: absolute;
  left: 70px;
  right: 70px;
  top: 1025px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.p2 .constraint-card {
  min-height: 212px;
  padding: 24px 20px;
  border-radius: 8px;
  background: rgba(255,255,255,.86);
  border: 2px solid rgba(9,32,52,.10);
  box-shadow: 0 16px 30px rgba(6,27,45,.07);
}
.p2 .constraint-card b {
  display: block;
  margin-bottom: 16px;
  color: var(--maroon);
  font-size: 31px;
  line-height: 1.08;
}
.p2 .constraint-card span {
  display: block;
  color: #14324a;
  font-size: 24px;
  line-height: 1.22;
  font-weight: 700;
}
.p2 .constraint-card code {
  display: inline-block;
  margin-top: 12px;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 18px;
  color: var(--blue-2);
}
.p2 .method-strip {
  position: absolute;
  left: 70px;
  right: 70px;
  top: 1270px;
  min-height: 92px;
  padding: 22px 26px;
  border-radius: 8px;
  background: var(--navy);
  color: #d7edf9;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 25px;
  line-height: 1.35;
}
.p2 .method-strip strong {
  color: var(--gold);
  font-weight: 400;
}
`;
  return page(
    "Poster 02 - Identification First",
    shell(
      "02",
      "Identification First",
      `<div class="wrap p2">
        <h1 class="title">AER-Skills</h1>
        <p class="subtitle">Top-5 选刊 + 识别优先</p>
        <div class="linear-flow" aria-label="AER-Skills identification workflow">
          <div class="flow-node">贡献<br>一句话</div>
          <div class="flow-arrow">→</div>
          <div class="flow-node route-choice">AER<br>Insights<br>AEJ</div>
          <div class="flow-arrow">→</div>
          <div class="flow-node primary">识别<br>先行</div>
          <div class="flow-arrow">→</div>
          <div class="flow-node">稳健<br>机制</div>
        </div>
        <div class="constraint-grid">
          <div class="constraint-card"><b>选刊先行</b><span>摘要前决定 AER / Insights / AEJ</span><code>aer-topic-selection</code></div>
          <div class="constraint-card"><b>引用核验</b><span>最近邻论文地图，拒绝凭记忆引用</span><code>aer-literature</code></div>
          <div class="constraint-card"><b>现代计量</b><span>DiD / IV / RDD 先过方法门</span><code>aer-identification</code></div>
        </div>
        <div class="method-strip"><strong>Defaults</strong>  TWFE → CS/BJS · weak IV → AR · RDD → local linear</div>
      </div>`,
      "aer-topic-selection -> aer-identification"
    ),
    css
  );
}

function poster03() {
  const skills = [
    "topic-selection",
    "literature",
    "identification",
    "robustness",
    "paper-body",
    "introduction",
    "tables-figures",
    "consistency",
    "referee-sim",
    "replication",
    "submission",
    "rebuttal",
    "statspai",
    "workflow",
  ];
  const skillTags = skills
    .map((name, i) => `<div class="skill"><span>${String(i + 1).padStart(2, "0")}</span>aer-${name}</div>`)
    .join("");
  const css = `
.p3 .title {
  position: absolute;
  left: 70px;
  top: 190px;
  width: 920px;
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 138px;
  line-height: .95;
}
.p3 .subtitle {
  position: absolute;
  left: 70px;
  top: 372px;
  width: 780px;
  font-size: 43px;
  line-height: 1.28;
}
.p3 .workflow-core {
  display: none;
}
.p3 .workflow-core b {
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 74px;
  line-height: 1;
}
.p3 .workflow-core span {
  width: 260px;
  font-size: 27px;
  line-height: 1.22;
  font-weight: 700;
  color: rgba(255,255,255,.84);
}
.p3 .skill-grid {
  display: none;
}
.p3 .skill {
  height: 58px;
  padding: 0 17px;
  display: flex;
  align-items: center;
  gap: 13px;
  border-radius: 8px;
  background: rgba(255,255,255,.86);
  border: 1px solid rgba(9,32,52,.12);
  color: #14324a;
  font-size: 20px;
}
.p3 .skill span {
  color: var(--blue-2);
}
.p3 .three-lanes {
  display: none;
}
.p3 .lane {
  height: 156px;
  padding: 22px 18px;
  text-align: center;
}
.p3 .lane b {
  display: block;
  font-size: 28px;
  line-height: 1.15;
}
.p3 .lane span {
  display: block;
  margin-top: 13px;
  font-size: 20px;
  line-height: 1.25;
  color: var(--muted);
}
.p3 .stage-mark {
  display: none;
}
.p3 .cycle {
  position: absolute;
  left: 132px;
  top: 500px;
  width: 760px;
  height: 760px;
}
.p3 .cycle-ring {
  position: absolute;
  inset: 86px;
  border-radius: 50%;
  border: 10px solid rgba(21,148,246,.32);
  border-top-color: var(--maroon);
  border-right-color: var(--blue);
}
.p3 .cycle-center {
  position: absolute;
  left: 255px;
  top: 292px;
  width: 250px;
  height: 160px;
  border-radius: 8px;
  background: var(--blue);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 40px;
  line-height: 1.15;
  font-weight: 700;
  box-shadow: 0 22px 42px rgba(21,148,246,.24);
}
.p3 .cycle-arrow {
  position: absolute;
  left: 334px;
  top: 114px;
  font-size: 76px;
  color: var(--maroon);
  line-height: 1;
}
.p3 .cycle-node {
  position: absolute;
  width: 252px;
  height: 142px;
  border-radius: 8px;
  background: rgba(255,255,255,.92);
  border: 2px solid rgba(9,32,52,.12);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 42px;
  line-height: 1.02;
  font-weight: 700;
  box-shadow: 0 16px 30px rgba(6,27,45,.08);
}
.p3 .cycle-node small {
  display: block;
  margin-top: 8px;
  font-size: 29px;
  line-height: 1.05;
}
.p3 .n1 { left: 254px; top: 0; }
.p3 .n2 { right: 0; top: 309px; }
.p3 .n3 { left: 254px; bottom: 0; }
.p3 .n4 { left: 0; top: 309px; }
.p3 .skill-groups {
  position: absolute;
  left: 70px;
  right: 70px;
  top: 1264px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}
.p3 .skill-group {
  height: 86px;
  padding: 12px 18px;
  border-radius: 8px;
  background: rgba(255,255,255,.88);
  border: 2px solid rgba(9,32,52,.10);
  box-shadow: 0 12px 24px rgba(6,27,45,.06);
}
.p3 .skill-group b {
  display: block;
  margin-bottom: 6px;
  color: var(--maroon);
  font-size: 24px;
  line-height: 1;
}
.p3 .skill-group span {
  display: block;
  color: #14324a;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 15px;
  line-height: 1.12;
}
`;
  return page(
    "Poster 03 - 14 Skills",
    shell(
      "03",
      "Fourteen Skills",
      `<div class="wrap p3">
        <h1 class="title">AER-Skills</h1>
        <p class="subtitle">14 个 skill 生命周期</p>
        <div class="cycle" aria-label="AER-Skills lifecycle cycle">
          <div class="cycle-ring"></div>
          <div class="cycle-arrow">↻</div>
          <div class="cycle-center">14<br>Skills</div>
          <div class="cycle-node n1">路由<small>选题+文献</small></div>
          <div class="cycle-node n2">设计<small>识别+稳健</small></div>
          <div class="cycle-node n3">写作<small>正文+表图</small></div>
          <div class="cycle-node n4">提交<small>内审+复现</small></div>
        </div>
        <div class="skill-groups">
          <div class="skill-group"><b>Route</b><span>workflow · topic · lit</span></div>
          <div class="skill-group"><b>Design</b><span>id · robust · statspai</span></div>
          <div class="skill-group"><b>Write</b><span>body · intro · tables</span></div>
          <div class="skill-group"><b>Ship</b><span>check · sim · replicate</span></div>
        </div>
      </div>`,
      "aer-workflow routes the next skill"
    ),
    css
  );
}

function poster04() {
  const dimensions = [
    "Contribution",
    "Identification",
    "Data",
    "Robustness",
    "Magnitudes",
    "Exposition",
    "Integrity",
  ];
  const dimensionTags = dimensions.map((name) => `<div class="dimension">${name}<span>0-5</span></div>`).join("");
  const css = `
.p4 .title {
  position: absolute;
  left: 70px;
  top: 190px;
  width: 920px;
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 138px;
  line-height: .95;
}
.p4 .subtitle {
  position: absolute;
  left: 70px;
  top: 372px;
  width: 780px;
  font-size: 43px;
  line-height: 1.28;
}
.p4 .desk {
  display: none;
}
.p4 .steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
.p4 .step {
  height: 150px;
  padding: 20px 15px;
  text-align: center;
  border-radius: 8px;
  background: rgba(255,255,255,.18);
  border: 1px solid rgba(255,255,255,.26);
}
.p4 .step b {
  display: block;
  font-size: 26px;
  line-height: 1.12;
}
.p4 .step span {
  display: block;
  margin-top: 12px;
  font-size: 18px;
  line-height: 1.24;
  color: rgba(255,255,255,.76);
}
.p4 .stamp {
  position: absolute;
  left: 158px;
  right: 158px;
  top: 196px;
  height: 66px;
  border: 3px solid rgba(255,255,255,.82);
  display: flex;
  align-items: center;
  justify-content: center;
  transform: rotate(-1.6deg);
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 38px;
}
.p4 .score-title {
  display: none;
}
.p4 .dimension-grid {
  display: none;
}
.p4 .dimension {
  height: 56px;
  padding: 0 20px;
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid rgba(9,32,52,.13);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 18px;
  color: #14324a;
}
.p4 .dimension span {
  color: var(--maroon);
}
.p4 .exit {
  display: none;
}
.p4 .exit b {
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 38px;
}
.p4 .exit span {
  font-size: 22px;
  line-height: 1.25;
  font-weight: 700;
  color: rgba(255,255,255,.82);
}
.p4 .stage-mark {
  display: none;
}
.p4 .review-loop {
  position: absolute;
  left: 92px;
  top: 575px;
  width: 850px;
  height: 610px;
}
.p4 .review-box {
  position: absolute;
  width: 310px;
  height: 156px;
  border-radius: 8px;
  background: rgba(255,255,255,.92);
  border: 2px solid rgba(9,32,52,.12);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 38px;
  line-height: 1.08;
  font-weight: 700;
  box-shadow: 0 18px 34px rgba(6,27,45,.08);
}
.p4 .review-box.dark {
  background: var(--maroon);
  color: #ffffff;
}
.p4 .r1 { left: 0; top: 0; }
.p4 .r2 { right: 0; top: 0; }
.p4 .r3 { right: 0; bottom: 0; }
.p4 .r4 { left: 0; bottom: 0; }
.p4 .review-arrow {
  position: absolute;
  font-size: 72px;
  line-height: 1;
  color: var(--blue);
  font-weight: 700;
}
.p4 .a1 { left: 386px; top: 40px; }
.p4 .a2 { right: 118px; top: 258px; transform: rotate(90deg); }
.p4 .a3 { left: 386px; bottom: 40px; transform: rotate(180deg); }
.p4 .a4 { left: 118px; top: 258px; transform: rotate(270deg); }
.p4 .loop-label {
  position: absolute;
  left: 292px;
  top: 226px;
  width: 266px;
  height: 158px;
  border-radius: 8px;
  background: var(--blue);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 36px;
  line-height: 1.12;
  font-weight: 700;
  box-shadow: 0 20px 38px rgba(21,148,246,.24);
}
.p4 .rubric-panel {
  position: absolute;
  left: 70px;
  right: 70px;
  top: 1228px;
  min-height: 202px;
  padding: 24px 26px;
  border-radius: 8px;
  background: rgba(255,255,255,.88);
  border: 2px solid rgba(9,32,52,.10);
  box-shadow: 0 16px 30px rgba(6,27,45,.07);
}
.p4 .rubric-panel b {
  display: block;
  margin-bottom: 16px;
  color: var(--maroon);
  font-size: 32px;
  line-height: 1.05;
}
.p4 .rubric-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.p4 .rubric-chips span {
  min-height: 44px;
  padding: 9px 14px;
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid rgba(9,32,52,.12);
  color: #14324a;
  font-size: 21px;
  line-height: 1.05;
  font-weight: 700;
}
.p4 .rubric-note {
  margin-top: 16px;
  color: var(--muted);
  font-family: "JetBrains Mono Local", monospace;
  font-size: 19px;
  line-height: 1.25;
}
`;
  return page(
    "Poster 04 - Referee Simulation",
    shell(
      "04",
      "Referee Simulation",
      `<div class="wrap p4">
        <h1 class="title">AER-Skills</h1>
        <p class="subtitle">投稿前内审循环</p>
        <div class="review-loop" aria-label="AER-Skills referee simulation loop">
          <div class="review-box r1">一致性<br>审计</div>
          <div class="review-arrow a1">→</div>
          <div class="review-box dark r2">三位<br>审稿人</div>
          <div class="review-arrow a2">→</div>
          <div class="review-box r3">修改<br>清单</div>
          <div class="review-arrow a3">→</div>
          <div class="review-box r4">重新<br>过门</div>
          <div class="review-arrow a4">→</div>
          <div class="loop-label">≥<br>Major R&amp;R</div>
        </div>
        <div class="rubric-panel">
          <b>审稿模拟评分维度</b>
          <div class="rubric-chips">
            <span>贡献</span><span>识别</span><span>数据</span><span>稳健</span>
            <span>效应量</span><span>表图</span><span>文字</span><span>完整性</span>
          </div>
          <div class="rubric-note">desk screen + 3 adversarial referees + routed revise list</div>
        </div>
      </div>`,
      "aer-consistency -> aer-referee-sim"
    ),
    css
  );
}

function poster05() {
  const css = `
.p5 .title {
  position: absolute;
  left: 70px;
  top: 190px;
  width: 920px;
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 138px;
  line-height: .95;
}
.p5 .subtitle {
  position: absolute;
  left: 70px;
  top: 372px;
  width: 780px;
  font-size: 43px;
  line-height: 1.28;
}
.p5 .folder {
  display: none;
}
.p5 .folder-tab {
  position: absolute;
  left: 42px;
  top: -52px;
  width: 305px;
  height: 52px;
  border-radius: 8px 8px 0 0;
  background: var(--blue);
}
.p5 .folder h3 {
  margin: 0;
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 68px;
  line-height: 1;
  letter-spacing: 0;
}
.p5 .folder p {
  width: 690px;
  margin: 26px 0 0;
  font-size: 28px;
  line-height: 1.32;
  font-weight: 700;
  color: rgba(255,255,255,.82);
}
.p5 .ok {
  position: absolute;
  right: 42px;
  bottom: 42px;
  width: 112px;
  height: 112px;
  border-radius: 50%;
  background: var(--gold);
  color: var(--ink);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "Bricolage Local", "Work Sans Local", sans-serif;
  font-size: 45px;
}
.p5 .stacks {
  display: none;
}
.p5 .stack-card {
  height: 112px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 23px;
}
.p5 .stack-card span {
  font-size: 16px;
  color: var(--muted);
}
.p5 .commands {
  display: none;
}
.p5 .command {
  height: 94px;
  border-radius: 8px;
  background: var(--navy);
  color: #d7edf9;
  display: flex;
  align-items: center;
  padding: 0 24px;
  font-size: 21px;
}
.p5 .command strong {
  color: var(--gold);
  font-weight: 400;
}
.p5 .stage-mark {
  display: none;
}
.p5 .deposit-flow {
  position: absolute;
  left: 128px;
  right: 128px;
  top: 565px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}
.p5 .deposit-node {
  width: 100%;
  height: 128px;
  border-radius: 8px;
  background: rgba(255,255,255,.92);
  border: 2px solid rgba(9,32,52,.12);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 38px;
  line-height: 1.04;
  font-weight: 700;
  box-shadow: 0 18px 34px rgba(6,27,45,.08);
}
.p5 .deposit-node span {
  display: block;
  margin-top: 8px;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 20px;
  line-height: 1.18;
  font-weight: 400;
  color: var(--muted);
}
.p5 .deposit-node.primary {
  background: var(--maroon);
  color: #ffffff;
}
.p5 .deposit-node.primary span {
  color: rgba(255,255,255,.78);
}
.p5 .deposit-arrow {
  text-align: center;
  color: var(--blue);
  font-size: 58px;
  line-height: .8;
  font-weight: 700;
}
.p5 .deposit-command {
  position: absolute;
  left: 128px;
  right: 128px;
  top: 1350px;
  min-height: 110px;
  padding: 20px 28px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  background: var(--navy);
  color: #d7edf9;
  font-family: "JetBrains Mono Local", monospace;
  font-size: 24px;
  line-height: 1.45;
}
.p5 .deposit-command strong {
  color: var(--gold);
  font-weight: 400;
}
`;
  return page(
    "Poster 05 - Replication Package",
    shell(
      "05",
      "Replication Package",
      `<div class="wrap p5">
        <h1 class="title">AER-Skills</h1>
        <p class="subtitle">复现包 = 论文的一部分</p>
        <div class="deposit-flow" aria-label="AER-Skills replication submission flow">
          <div class="deposit-node">Stata / R / Python<span>reghdfe · fixest · pyfixest</span></div>
          <div class="deposit-arrow">↓</div>
          <div class="deposit-node">README-first<span>data · codebook · exhibit register</span></div>
          <div class="deposit-arrow">↓</div>
          <div class="deposit-node primary">make preflight<span>validate · skillopt · citations</span></div>
          <div class="deposit-arrow">↓</div>
          <div class="deposit-node">AEA / openICPSR<span>DCAP-ready replication deposit</span></div>
        </div>
        <div class="deposit-command"><div><strong>$</strong>&nbsp; scaffold_project.py skeleton</div><div><strong>$</strong>&nbsp; make preflight</div></div>
      </div>`,
      "python3 scripts/scaffold_project.py skeleton /path/to/paper"
    ),
    css
  );
}

const posters = [
  ["poster-01-aer-skills.html", "poster-01-aer-skills.png", poster01],
  ["poster-02-identification-first.html", "poster-02-identification-first.png", poster02],
  ["poster-03-fourteen-skills.html", "poster-03-fourteen-skills.png", poster03],
  ["poster-04-referee-sim.html", "poster-04-referee-sim.png", poster04],
  ["poster-05-replication-package.html", "poster-05-replication-package.png", poster05],
];

function writeIndex() {
  const cards = posters
    .map(([html, png], i) => `<a class="card" href="${html}"><img src="${png}" alt="poster ${i + 1}"><span>${String(i + 1).padStart(2, "0")} ${html}</span></a>`)
    .join("");
  fs.writeFileSync(
    path.join(OUT_DIR, "index.html"),
    `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>AER-Skills 小红书海报</title><style>
body{margin:0;background:#061b2d;color:#f4fbff;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;padding:40px}
h1{font-size:34px;margin:0 0 28px}.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:20px}
.card{color:inherit;text-decoration:none}.card img{width:100%;display:block;border:1px solid rgba(255,255,255,.18)}
.card span{display:block;margin-top:10px;font-size:13px;line-height:1.4;word-break:break-all;color:rgba(244,251,255,.72)}
@media (max-width: 1100px){.grid{grid-template-columns:repeat(2,1fr)}}
</style></head><body><h1>AER-Skills 小红书竖屏海报</h1><div class="grid">${cards}</div></body></html>`
  );
}

function renderPng(htmlFile, pngFile) {
  const htmlPath = path.join(OUT_DIR, htmlFile);
  const pngPath = path.join(OUT_DIR, pngFile);
  const result = spawnSync(
    CHROME,
    [
      "--headless=new",
      "--disable-gpu",
      "--hide-scrollbars",
      "--allow-file-access-from-files",
      "--force-device-scale-factor=1",
      `--window-size=${W},${H}`,
      "--virtual-time-budget=1600",
      `--screenshot=${pngPath}`,
      pathToFileURL(htmlPath).href,
    ],
    { stdio: "pipe" }
  );
  if (result.status !== 0) {
    throw new Error(`Chrome failed for ${htmlFile}\n${result.stderr.toString()}\n${result.stdout.toString()}`);
  }
}

function main() {
  writeDesignPhilosophy();
  for (const [html, , make] of posters) {
    fs.writeFileSync(path.join(OUT_DIR, html), make());
  }
  writeIndex();
  for (const [html, png] of posters) {
    renderPng(html, png);
    console.log(`rendered ${png}`);
  }
}

main();
