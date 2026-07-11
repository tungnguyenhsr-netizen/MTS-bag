#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate MTS-Portfolio.pdf — bilingual (VI/EN) OEM bag manufacturer portfolio.
Brand colors: ink #1A1A1A, gold #C8A96E, cream #F5F0EB. Uses Arial (Vietnamese-capable)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, PageBreak,
                                HRFlowable, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")

# --- Fonts (Vietnamese-capable) ---
pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", "C:/Windows/Fonts/ariali.ttf"))

# --- Brand palette ---
INK = colors.HexColor("#1A1A1A")
GOLD = colors.HexColor("#C8A96E")
CREAM = colors.HexColor("#F5F0EB")
MUTED = colors.HexColor("#6B6258")
BORDER = colors.HexColor("#E2D9CC")

# --- Styles ---
styles = getSampleStyleSheet()
def S(name, **kw):
    base = kw.pop("parent", styles["Normal"])
    kw.setdefault("fontName", "Arial")
    return ParagraphStyle(name, parent=base, **kw)

st_title = S("t", fontName="Arial-Bold", fontSize=26, textColor=INK, leading=30)
st_sub = S("s", fontSize=12, textColor=MUTED, leading=16)
st_mono = S("m", fontName="Arial-Bold", fontSize=9, textColor=GOLD, leading=12,
            spaceAfter=6)
st_h2 = S("h2", fontName="Arial-Bold", fontSize=16, textColor=INK, leading=20,
          spaceBefore=10, spaceAfter=4)
st_body = S("b", fontSize=10.5, textColor=INK, leading=15)
st_body_vi = S("bv", fontSize=10.5, textColor=INK, leading=15)
st_body_en = S("be", fontSize=9.5, textColor=MUTED, leading=13)
st_cap = S("c", fontSize=8.5, textColor=MUTED, leading=11)
st_cap_c = S("cc", fontSize=8.5, textColor=colors.white, leading=11,
             alignment=TA_CENTER)

PAGE_W, PAGE_H = A4
LM = RM = 18 * mm
content_w = PAGE_W - LM - RM

def header_footer(canvas, doc):
    canvas.saveState()
    # Top rule
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(2)
    canvas.line(LM, PAGE_H - 14*mm, PAGE_W - RM, PAGE_H - 14*mm)
    canvas.setFont("Arial-Bold", 9)
    canvas.setFillColor(INK)
    canvas.drawString(LM, PAGE_H - 12*mm, "MINH TÙNG STUDIO")
    canvas.setFillColor(GOLD)
    canvas.drawRightString(PAGE_W - RM, PAGE_H - 12*mm, "OEM BAG & BACKPACK MANUFACTURER")
    # Footer
    canvas.setStrokeColor(BORDER); canvas.setLineWidth(0.5)
    canvas.line(LM, 14*mm, PAGE_W - RM, 14*mm)
    canvas.setFont("Arial", 8); canvas.setFillColor(MUTED)
    canvas.drawString(LM, 10*mm, "Minh Tùng Studio — TP.HCM, Vietnam")
    canvas.drawRightString(PAGE_W - RM, 10*mm, "Trang %d" % doc.page)
    canvas.restoreState()

doc = BaseDocTemplate(
    os.path.join(BASE, "MTS-Portfolio.pdf"),
    pagesize=A4, leftMargin=LM, rightMargin=RM,
    topMargin=20*mm, bottomMargin=18*mm,
    title="Minh Tùng Studio — Portfolio", author="Minh Tùng Studio")
frame = Frame(LM, 16*mm, content_w, PAGE_H - 36*mm, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])

def img(name, w):
    p = os.path.join(IMG, name)
    if not os.path.exists(p):
        return None
    from PIL import Image as PImage
    iw, ih = PImage.open(p).size
    return Image(p, width=w, height=w * ih / iw)

def hr():
    return HRFlowable(width="100%", thickness=0.6, color=BORDER,
                      spaceBefore=8, spaceAfter=8)

flow = []

# ===== COVER =====
flow.append(Spacer(1, 18*mm))
flow.append(Paragraph("MINH TÙNG STUDIO", st_title))
flow.append(Spacer(1, 3*mm))
flow.append(Paragraph("Gia công túi / balo tại Việt Nam — từ 300 sản phẩm", st_sub))
flow.append(Paragraph("Custom bag &amp; backpack manufacturing in Vietnam — from 300 pieces", st_sub))
flow.append(Spacer(1, 8*mm))
flow.append(hr())
flow.append(Paragraph("01 — GIỚI THIỆU / ABOUT", st_mono))
flow.append(Paragraph(
    "Minh Tùng Studio (MTS) là xưởng sản xuất túi / balo tại TP.HCM, chuyên gia công cho "
    "các brand thời trang, streetwear và phụ kiện. Chúng tôi không phải trung gian — tự cắt, "
    "may, ép logo, QC và đóng gói tại xưởng.", st_body_vi))
flow.append(Spacer(1, 2*mm))
flow.append(Paragraph(
    "Minh Tùng Studio (MTS) is a Ho Chi Minh City-based bag and backpack manufacturer. We are "
    "not a trading company — we cut, sew, print, emboss, QC, and pack under one roof.", st_body_en))
flow.append(Spacer(1, 6*mm))
# stats strip
stats = [["6+", "50K+", "300"],
         ["Thương hiệu / Brands", "Sản phẩm/năm / Units per year", "MOQ"]]
t = Table(stats, colWidths=[content_w/3.0]*3)
t.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,0), "Arial-Bold"),
    ("FONTSIZE", (0,0), (-1,0), 20),
    ("TEXTCOLOR", (0,0), (-1,0), GOLD),
    ("FONTNAME", (0,1), (-1,1), "Arial"),
    ("FONTSIZE", (0,1), (-1,1), 8.5),
    ("TEXTCOLOR", (0,1), (-1,1), MUTED),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
flow.append(t)
flow.append(PageBreak())

# ===== PRODUCTS =====
flow.append(Paragraph("02 — SẢN PHẨM / PRODUCTS", st_mono))
flow.append(Paragraph("Danh mục sản phẩm cho đối tác B2B.", st_sub))
flow.append(Paragraph("Product categories for B2B partners.", st_sub))
flow.append(Spacer(1, 4*mm))

products = [
    ("Balo / Backpacks", "images/product-backpack-1.png",
     "Balo ngày, laptop, thời trang. Canvas, PU da, hỗn hợp. Ngăn đệm, đa túi.",
     "Daypacks, laptop & fashion backpacks. Canvas, PU leather, mixed. Padded, multi-pocket."),
    ("Túi Đeo Chéo / Sling", "images/product-sling-bag.png",
     "Mini sling, túi vai, crossbody. PU da, canvas, nylon. Dây điều chỉnh, ngăn khóa kéo.",
     "Mini slings, shoulder & crossbody messengers. PU leather, canvas, nylon."),
    ("Túi Du Lịch / Duffel", "images/product-duffle-bag.png",
     "Gym duffel, travel weekender, mini duffle. Canvas, PU da, vải phủ. Dây tháo rời, ngăn giày.",
     "Gym duffels, weekenders, mini duffles. Canvas, PU leather, coated fabrics."),
    ("Túi Tote", "images/product-tote-bag.png",
     "Tote cấu trúc, tote gấp gọn, shopping tote. Canvas, PU da. Khóa từ, quai gia cố.",
     "Structured & foldable totes, shopping totes. Canvas, PU leather."),
    ("Phụ Kiện Da / Leather", "images/product-mini-backpack.png",
     "Card holder, ví, túi nhỏ, móc khóa. Da thật hoặc PU. Quà tặng kèm.",
     "Card holders, wallets, pouches, keychains. Real or PU leather."),
]
col_w = (content_w - 6*mm) / 2.0
for i in range(0, len(products), 2):
    row = []
    for name, fn, vi, en in products[i:i+2]:
        cell = []
        im = img(fn, col_w - 4*mm)
        if im:
            cell.append(im)
        cell.append(Paragraph(name, S("pn", fontName="Arial-Bold", fontSize=11,
                                       textColor=INK, leading=14, spaceBefore=2)))
        cell.append(Paragraph(vi, st_cap))
        cell.append(Paragraph(en, st_body_en))
        row.append(cell)
    inner = Table([row], colWidths=[col_w]*len(row))
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CREAM),
        ("BOX", (0,0), (-1,-1), 0.6, BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.6, BORDER),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    flow.append(inner)
    flow.append(Spacer(1, 4*mm))

flow.append(PageBreak())

# ===== CAPABILITIES & PROCESS =====
flow.append(Paragraph("03 — NĂNG LỰC & QUY TRÌNH / CAPABILITIES & PROCESS", st_mono))
caps = [
    ("Sản phẩm / Products", "Backpack, Sling, Duffel, Tote, Phụ kiện da."),
    ("Nguyên liệu / Materials", "Da thật, da PU, Canvas, Nylon, Polyester, phụ kiện kim loại."),
    ("Phát triển / Development", "Techpack → Mẫu thử → Sản xuất. MOQ 300 / 1000."),
    ("Chất lượng / Quality", "QC nội bộ AQL 2.5. Báo cáo từng lô. Ảnh trước khi giao."),
]
data = [[Paragraph(a, S("k", fontName="Arial-Bold", fontSize=10, textColor=GOLD)),
         Paragraph(b, st_body)] for a, b in caps]
ct = Table(data, colWidths=[content_w*0.32, content_w*0.68])
ct.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), CREAM),
    ("BOX", (0,0), (-1,-1), 0.6, BORDER),
    ("INNERGRID", (0,0), (-1,-1), 0.6, BORDER),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
flow.append(ct)
flow.append(Spacer(1, 6*mm))

flow.append(Paragraph("Quy trình 6 bước — minh bạch, đúng tiến độ.", st_sub))
flow.append(Paragraph("6-step process — transparent, on schedule.", st_sub))
flow.append(Spacer(1, 3*mm))
steps = [
    ("1. Tiếp nhận / Inquiry", "1–2 ngày / days"),
    ("2. Báo giá / Quote", "2–3 ngày / days"),
    ("3. Mẫu thử / Sample", "7–10 ngày / days"),
    ("4. Sản xuất / Production", "10–25 ngày / days"),
    ("5. Kiểm định / QC", "1–2 ngày / days"),
    ("6. Giao hàng / Delivery", "—"),
]
sc = [[Paragraph(a, S("sk", fontName="Arial-Bold", fontSize=9.5, textColor=INK)),
       Paragraph(b, st_cap)] for a, b in steps]
sct = Table(sc, colWidths=[content_w*0.6, content_w*0.4])
sct.setStyle(TableStyle([
    ("LINEBELOW", (0,0), (-1,-2), 0.5, BORDER),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0), (-1,-1), 2), ("RIGHTPADDING", (0,0), (-1,-1), 2),
    ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
flow.append(sct)

flow.append(PageBreak())

# ===== FACILITY =====
flow.append(Paragraph("04 — XƯỞNG / FACILITY", st_mono))
flow.append(Paragraph("Quy trình khép kín — từ cắt, may, logo đến kiểm định.", st_sub))
flow.append(Paragraph("End-to-end process — cutting, sewing, branding, QC.", st_sub))
flow.append(Spacer(1, 4*mm))
fac = ["factory-assembly-line.png", "factory-sewing-station.png",
       "factory-craftsmanship.png", "factory-cutting-equipment.png"]
fw = (content_w - 6*mm) / 2.0
for i in range(0, len(fac), 2):
    row = []
    for fn in fac[i:i+2]:
        im = img(fn, fw - 4*mm)
        row.append([im] if im else [])
    ft = Table([row], colWidths=[fw]*len(row))
    ft.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.6, BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.6, BORDER),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    flow.append(ft)
    flow.append(Spacer(1, 4*mm))

flow.append(Spacer(1, 4*mm))
flow.append(hr())
flow.append(Paragraph("05 — LIÊN HỆ / CONTACT", st_mono))
contact_tbl = Table([
    [Paragraph("Email", st_cap), Paragraph("tungnguyenhsr@gmail.com", st_body)],
    [Paragraph("Zalo / Phone (Tùng)", st_cap), Paragraph("+84 773 108 320", st_body)],
    [Paragraph("WhatsApp (Lâm)", st_cap), Paragraph("+84 979 768 997", st_body)],
    [Paragraph("Địa chỉ / Address", st_cap), Paragraph("TP.HCM, Vietnam", st_body)],
], colWidths=[content_w*0.35, content_w*0.65])
contact_tbl.setStyle(TableStyle([
    ("LINEBELOW", (0,0), (-1,-2), 0.5, BORDER),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING", (0,0), (-1,-1), 2),
    ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
flow.append(contact_tbl)
flow.append(Spacer(1, 4*mm))
flow.append(Paragraph(
    "Gửi thiết kế — chúng tôi báo giá trong 48h, không cam kết.  /  Send us your design — "
    "we quote within 48 hours, no commitment.", st_body_en))

doc.build(flow)
print("OK -> MTS-Portfolio.pdf")
