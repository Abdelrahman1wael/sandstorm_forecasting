# -*- coding: utf-8 -*-
"""
Master Document Generation Script:
Extended-Range Sand and Dust Storm (SDS) Forecasting in Saudi Arabia with Special Emphasis on Riyadh City.
Grounds all data, equations, models, and validations in Riyadh, Kingdom of Saudi Arabia.
Output File: Documentation/final for Saudi Arabia and especially in Riyadh city.docx
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top="CBD5E0", bottom="CBD5E0", left="none", right="none", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for b_name, b_val in borders.items():
        node = OxmlElement(f'w:{b_name}')
        if b_val == "none":
            node.set(qn('w:val'), 'none')
        else:
            node.set(qn('w:val'), 'single')
            node.set(qn('w:sz'), sz)
            node.set(qn('w:space'), '0')
            node.set(qn('w:color'), b_val)
        tcBorders.append(node)
    tcPr.append(tcBorders)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    return p

def add_body_paragraph(doc, text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
        
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    return p

def add_bullet_point(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
        
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    return p

def add_callout_box(doc, text, title=None, fill_hex="F0F4F8", border_hex="1A365D"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    left_node = OxmlElement('w:left')
    left_node.set(qn('w:val'), 'single')
    left_node.set(qn('w:sz'), '24')
    left_node.set(qn('w:space'), '0')
    left_node.set(qn('w:color'), border_hex)
    tcBorders.append(left_node)
    
    for side in ['top', 'bottom', 'right']:
        node = OxmlElement(f'w:{side}')
        node.set(qn('w:val'), 'none')
        tcBorders.append(node)
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        run_title = p.add_run(f"{title}\n")
        run_title.font.name = 'Calibri'
        run_title.font.size = Pt(10.5)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
        
    run_text = p.add_run(text)
    run_text.font.name = 'Calibri'
    run_text.font.size = Pt(10)
    run_text.font.italic = True
    run_text.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def add_figure_with_caption(doc, img_path, figure_num, title, explanation, width_inches=6.0):
    if not os.path.exists(img_path):
        print(f"Warning: image path does not exist: {img_path}")
        return
        
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.line_spacing = 1.15
    
    run_tag = p_cap.add_run(f"Figure {figure_num}: {title}. ")
    run_tag.font.name = 'Calibri'
    run_tag.font.size = Pt(9.5)
    run_tag.font.bold = True
    run_tag.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    
    run_exp = p_cap.add_run(explanation)
    run_exp.font.name = 'Calibri'
    run_exp.font.size = Pt(9)
    run_exp.font.italic = True
    run_exp.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

def add_equation_block(doc, eq_text, eq_number):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(5.6)
    table.columns[1].width = Inches(0.9)
    
    cell_eq = table.cell(0, 0)
    cell_num = table.cell(0, 1)
    
    for c in [cell_eq, cell_num]:
        set_cell_borders(c, top="none", bottom="none", left="none", right="none")
        set_cell_background(c, "F8FAFC")
        set_cell_margins(c, top=50, bottom=50, left=80, right=80)
        
    p_eq = cell_eq.paragraphs[0]
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq.paragraph_format.space_before = Pt(2)
    p_eq.paragraph_format.space_after = Pt(2)
    run_eq = p_eq.add_run(eq_text)
    run_eq.font.name = 'Cambria Math'
    run_eq.font.size = Pt(10.5)
    run_eq.font.bold = False
    run_eq.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)
    
    p_num = cell_num.paragraphs[0]
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.space_before = Pt(2)
    p_num.paragraph_format.space_after = Pt(2)
    run_num = p_num.add_run(f"({eq_number})")
    run_num.font.name = 'Calibri'
    run_num.font.size = Pt(10)
    run_num.font.bold = True
    run_num.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

print("Framework functions ready.")
