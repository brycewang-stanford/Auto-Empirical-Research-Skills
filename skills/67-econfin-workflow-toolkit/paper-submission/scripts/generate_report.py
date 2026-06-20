"""
Paper Submission Target Report PDF Generator

Usage:
    python generate_report.py --json report_data.json --output target.pdf

The JSON file should contain all report sections. See ReportData schema below.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

from fpdf import FPDF


# ── Constants ──────────────────────────────────────────────────────────────

FONT_PATH = r"C:\Windows\Fonts\simsun.ttc"
FONT_BOLD_PATH = r"C:\Windows\Fonts\simhei.ttf"
PAGE_W = 210  # A4 width mm
MARGIN = 15
CONTENT_W = PAGE_W - 2 * MARGIN


# ── PDF Builder ────────────────────────────────────────────────────────────

class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("SimSun", "", FONT_PATH)
        self.add_font("SimHei", "", FONT_BOLD_PATH)
        self.set_auto_page_break(auto=True, margin=20)

    # ── helpers ────────────────────────────────────────────────────────

    def _heading(self, text: str, size: int = 14):
        """Section heading in bold font."""
        self.set_font("SimHei", "", size)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def _subheading(self, text: str, size: int = 11):
        self.set_font("SimHei", "", size)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def _body(self, text: str, size: int = 10):
        self.set_font("SimSun", "", size)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def _separator(self):
        self.set_draw_color(100, 100, 100)
        y = self.get_y()
        self.line(MARGIN, y, PAGE_W - MARGIN, y)
        self.ln(4)

    def _kv(self, key: str, value: str):
        """Key-value line: bold key, normal value."""
        self.set_font("SimHei", "", 10)
        kw = self.get_string_width(key) + 2
        self.cell(kw, 6, key)
        self.set_font("SimSun", "", 10)
        self.multi_cell(0, 6, value)
        self.ln(1)

    # ── table helper ───────────────────────────────────────────────────

    def _journal_table(self, journals: list[dict]):
        """
        Draw a journal recommendation table.
        Each journal dict: {rank, name, abs, ssci, jif, rationale}
        """
        col_widths = [8, 62, 12, 12, 14, CONTENT_W - 108]
        headers = ["#", "Journal", "ABS", "SSCI", "JIF", "Rationale"]

        # header row
        self.set_font("SimHei", "", 9)
        self.set_fill_color(230, 230, 230)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True)
        self.ln()

        # data rows
        self.set_font("SimSun", "", 8)
        for j in journals:
            row = [
                str(j.get("rank", "")),
                j.get("name", ""),
                str(j.get("abs", "")),
                j.get("ssci", ""),
                str(j.get("jif", "")),
                j.get("rationale", ""),
            ]
            # calculate row height based on rationale length
            max_lines = max(1, len(row[5]) // 18 + 1)
            rh = 6 * max_lines

            x_start = self.get_x()
            y_start = self.get_y()

            # check page break
            if y_start + rh > self.h - 20:
                self.add_page()
                # reprint header
                self.set_font("SimHei", "", 9)
                self.set_fill_color(230, 230, 230)
                for i, h in enumerate(headers):
                    self.cell(col_widths[i], 7, h, border=1, fill=True)
                self.ln()
                self.set_font("SimSun", "", 8)
                x_start = self.get_x()
                y_start = self.get_y()

            for i in range(len(row) - 1):
                self.set_xy(x_start + sum(col_widths[:i]), y_start)
                self.cell(col_widths[i], rh, row[i], border=1)

            # last column: multi_cell for wrapping
            self.set_xy(x_start + sum(col_widths[:5]), y_start)
            self.multi_cell(col_widths[5], 6, row[5], border=1)

            # ensure we move to next row
            self.set_y(y_start + rh)

        self.ln(3)


# ── Report Builder ─────────────────────────────────────────────────────────

def build_report(data: dict, output_path: str):
    pdf = ReportPDF()
    pdf.add_page()

    # ── Title page ─────────────────────────────────────────────────────
    pdf.ln(30)
    pdf.set_font("SimHei", "", 22)
    pdf.cell(0, 14, "Paper Submission Target Report", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("SimHei", "", 18)
    pdf.cell(0, 12, "论文投稿目标评估报告", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    pdf.set_font("SimSun", "", 11)
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    pdf.cell(0, 8, f"Date: {date_str}", align="C",
             new_x="LMARGIN", new_y="NEXT")
    title = data.get("paper_title", "")
    if title:
        pdf.ln(3)
        pdf.set_font("SimSun", "", 11)
        pdf.multi_cell(0, 8, f"Paper: {title}", align="C")

    # ── Section 1: Paper Summary ───────────────────────────────────────
    pdf.add_page()
    pdf._heading("一、论文概要  Paper Summary")
    pdf._separator()
    summary = data.get("summary", {})
    if isinstance(summary, dict):
        for k, v in summary.items():
            pdf._kv(f"{k}：", v)
    else:
        pdf._body(str(summary))

    # ── Section 2: Novelty Assessment ──────────────────────────────────
    pdf.ln(5)
    pdf._heading("二、文献创新性评估  Novelty Assessment")
    pdf._separator()

    novelty = data.get("novelty", {})
    score = novelty.get("score", 0)
    rating = novelty.get("rating", "")
    pdf._kv("综合得分 Overall Score：", f"{score}/100 — {rating}")
    pdf.ln(2)

    # dimensions
    dims = novelty.get("dimensions", [])
    for d in dims:
        pdf._subheading(f"维度: {d['name']} — {d['sub_score']}/100")
        if d.get("related_papers"):
            pdf._kv("  相关文献：", d["related_papers"])
        if d.get("innovation"):
            pdf._kv("  本文创新：", d["innovation"])
        pdf.ln(1)

    # key innovations
    innovations = novelty.get("innovations", [])
    if innovations:
        pdf._subheading("主要创新点：")
        for i, inn in enumerate(innovations, 1):
            pdf._body(f"  {i}. {inn}")

    # risks
    risks = novelty.get("risks", [])
    if risks:
        pdf._subheading("潜在审稿风险：")
        for r in risks:
            pdf._body(f"  - {r}")

    # ── Section 3: Field & Star Rating ─────────────────────────────────
    pdf.add_page()
    pdf._heading("三、目标领域与星级  Target Field & Rating")
    pdf._separator()

    target = data.get("target", {})
    fields = target.get("fields", [])
    star = target.get("star_rating", "")
    if fields:
        pdf._kv("最佳领域 Best Fields：", f"{fields[0]}, {fields[1]}" if len(fields) > 1 else fields[0])
    pdf._kv("建议星级 Recommended Rating：", f"ABS {star}")
    pdf.ln(2)

    assessments = target.get("assessments", {})
    for k, v in assessments.items():
        pdf._kv(f"  {k}：", v)

    # ── Section 4: Journal Recommendations ─────────────────────────────
    pdf.add_page()
    pdf._heading("四、推荐期刊  Journal Recommendations（共20本）")
    pdf._separator()

    journals_by_field = data.get("journals", {})
    for field_name, jlist in journals_by_field.items():
        pdf._subheading(f"{field_name}（{len(jlist)}本）")
        pdf._journal_table(jlist)
        pdf.ln(3)

    # ── Section 5: Strategic Advice ────────────────────────────────────
    pdf.add_page()
    pdf._heading("五、投稿建议  Submission Strategy")
    pdf._separator()

    advice = data.get("advice", "")
    pdf._body(advice)

    # ── Save ───────────────────────────────────────────────────────────
    pdf.output(output_path)
    print(f"Report saved to: {output_path}")


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate paper submission target report PDF")
    parser.add_argument("--json", required=True, help="Path to JSON data file")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    build_report(data, args.output)


if __name__ == "__main__":
    main()
