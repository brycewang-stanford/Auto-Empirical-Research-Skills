#!/usr/bin/env python3
"""
后处理脚本：修复Word文档中的标题字体、行距和段后间距
确保所有标题都使用仿宋字体，所有段落使用1.5倍行距，标题段后1行
"""

import sys
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.enum.text import WD_LINE_SPACING

def fix_heading_fonts(docx_file):
    """
    修复Word文档中所有标题的字体、行距和段后间距，确保使用仿宋、1.5倍行距和段后1行

    Args:
        docx_file (str): Word文档路径

    Returns:
        bool: 成功返回True，失败返回False
    """
    if not os.path.exists(docx_file):
        print(f"错误：文件不存在：{docx_file}")
        return False

    try:
        # 打开文档
        doc = Document(docx_file)

        # 遍历所有段落
        for para in doc.paragraphs:
            # 为所有段落设置1.5倍行距
            para.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

            # 检查是否是标题段落
            if para.style.name.startswith('Heading') or para.style.name in ['Title', 'Subtitle']:
                # 设置段后间距为1行（12磅）
                para.paragraph_format.space_after = Pt(12)

                # 为该段落的每个run设置字体
                for run in para.runs:
                    run.font.name = '仿宋'
                    run.font.italic = False  # 确保不是斜体
                    run.font.color.rgb = RGBColor(0, 0, 0)  # 黑色

                    # 设置所有字体属性
                    r = run._element
                    r.rPr.rFonts.set(qn('w:eastAsia'), '仿宋')
                    r.rPr.rFonts.set(qn('w:ascii'), '仿宋')
                    r.rPr.rFonts.set(qn('w:hAnsi'), '仿宋')
                    r.rPr.rFonts.set(qn('w:cs'), '仿宋')

        # 保存文档
        doc.save(docx_file)
        print(f"✓ 已修复标题字体、行距和段后间距：{docx_file}")
        print(f"  所有标题现在都使用仿宋字体")
        print(f"  所有段落现在都使用1.5倍行距")
        print(f"  所有标题段后间距为1行")
        return True

    except Exception as e:
        print(f"错误：{str(e)}")
        return False

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='修复Word文档中的标题字体、行距和段后间距')
    parser.add_argument('docx_file', help='要修复的Word文档')

    args = parser.parse_args()

    success = fix_heading_fonts(args.docx_file)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
