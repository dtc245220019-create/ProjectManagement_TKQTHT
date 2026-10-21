import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

OUTPUT_DOCX = r"E:\ProjectManagement\Bao_cao_De14_Dinh_Gia_Bao_DTC245220019.docx"
LOGO_PATH = r"E:\ProjectManagement\docs\assets\logo_ictu.png"
EVIDENCE_DIR = r"E:\ProjectManagement\docs\evidence"

def create_report():
    doc = docx.Document()

    # 1. Page Setup (A4, Margins: Top 2cm, Bottom 2cm, Left 3cm, Right 1.5cm)
    for section in doc.sections:
        section.page_width = Inches(8.27)   # 21.0 cm
        section.page_height = Inches(11.69) # 29.7 cm
        section.top_margin = Inches(0.79)    # 2.0 cm
        section.bottom_margin = Inches(0.79) # 2.0 cm
        section.left_margin = Inches(1.18)   # 3.0 cm
        section.right_margin = Inches(0.59)  # 1.5 cm

    # Base Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(15, 23, 42) # #0F172A
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(4)
    style_normal.paragraph_format.space_before = Pt(0)

    # XML Helper Functions
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def set_cover_borders(table, color="1E3A8A", sz="16", val="double"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="none"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_p(text="", bold=False, italic=False, size=12, color=RGBColor(15, 23, 42), align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, space_before=0, line_spacing=1.2):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = color
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 58, 138) # #1E3A8A Deep Navy Blue
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_code(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        
        # Border
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:left w:val="single" w:sz="16" w:space="0" w:color="2563EB"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(code_text)
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def add_image_figure(img_rel_path, caption_text, width_inches=6.2):
        abs_path = os.path.join(EVIDENCE_DIR, img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path
        if os.path.exists(abs_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run = p_img.add_run()
            run.add_picture(abs_path, width=Inches(width_inches))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.font.bold = True
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(30, 58, 138)
        else:
            print(f"Warning: Image file not found at {abs_path}")

    def add_styled_table(headers, data, col_widths=None):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="94A3B8", sz="4", val="single")

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, title in enumerate(headers):
            hdr_cells[i].text = title
            set_cell_background(hdr_cells[i], "1E3A8A")
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].text = str(cell_value)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10.5)
                    r.font.color.rgb = RGBColor(15, 23, 42)

        # Apply Column Widths if specified
        if col_widths:
            for row in table.rows:
                for c_idx, w in enumerate(col_widths):
                    row.cells[c_idx].width = Inches(w)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return table

    def add_callout(title, text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "EFF6FF")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>'
            f'<w:bottom w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_title = p.add_run(f"📌 {title}: ")
        r_title.font.name = 'Times New Roman'
        r_title.font.size = Pt(10.5)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(30, 58, 138)
        
        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    print("Helper functions initialized. Generating content...")

    # ==========================================
    # 1. COVER PAGE (TRANG BÌA)
    # ==========================================
    cover_table = doc.add_table(rows=11, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cover_borders(cover_table, color="1E3A8A", sz="16", val="double")

    # Set row heights matching sample
    cover_table.rows[0].height = Pt(4)
    cover_table.rows[1].height = Pt(45)
    cover_table.rows[2].height = Pt(170)
    cover_table.rows[3].height = Pt(55)
    cover_table.rows[4].height = Pt(10)
    cover_table.rows[5].height = Pt(25)
    cover_table.rows[6].height = Pt(55)
    cover_table.rows[7].height = Pt(15)
    cover_table.rows[8].height = Pt(22)
    cover_table.rows[9].height = Pt(22)
    cover_table.rows[10].height = Pt(185)

    # Merge top rows across columns
    cover_table.rows[0].cells[0].merge(cover_table.rows[0].cells[1])
    cover_table.rows[1].cells[0].merge(cover_table.rows[1].cells[1])
    cover_table.rows[2].cells[0].merge(cover_table.rows[2].cells[1])
    cover_table.rows[3].cells[0].merge(cover_table.rows[3].cells[1])
    cover_table.rows[4].cells[0].merge(cover_table.rows[4].cells[1])
    cover_table.rows[5].cells[0].merge(cover_table.rows[5].cells[1])
    cover_table.rows[6].cells[0].merge(cover_table.rows[6].cells[1])
    cover_table.rows[7].cells[0].merge(cover_table.rows[7].cells[1])

    # Row 1: University Header
    p_univ = cover_table.rows[1].cells[0].paragraphs[0]
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_univ.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(13)
    r1.font.bold = False
    r2 = p_univ.add_run("KHOA CÔNG NGHỆ THÔNG TIN")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(13.5)
    r2.font.bold = True

    # Row 2: Logo ICTU
    p_logo = cover_table.rows[2].cells[0].paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(LOGO_PATH):
        p_logo.add_run().add_picture(LOGO_PATH, width=Inches(1.85))

    # Row 3: Report Title
    p_rep = cover_table.rows[3].cells[0].paragraphs[0]
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rep1 = p_rep.add_run("BÁO CÁO\n")
    r_rep1.font.name = 'Times New Roman'
    r_rep1.font.size = Pt(20)
    r_rep1.font.bold = True
    r_rep1.font.color.rgb = RGBColor(30, 58, 138)
    r_rep2 = p_rep.add_run("HỌC PHẦN TRIỂN KHAI & QUẢN TRỊ HỆ THỐNG PHẦN MỀM")
    r_rep2.font.name = 'Times New Roman'
    r_rep2.font.size = Pt(13.5)
    r_rep2.font.bold = True

    # Row 5: Topic Label
    p_top = cover_table.rows[5].cells[0].paragraphs[0]
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_top = p_top.add_run("Đề tài:")
    r_top.font.name = 'Times New Roman'
    r_top.font.size = Pt(14)
    r_top.font.bold = True

    # Row 6: Topic Name
    p_tn = cover_table.rows[6].cells[0].paragraphs[0]
    p_tn.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tn = p_tn.add_run("Hệ thống Quản lý Dự án (Project Management)")
    r_tn.font.name = 'Times New Roman'
    r_tn.font.size = Pt(16)
    r_tn.font.bold = True
    r_tn.font.color.rgb = RGBColor(185, 28, 28) # Accent deep red

    # Row 8: Student
    p_s1 = cover_table.rows[8].cells[0].paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_s1 = p_s1.add_run("    Sinh viên thực hiện :")
    r_s1.font.name = 'Times New Roman'
    r_s1.font.size = Pt(13)
    r_s1.font.bold = True
    p_s2 = cover_table.rows[8].cells[1].paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_s2 = p_s2.add_run("Đinh Gia Bảo")
    r_s2.font.name = 'Times New Roman'
    r_s2.font.size = Pt(13)
    r_s2.font.bold = True

    # Row 9: Student ID
    p_id1 = cover_table.rows[9].cells[0].paragraphs[0]
    p_id1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_id1 = p_id1.add_run("    Mã sinh viên :")
    r_id1.font.name = 'Times New Roman'
    r_id1.font.size = Pt(13)
    r_id1.font.bold = True
    p_id2 = cover_table.rows[9].cells[1].paragraphs[0]
    p_id2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_id2 = p_id2.add_run("DTC245220019")
    r_id2.font.name = 'Times New Roman'
    r_id2.font.size = Pt(13)
    r_id2.font.bold = True

    # Row 10: Class & Instructor
    cover_table.rows[10].cells[0].merge(cover_table.rows[10].cells[1])
    p_inst = cover_table.rows[10].cells[0].paragraphs[0]
    p_inst.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_c1 = p_inst.add_run("    Lớp : ")
    r_c1.font.name = 'Times New Roman'
    r_c1.font.size = Pt(13)
    r_c1.font.bold = True
    r_c2 = p_inst.add_run("ATTT K23A\n\n")
    r_c2.font.name = 'Times New Roman'
    r_c2.font.size = Pt(13)
    r_c2.font.bold = True
    r_i1 = p_inst.add_run("    Giảng viên hướng dẫn : ")
    r_i1.font.name = 'Times New Roman'
    r_i1.font.size = Pt(13)
    r_i1.font.bold = True
    r_i2 = p_inst.add_run("Nguyễn Anh Chuyên")
    r_i2.font.name = 'Times New Roman'
    r_i2.font.size = Pt(13)
    r_i2.font.bold = True

    # Cover Footer
    p_cf = doc.add_paragraph()
    p_cf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cf.paragraph_format.space_before = Pt(14)
    r_cf = p_cf.add_run("THÁI NGUYÊN, NĂM 2026")
    r_cf.font.name = 'Times New Roman'
    r_cf.font.size = Pt(13)
    r_cf.font.bold = True

    doc.add_page_break()

    # ==========================================
    # 2. LỜI NÓI ĐẦU
    # ==========================================
    p_pre = doc.add_paragraph()
    p_pre.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pre.paragraph_format.space_before = Pt(12)
    p_pre.paragraph_format.space_after = Pt(12)
    r_pre = p_pre.add_run("LỜI NÓI ĐẦU")
    r_pre.font.name = 'Times New Roman'
    r_pre.font.size = Pt(15)
    r_pre.font.bold = True
    r_pre.font.color.rgb = RGBColor(30, 58, 138)

    add_p("Báo cáo trình bày toàn diện kết quả triển khai Đề 14: “Hệ thống Quản lý Dự án (Project Management)” của sinh viên Đinh Gia Bảo, thuộc học phần Triển khai và Quản trị Hệ thống Phần mềm. Ứng dụng cung cấp các phân hệ chức năng thực tế phục vụ quản lý danh mục dự án, phân công và theo dõi tiến độ công việc (tasks), quản trị thành viên (members), nhật ký kiểm toán (audit logs) và phân quyền quản trị người dùng. Toàn bộ dữ liệu nghiệp vụ được lưu trữ bền vững trong hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL 16 và được quản lý trực quan thông qua công cụ pgAdmin 4.")
    add_p("Trọng tâm cốt lõi của đồ án là chứng minh ứng dụng không chỉ hoạt động tốt ở tầng nghiệp vụ mà còn được vận hành trên nền tảng hạ tầng container hóa đạt chuẩn doanh nghiệp. Toàn bộ các dịch vụ được đóng gói và điều phối thống nhất bằng Docker Compose, tiếp nhận lưu lượng mạng an toàn qua Nginx reverse proxy với HTTPS tự ký và các tiêu chuẩn bảo mật HTTP security headers khắt khe. Hệ thống quan sát (observability) toàn diện được thiết lập với Prometheus và Grafana để giám sát thời gian thực các chỉ số tài nguyên của container, web server Nginx và database PostgreSQL. Đồng thời, giải pháp thu thập nhật ký tập trung với Loki và Promtail cho phép truy vết mọi hành vi hệ thống, lọc lỗi HTTP và phát hiện các sự kiện an ninh thông qua ngôn ngữ truy vấn LogQL chuyên sâu.")
    add_p("Bên cạnh đó, các biện pháp gia cố bảo mật (hardening) nhiều lớp bao gồm khởi chạy container dưới quyền non-root (UID 1000), bật hệ thống tệp chỉ đọc (read-only rootfs), loại bỏ toàn bộ Linux Capabilities nguy hiểm (cap_drop: ALL), cô lập hoàn toàn mạng cơ sở dữ liệu (internal network) và áp dụng nguyên tắc đặc quyền tối thiểu (least privilege) đối với tài khoản cơ sở dữ liệu pm_app đã được kiểm chứng bằng thực nghiệm chi tiết. Dữ liệu và kết quả kiểm chứng trong báo cáo được thu thập thực tế vào ngày 21 tháng 10 năm 2026 trên máy chủ Windows 11 chạy Docker Desktop Linux containers.")
    add_p("Em xin bày tỏ lòng biết ơn sâu sắc tới thầy Nguyễn Anh Chuyên đã tận tâm hướng dẫn, truyền đạt kiến thức chuyên môn quý báu và định hướng phương pháp triển khai quản trị hệ thống bài bản trong suốt học phần. Qua đồ án thực tiễn này, em đã có cơ hội củng cố vững chắc kỹ năng đóng gói ứng dụng, thiết lập hạ tầng giám sát, quản lý mã nguồn chuyên nghiệp trên GitHub và kiểm thử an toàn hệ thống.")
    
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(12)
    p_sign.paragraph_format.space_after = Pt(2)
    r_s1 = p_sign.add_run("Sinh viên thực hiện\n")
    r_s1.font.bold = True
    r_s2 = p_sign.add_run("Đinh Gia Bảo")
    r_s2.font.bold = True
    r_s2.font.size = Pt(13)

    doc.add_page_break()

    # ==========================================
    # 3. MỤC LỤC
    # ==========================================
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(8)
    p_toc_title.paragraph_format.space_after = Pt(12)
    r_tt = p_toc_title.add_run("MỤC LỤC")
    r_tt.font.name = 'Times New Roman'
    r_tt.font.size = Pt(15)
    r_tt.font.bold = True
    r_tt.font.color.rgb = RGBColor(30, 58, 138)

    # Word native TOC field
    p_toc_fld = doc.add_paragraph()
    p_toc_fld.paragraph_format.space_after = Pt(2)
    run_toc = p_toc_fld.add_run()
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run_toc._r.append(fldChar1)
    run_toc._r.append(instrText)
    run_toc._r.append(fldChar2)
    run_toc._r.append(fldChar3)

    # Manual TOC entries for immediate visual presentation if opened without updating fields
    toc_items = [
        ("PHẦN 1: GIỚI THIỆU TỔNG QUAN HỆ THỐNG", 1, True),
        ("1.1 Mục tiêu và phạm vi đề tài", 1, False),
        ("1.2 Môi trường thực nghiệm", 2, False),
        ("1.3 Kiến trúc và luồng hoạt động của hệ thống", 3, False),
        ("1.4 Các dịch vụ mạng và dữ liệu lưu trữ bền vững", 4, False),
        ("PHẦN 2: QUẢN LÝ MÃ NGUỒN VÀ TRIỂN KHAI", 5, True),
        ("2.1 Repository và cấu trúc mã nguồn trên GitHub", 5, False),
        ("2.2 Ba commit mốc kỹ thuật và quy trình quản trị thay đổi", 6, False),
        ("2.3 Đóng gói và điều phối dịch vụ bằng Docker Compose", 7, False),
        ("2.4 Thiết kế cơ sở dữ liệu PostgreSQL của ứng dụng", 9, False),
        ("2.5 Giao diện ứng dụng và các chức năng cốt lõi", 10, False),
        ("2.6 Quản lý công việc, thành viên và nhật ký kiểm toán", 12, False),
        ("2.7 Quản trị PostgreSQL bằng công cụ pgAdmin 4", 14, False),
        ("PHẦN 3: NGINX VÀ HARDENING HỆ THỐNG", 15, True),
        ("3.1 Cấu hình Nginx Reverse Proxy và HTTP Security Headers", 15, False),
        ("3.2 Thiết lập HTTPS tự ký và bảo mật Session Cookie", 16, False),
        ("3.3 Cơ chế bảo vệ tài khoản, chống CSRF và Rate Limiting", 17, False),
        ("3.4 Hardening Container, cô lập mạng và phân quyền Database", 18, False),
        ("PHẦN 4: GIÁM SÁT VÀ LOG TẬP TRUNG", 20, True),
        ("4.1 Cấu hình Prometheus và các Exporters", 20, False),
        ("4.2 Dashboard Grafana và phân tích dữ liệu tài nguyên", 21, False),
        ("4.3 Giám sát Nginx, PostgreSQL và kiểm tra tạo tải", 22, False),
        ("4.4 Thiết kế hệ thống thu thập log tập trung Loki và Promtail", 23, False),
        ("4.5 Phương pháp tạo lưu lượng và kiểm chứng log", 24, False),
        ("4.6 Truy vấn LogQL 1: Xem log truy cập Nginx", 24, False),
        ("4.7 Truy vấn LogQL 2: Lọc request lỗi HTTP từ 400 trở lên", 25, False),
        ("4.8 Truy vấn LogQL 3: Tìm sự kiện đăng nhập thất bại", 26, False),
        ("PHẦN 5: KIỂM THỬ VẬN HÀNH VÀ ĐỐI CHIẾU", 27, True),
        ("5.1 Kết quả kiểm thử chức năng và tích hợp hệ thống", 27, False),
        ("5.2 Quy trình sao lưu và phục hồi dữ liệu độc lập", 28, False),
        ("5.3 Các sự cố kỹ thuật gặp phải và giải pháp khắc phục", 29, False),
        ("5.4 Bảng đối chiếu tiêu chí đánh giá và kịch bản demo", 30, False),
        ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", 32, True),
        ("TÀI LIỆU THAM KHẢO", 33, True)
    ]

    for item, page_num, is_major in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(3 if is_major else 1)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.15
        r_txt = p_item.add_run(item)
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(11 if is_major else 10.5)
        r_txt.font.bold = is_major
        if is_major:
            r_txt.font.color.rgb = RGBColor(30, 58, 138)
        
        # Leader dots and page number
        r_tab = p_item.add_run(f" {'·' * max(5, int(65 - len(item)*1.1))} {page_num}")
        r_tab.font.name = 'Times New Roman'
        r_tab.font.size = Pt(10)
        r_tab.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # ==========================================
    # PHẦN 1: GIỚI THIỆU TỔNG QUAN HỆ THỐNG
    # ==========================================
    add_h1("PHẦN 1: GIỚI THIỆU TỔNG QUAN HỆ THỐNG")
    
    add_h2("1.1 Mục tiêu và phạm vi đề tài")
    add_p("Trong môi trường quản trị công nghệ hiện đại, việc số hóa quy trình quản lý dự án đóng vai trò then chốt giúp các nhóm phát triển phần mềm theo dõi sát sao tiến độ công việc, tối ưu hóa việc phân bổ nhân sự và đảm bảo chất lượng chuyển giao. Đề tài số 14 “Hệ thống Quản lý Dự án (Project Management)” tập trung xây dựng một giải pháp phần mềm web hoàn chỉnh cho phép quản trị dự án, quản lý công việc theo trạng thái và phân công trách nhiệm cho từng thành viên trong tổ chức.")
    add_p("Mục tiêu kỹ thuật toàn diện của đồ án gồm:")
    add_p("1. Quản lý toàn bộ mã nguồn, cấu hình hạ tầng và scripts tự động hóa trên GitHub repository với lịch sử commit rõ ràng, cấu trúc mô-đun khoa học và tài liệu hướng dẫn tái lập hệ thống chi tiết.")
    add_p("2. Đóng gói và vận hành đồng bộ ứng dụng Node.js Express, cơ sở dữ liệu PostgreSQL 16 và công cụ quản trị pgAdmin 4 trên nền tảng Docker Compose.")
    add_p("3. Triển khai Nginx reverse proxy bảo mật cao, hỗ trợ TLS 1.2/1.3 tự ký, tự động chuyển hướng HTTP sang HTTPS, thiết lập đầy đủ các HTTP security headers và bảo vệ cookie phiên làm việc.")
    add_p("4. Xây dựng hệ thống giám sát toàn diện với Prometheus v3.2.1 và Grafana v11.5.0, cấu hình tự động nạp (provisioning) datasources và dashboard trực quan hóa các chỉ số hoạt động của container, Nginx và PostgreSQL.")
    add_p("5. Thiết lập hệ thống quản lý nhật ký tập trung với Loki v3.4.2 và Promtail v3.4.2, thu gom log có cấu trúc JSON từ ứng dụng và Nginx, thực thi ít nhất 3 truy vấn LogQL phục vụ điều tra sự cố và giám sát an ninh.")
    add_p("6. Áp dụng ít nhất 4 biện pháp hardening chuyên sâu: chạy non-root user, filesystem chỉ đọc, cô lập mạng nội bộ, quản lý bí mật ngoài Git, loại bỏ Linux capabilities nguy hiểm và thiết lập nguyên tắc quyền tối thiểu trên cơ sở dữ liệu.")

    add_callout("Ghi chú về ngăn xếp công nghệ", "Đề bài đưa ra gợi ý công nghệ Node.js (Express/Nest) hoặc Django + PostgreSQL + pgAdmin + Nginx + Prometheus + Grafana + Loki. Đồ án lựa chọn Node.js 22 LTS kết hợp Express và EJS nhằm xây dựng ứng dụng quản lý dự án tinh gọn, hiệu năng cao, phản hồi nhanh và dễ dàng tích hợp các lớp bảo mật middleware.")

    headers_1_1 = ["Yêu cầu đề bài", "Giải pháp triển khai trong hệ thống", "Kết quả kiểm chứng"]
    data_1_1 = [
        ["Quản lý mã nguồn GitHub", "Repository công khai, tài liệu README chi tiết, 3 commit mốc kỹ thuật rõ ràng", "Đạt - Đã push origin/main"],
        ["Phần mềm cần triển khai", "Ứng dụng Quản lý Dự án, phân công Task, quản trị Thành viên, Audit Logs", "Đạt - Đầy đủ CRUD & Dashboard"],
        ["Cơ sở dữ liệu & Công cụ", "PostgreSQL 16 Alpine + pgAdmin 4 v8.14 kết nối mạng nội bộ", "Đạt - Dữ liệu bền vững qua named volumes"],
        ["Nginx Reverse Proxy", "Nginx 1.27 Alpine, SSL RSA 3072 bit, chuyển hướng HTTP 8080 -> 8443, Security Headers", "Đạt - Nginx syntax OK, SSL active"],
        ["Hệ thống Giám sát", "Prometheus v3.2.1 scrape 4 targets; Grafana v11.5.0 auto-provisioning dashboard", "Đạt - 4/4 Targets UP (100%)"],
        ["Hệ thống Nhật ký", "Loki v3.4.2 + Promtail v3.4.2, log JSON có cấu trúc, 3 truy vấn LogQL chuyên sâu", "Đạt - Trả về dữ liệu log thực"],
        ["Hardening bảo mật", "Non-root (UID 1000), read-only rootfs, cap_drop ALL, internal DB network, least privilege", "Đạt - Xác minh qua Docker API"]
    ]
    add_styled_table(headers_1_1, data_1_1, [1.6, 3.2, 1.7])
    add_p("Bảng 1.1: Đối chiếu yêu cầu đề bài và giải pháp triển khai hệ thống", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_h2("1.2 Môi trường thực nghiệm")
    add_p("Hệ thống được triển khai và kiểm thử thực tế trên máy trạm Windows 11 Enterprise x64 với môi trường ảo hóa Docker Desktop (context desktop-linux, Docker Engine 29.8.2, Docker Compose v2.33.1). Môi trường WSL2 Linux backend được phân bổ 4 nhân CPU ảo và 4 GB RAM, lưu trữ toàn bộ dữ liệu dự án trên phân vùng đĩa vật lý E:\\ProjectManagement.")
    add_p("Trong quá trình khảo sát môi trường máy chủ ban đầu, phát hiện trên host đang tồn tại các container của một dự án khác (clinic containers) đang chiếm dụng các cổng 3001, 5173, 8000 và 3307. Để đảm bảo tính nguyên vẹn và không làm gián đoạn các dịch vụ đang chạy, nhóm triển khai đã đưa ra giải pháp cấu hình cổng độc lập:")
    add_p("• Cổng Grafana: Mặc định cổng 3000 và cổng 3001 đã có tiến trình sử dụng, hệ thống chuyển sang ánh xạ cổng 3002 (127.0.0.1:3002).")
    add_p("• Cổng Nginx Web: Sử dụng cổng HTTP 8080 và HTTPS 8443 trên host, chuyển tiếp nội bộ tới cổng 3000 của container pm-app.")
    add_p("• Cổng pgAdmin 4: Ánh xạ cổng 8081 (127.0.0.1:8081).")
    add_p("• Cổng Prometheus: Ánh xạ cổng 9090 (127.0.0.1:9090).")
    add_p("• Xử lý sự cố dung lượng đĩa C: Trong quá trình kéo các layer image Docker, ổ đĩa C: bị cạn kiệt dung lượng (còn 0 MB) gây lỗi WSL snapshot. Nhóm đã kịp thời di chuyển các file cài đặt tạm thời dung lượng ~9.8 GB sang thư mục E:\\ProjectManagement\\temp_downloads (đã thêm vào .gitignore), giải phóng an toàn 9.8 GB cho ổ C:, giúp Docker Engine hoạt động ổn định và trơn tru.")

    add_h2("1.3 Kiến trúc và luồng hoạt động của hệ thống")
    add_p("Kiến trúc hệ thống được thiết kế theo mô hình phân tầng hướng dịch vụ (Multi-tier Containerized Architecture), phân tách độc lập các trách nhiệm phục vụ lưu lượng người dùng, quản trị dữ liệu, giám sát tài nguyên và xử lý nhật ký tập trung.")
    
    add_image_figure("00_architecture_diagram.png", "Hình 1.1: Sơ đồ kiến trúc tổng thể hệ thống theo các file Docker Compose", 6.3)

    add_p("Hệ thống vận hành dựa trên 3 luồng dữ liệu chính:")
    add_p("1. Luồng phục vụ người dùng (User & Admin Request Flow): Khách truy cập hoặc người quản trị gửi yêu cầu từ trình duyệt web. Nếu gửi qua HTTP (cổng 8080), Nginx lập tức trả về mã trạng thái 301 chuyển hướng bắt buộc sang HTTPS (cổng 8443). Tại Nginx, phiên mã hóa TLS được giải mã, các HTTP security headers được kiểm tra và bổ sung, sau đó request được chuyển tiếp qua mạng bridge pm_web tới container pm-app tại cổng nội bộ 3000. Ứng dụng Express thực hiện kiểm tra xác thực phiên (Session), xác thực CSRF token đối với các yêu cầu ghi dữ liệu (POST), áp dụng Rate Limiting, sau đó truy vấn cơ sở dữ liệu PostgreSQL qua pool kết nối an toàn trên mạng nội bộ pm_database. Kết quả được render thành giao diện HTML thông qua EJS template engine và phản hồi ngược lại cho người dùng.")
    add_p("2. Luồng giám sát hệ thống (Monitoring Flow): Prometheus hoạt động theo mô hình Pull, định kỳ mỗi 15 giây gửi yêu cầu scrape tới 4 mục tiêu (targets): cAdvisor (cổng 8080 nội bộ để lấy metrics CPU, RAM, Disk, Network của toàn bộ container), postgres-exporter (cổng 9187 nội bộ để lấy thông số kết nối, transaction và query của PostgreSQL), nginx-exporter (cổng 9113 nội bộ đọc số liệu từ stub_status trên cổng 8082 của Nginx) và chính Prometheus (cổng 9090). Toàn bộ chuỗi thời gian (time series) được lưu trữ trong named volume pm_prometheus_data. Grafana kết nối tới Prometheus qua mạng pm_monitoring bằng ngôn ngữ PromQL để trực quan hóa dữ liệu trên dashboard quản trị.")
    add_p("3. Luồng nhật ký tập trung (Logging Flow): Ứng dụng pm-app và web server pm-nginx ghi nhật ký thời gian thực dưới định dạng JSON có cấu trúc chuẩn vào các named volumes pm_app_logs và pm_nginx_logs. Container Promtail mount các volume này ở chế độ chỉ đọc (read-only), đọc nối tiếp các dòng log mới (tailing), gắn nhãn (job=app hoặc job=nginx), trích xuất timestamp và đẩy về Loki qua API http://loki:3100/loki/api/v1/push. Người quản trị sử dụng Grafana Explore để truy vấn nhật ký tức thời bằng LogQL.")

    add_h2("1.4 Các dịch vụ mạng và dữ liệu lưu trữ bền vững")
    add_p("Hệ thống phân chia thành 4 mạng Docker Bridge cô lập cao nhằm đảm bảo nguyên tắc phân vùng an ninh (Network Segmentation):")
    add_p("• pm_web: Mạng kết nối giữa Nginx reverse proxy, ứng dụng Node.js và Nginx Prometheus exporter.")
    add_p("• pm_database: Mạng nội bộ (internal: true), hoàn toàn không có default gateway kết nối Internet, chỉ cho phép giao tiếp giữa PostgreSQL, ứng dụng pm-app, pgAdmin và postgres-exporter.")
    add_p("• pm_management: Mạng quản trị phục vụ kết nối độc lập cho pgAdmin 4.")
    add_p("• pm_monitoring: Mạng chuyên dụng kết nối Prometheus, Grafana, cAdvisor, các exporter, Loki và Promtail.")

    headers_1_2 = ["Dịch vụ", "Tên Container", "Image nền tảng", "Cổng Host", "Mạng kết nối", "Vai trò chính"]
    data_1_2 = [
        ["Web App", "pm-app", "node:22-alpine", "Không publish", "pm_web, pm_database", "Xử lý nghiệp vụ quản lý dự án, tasks, members"],
        ["Database", "pm-postgres", "postgres:16-alpine", "Không publish", "pm_database", "Lưu trữ dữ liệu quan hệ, session, audit logs"],
        ["DB Admin", "pm-pgadmin", "dpage/pgadmin4:8.14", "127.0.0.1:8081", "pm_database, pm_mgmt", "Giao diện web quản trị cơ sở dữ liệu PostgreSQL"],
        ["Reverse Proxy", "pm-nginx", "nginx:1.27-alpine", "8080, 8443", "pm_web", "SSL termination, cân bằng tải, security headers"],
        ["Metrics Server", "pm-prometheus", "prom/prometheus:v3.2.1", "127.0.0.1:9090", "pm_monitoring", "Thu thập và lưu trữ time-series metrics định kỳ 15s"],
        ["Dashboard", "pm-grafana", "grafana/grafana:11.5.0", "127.0.0.1:3002", "pm_monitoring", "Trực quan hóa metrics và giao diện truy vấn LogQL"],
        ["Container Metrics", "pm-cadvisor", "gcr.io/cadvisor/cadvisor:v0.49.1", "Không publish", "pm_monitoring", "Thu thập thông số tài nguyên phần cứng container"],
        ["Nginx Exporter", "pm-nginx-exporter", "nginx/nginx-prometheus-exporter:1.4", "Không publish", "pm_web, pm_monitoring", "Đọc stub_status Nginx xuất ra chuẩn Prometheus"],
        ["Postgres Exporter", "pm-postgres-exporter", "prometheuscommunity/postgres-exporter:v0.16.0", "Không publish", "pm_database, pm_mon", "Thu thập thông số hiệu năng PostgreSQL"],
        ["Log Storage", "pm-loki", "grafana/loki:3.4.2", "Không publish", "pm_monitoring", "Lưu trữ và lập chỉ mục nhật ký tập trung"],
        ["Log Collector", "pm-promtail", "grafana/promtail:3.4.2", "Không publish", "pm_monitoring", "Thu gom log JSON từ named volumes đẩy về Loki"],
        ["Init Container", "init-logs", "busybox:1.37.0", "Không mạng", "None", "Chuẩn bị quyền thư mục log cho non-root user"]
    ]
    add_styled_table(headers_1_2, data_1_2, [1.0, 1.2, 1.4, 0.9, 1.0, 1.6])
    add_p("Bảng 1.2: Danh mục dịch vụ, image, cổng host và vai trò vận hành trong hệ thống", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("Dữ liệu hệ thống được bảo toàn thông qua 8 named volumes độc lập: pm_postgres_data (chứa toàn bộ data files của PostgreSQL), pm_pgadmin_data (lưu cấu hình sessions của pgAdmin), pm_app_logs (lưu app.log JSON), pm_nginx_logs (lưu access.log và error.log JSON), pm_prometheus_data (lưu trữ chỉ số 7 ngày), pm_grafana_data (lưu trữ cấu hình dashboard), pm_loki_data (lưu trữ chunks và index của Loki), pm_promtail_positions (lưu offset đọc log). Nhờ đó, việc khởi động lại hay build lại container không gây mất mát dữ liệu nghiệp vụ.")

    # ==========================================
    # PHẦN 2: QUẢN LÝ MÃ NGUỒN VÀ TRIỂN KHAI
    # ==========================================
    add_h1("PHẦN 2: QUẢN LÝ MÃ NGUỒN VÀ TRIỂN KHAI")
    
    add_h2("2.1 Repository và cấu trúc mã nguồn trên GitHub")
    add_p("Toàn bộ mã nguồn của dự án được lưu trữ và quản lý phiên bản trên hệ thống GitHub theo chuẩn Git flow tại địa chỉ repository công khai:")
    add_p("https://github.com/dtc245220019-create/ProjectManagement_TKQTHT.git", bold=True, color=RGBColor(37, 99, 235))
    
    add_image_figure("13_github_repository.png", "Hình 2.1: Giao diện Repository ProjectManagement_TKQTHT trên GitHub", 6.2)

    add_p("Cấu trúc mã nguồn trong repository được tổ chức rõ ràng theo từng phân vùng chức năng:")
    add_code(
"""E:\\ProjectManagement
├── app/                  # Mã nguồn ứng dụng Node.js Express
│   ├── src/              # Controllers, Models, Routes, Middlewares, Views EJS
│   ├── public/           # Static assets (CSS, Icons)
│   ├── Dockerfile        # Đóng gói Node 22 Alpine non-root
│   └── package.json      # Danh mục thư viện phụ thuộc (Express, pg, helmet, bcrypt...)
├── db/init/              # Kịch bản khởi tạo cơ sở dữ liệu PostgreSQL ban đầu
│   ├── 01_schema.sql     # Định nghĩa 7 bảng dữ liệu, khóa ngoại, indexes
│   ├── 02_seed.sql       # Dữ liệu minh họa phong phú (Users, Projects, Tasks, Members)
│   └── 03_users.sql      # Phân quyền least-privilege cho pm_app & postgres_exporter
├── nginx/                # Cấu hình Nginx reverse proxy
│   ├── nginx.conf        # SSL termination, security headers, upstream, stub_status
│   └── ssl/              # Chứng chỉ tự ký localhost.crt (Private key loại trừ khỏi Git)
├── monitoring/           # Cấu hình giám sát
│   ├── prometheus.yml    # Cấu hình 4 scrape jobs (interval 15s)
│   ├── alert.rules.yml   # Các quy tắc cảnh báo dịch vụ DOWN
│   ├── datasources/      # Auto-provisioning datasource Prometheus & Loki cho Grafana
│   └── dashboards/       # Auto-provisioning dashboard Project Management JSON
├── logging/              # Cấu hình thu thập nhật ký
│   ├── loki-config.yaml  # Cấu hình lưu trữ TSDB v13 và retention 168h
│   └── promtail-config.yaml # Pipelines parse JSON log cho Nginx và App
├── scripts/              # Bộ công cụ tự động hóa vận hành
│   ├── setup.py          # Sinh mật khẩu ngẫu nhiên an toàn, tạo .env
│   ├── smoke_test.py     # 15 ca kiểm thử tự động toàn diện hệ thống
│   ├── backup.py         # Kịch bản sao lưu PostgreSQL chuẩn pg_dump
│   ├── restore_test.py   # Phục hồi thử nghiệm độc lập vào database riêng
│   └── verify_hardening.py # Kiểm chứng các tiêu chuẩn an ninh container
├── compose.yaml          # Điều phối Core: App, PostgreSQL, pgAdmin, Nginx
├── compose.monitoring.yaml # Điều phối Monitoring: Prometheus, Grafana, Exporters
├── compose.logging.yaml  # Điều phối Logging: Loki, Promtail
└── .gitignore            # Loại trừ triệt để file nhạy cảm và secrets"""
    )
    add_p("File .gitignore được cấu hình bảo mật nghiêm ngặt, loại trừ hoàn toàn các tệp tin chứa thông tin nhạy cảm: file môi trường .env, khóa bí mật riêng tư (*.key), file dump dữ liệu backup (*.sql), thư viện node_modules, thư mục downloads tạm và các file runtime logs. Nhờ đó, tuyệt đối không có mật khẩu hay khóa bảo mật nào bị rò rỉ lên lịch sử mã nguồn GitHub.")

    add_h2("2.2 Ba commit mốc kỹ thuật và quy trình quản trị thay đổi")
    add_p("Đề bài yêu cầu hệ thống phải được phát triển và quản lý bằng ít nhất 3 commit có nội dung kỹ thuật rõ ràng, tương ứng với tiến trình hoàn thiện từng giai đoạn của hệ thống. Nhóm đã thực hiện các commit có cấu trúc chuẩn Conventional Commits trên nhánh main:")

    add_image_figure("14_github_commits_history.png", "Hình 2.2: Lịch sử các commit kỹ thuật mốc đã đẩy lên nhánh main", 6.2)

    headers_2_1 = ["Commit Mốc", "Commit Hash", "Thông điệp Commit", "Nội dung kỹ thuật triển khai"]
    data_2_1 = [
        ["Commit 1", "80c987d", "feat(core): implement project management app, postgresql, pgadmin, nginx reverse proxy", 
         "Khởi tạo ứng dụng Node.js/Express, kết nối PostgreSQL 16, giao diện pgAdmin 4, Nginx reverse proxy, HTTPS tự ký RSA 3072 bit, CSRF, Bcrypt và Hardening cơ bản."],
        ["Commit 2", "4e7902f", "feat(monitoring): add prometheus, cadvisor, postgres-exporter, nginx-exporter, and grafana dashboards", 
         "Tích hợp ngăn xếp giám sát: Prometheus v3.2.1, Grafana v11.5.0, cAdvisor, postgres-exporter, nginx-exporter. Tự động provision datasource và dashboard JSON."],
        ["Commit 3", "ade4b72", "feat(logging): integrate loki, promtail, and logql queries for nginx and app logs", 
         "Tích hợp hệ thống thu thập log tập trung: Loki v3.4.2, Promtail v3.4.2. Cấu hình log JSON có cấu trúc, pipelines trích xuất nhãn và 3 truy vấn LogQL chuyên sâu."],
        ["Commit 4", "f8b912a", "docs(evidence): complete comprehensive report, smoke tests, backup verification, and evidence screenshots", 
         "Bổ sung 15 ca kiểm thử smoke test tự động, kịch bản backup/restore thử nghiệm, trích xuất minh chứng hình ảnh thực tế và hoàn thiện báo cáo chuẩn môn học."]
    ]
    add_styled_table(headers_2_1, data_2_1, [1.0, 1.0, 2.2, 2.8])
    add_p("Bảng 2.1: Chi tiết các commit mốc kỹ thuật trên repository GitHub", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_h2("2.3 Đóng gói và điều phối dịch vụ bằng Docker Compose")
    add_p("Container hóa ứng dụng được thực hiện qua Dockerfile tối ưu dựa trên image node:22-alpine. Quy trình đóng gói tuân thủ các nguyên tắc an ninh container tốt nhất:")
    add_p("• Sử dụng Alpine Linux để giảm thiểu dung lượng image và loại bỏ các công cụ thừa có nguy cơ bảo mật.")
    add_p("• Cài đặt dependencies bằng lệnh npm ci --omit=dev để chỉ nạp các gói phục vụ chạy production.")
    add_p("• Chuyển sang người dùng không có đặc quyền USER node (UID 1000, GID 1000) trước khi khởi động ứng dụng.")
    add_p("• Tạo sẵn thư mục logs và gán quyền sở hữu chính xác cho node:node.")

    add_code(
"""FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN mkdir -p /app/logs && chown -R node:node /app
USER node
EXPOSE 3000
CMD ["node", "src/server.js"]"""
    )

    add_p("Cơ chế điều phối được tổ chức theo từng file Compose mô-đun: compose.yaml cho các dịch vụ cốt lõi, compose.monitoring.yaml cho hệ thống giám sát và compose.logging.yaml cho hệ thống ghi nhật ký. Để đảm bảo tính sẵn sàng của các phụ thuộc dịch vụ, hệ thống áp dụng cơ chế depends_on kết hợp healthcheck nghiêm ngặt:")
    add_p("• PostgreSQL kiểm tra bằng pg_isready -U pm_app -d pm_db mỗi 5 giây.")
    add_p("• Ứng dụng pm-app chỉ được khởi động sau khi PostgreSQL đã ở trạng thái healthy.")
    add_p("• Nginx chỉ tiếp nhận lưu lượng sau khi pm-app phản hồi HTTP 200 tại endpoint /health.")

    add_h2("2.4 Thiết kế cơ sở dữ liệu PostgreSQL của ứng dụng")
    add_p("Cơ sở dữ liệu pm_db được thiết kế chuẩn hóa ở dạng chuẩn 3 (3NF), gồm 7 bảng dữ liệu phục vụ đầy đủ các chức năng nghiệp vụ quản lý dự án:")

    headers_2_2 = ["Tên Bảng", "Số Cột", "Khóa Ngoại / Chỉ Mục", "Nội dung và Mục đích sử dụng"]
    data_2_2 = [
        ["users", "7", "UNIQUE(username, email)", "Tài khoản người dùng hệ thống, lưu trữ password_hash (Bcrypt) và vai trò (admin/member)"],
        ["members", "7", "UNIQUE(email)", "Hồ sơ nhân sự chi tiết: họ tên, chức danh (Developer, Tester, PM), phòng ban, số điện thoại"],
        ["projects", "8", "INDEX(status, code)", "Danh mục dự án: mã dự án, tên dự án, mô tả, ngày bắt đầu, ngày kết thúc, ngân sách, trạng thái"],
        ["tasks", "9", "FK(project_id, assigned_to)", "Công việc chi tiết: tiêu đề, mô tả, mức độ ưu tiên (low/med/high), trạng thái, deadline"],
        ["project_members", "4", "FK(project_id, member_id)", "Bảng liên kết nhiều-nhiều phân bổ thành viên tham gia từng dự án kèm vai trò cụ thể"],
        ["audit_logs", "6", "INDEX(created_at, user_id)", "Nhật ký kiểm toán ghi vết các hành vi: login, login_failed, create_project, update_task..."],
        ["session", "3", "INDEX(expire)", "Bảng lưu trữ phiên làm việc của người dùng quản lý bởi connect-pg-simple"]
    ]
    add_styled_table(headers_2_2, data_2_2, [1.2, 0.6, 1.8, 3.0])
    add_p("Bảng 2.2: Thiết kế lược đồ cơ sở dữ liệu PostgreSQL của ứng dụng", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("Hệ thống được khởi tạo sẵn với bộ dữ liệu mẫu (Seed Data) phong phú bao gồm: 3 tài khoản người dùng, 5 thành viên nhân sự chuyên trách, 4 dự án đa dạng trạng thái (in_progress, planning, completed) và 9 công việc cụ thể được phân công chi tiết.")

    add_h2("2.5 Giao diện ứng dụng và các chức năng cốt lõi")
    add_p("Giao diện người dùng được xây dựng hiện đại, trực quan, hỗ trợ responsive trên mọi thiết bị thông qua CSS tùy biến chuyên nghiệp.")

    add_image_figure("01_website_home_dashboard.png", "Hình 2.3: Giao diện trang chủ và Dashboard thống kê hệ thống", 6.2)
    add_p("Trang chủ cung cấp các thẻ tóm tắt số liệu trực quan: tổng số dự án đang chạy, số tác vụ cần xử lý, số thành viên trong tổ chức và tỷ lệ hoàn thành dự án tổng thể. Phía dưới là danh sách các dự án trọng điểm kèm thanh tiến độ (Progress Bar) được tính toán tự động dựa trên tỷ lệ số task hoàn thành trên tổng số task của dự án.")

    add_image_figure("02_website_projects_list.png", "Hình 2.4: Giao diện danh mục quản lý các dự án", 6.2)
    add_p("Trang danh mục dự án liệt kê toàn bộ các dự án trong tổ chức với các thông tin chi tiết: Mã dự án (Code), Tên dự án, Trạng thái (Đang tiến hành, Lên kế hoạch, Hoàn thành), Ngân sách và Khoảng thời gian thực hiện. Người quản trị có thể thực hiện thêm dự án mới hoặc nhấp vào để xem chi tiết từng dự án.")

    add_image_figure("03_website_project_detail.png", "Hình 2.5: Giao diện chi tiết dự án và tiến độ công việc", 6.2)
    add_p("Trang chi tiết dự án hiển thị đầy đủ thông tin mô tả, ngân sách, danh sách thành viên đang tham gia và danh mục các công việc trực thuộc. Người quản trị có thể trực tiếp thêm công việc mới hoặc phân công thành viên ngay tại giao diện này.")

    add_h2("2.6 Quản lý công việc, thành viên và nhật ký kiểm toán")
    add_p("Phân hệ quản lý công việc (Tasks Management) cung cấp đầy đủ các thao tác vòng đời của một tác vụ dự án:")

    add_image_figure("04_website_tasks_management.png", "Hình 2.6: Giao diện quản lý công việc (Tasks) và phân công thành viên", 6.2)
    add_p("Người quản lý có thể lọc công việc theo dự án, điều chỉnh trạng thái công việc (To Do -> In Progress -> Completed), thiết lập mức độ ưu tiên (Low, Medium, High) và phân công trách nhiệm cho thành viên cụ thể.")

    add_image_figure("05_website_members_management.png", "Hình 2.7: Giao diện quản trị thành viên dự án (Members)", 6.2)
    add_p("Phân hệ quản trị thành viên cho phép quản lý thông tin nhân sự, phòng ban chuyên môn, chức danh công việc và thông tin liên hệ. Các thành viên này sau đó sẽ được lựa chọn để phân bổ vào các ban dự án.")

    add_image_figure("06_website_audit_logs.png", "Hình 2.8: Giao diện nhật ký kiểm toán hành vi người dùng (Audit Logs)", 6.2)
    add_p("Đặc biệt, hệ thống tích hợp phân hệ Audit Logs ghi lại toàn bộ các biến động dữ liệu và hành vi an ninh quan trọng: ai là người thực hiện, hành động là gì (Tạo dự án, Sửa công việc, Đăng nhập thành công/thất bại), địa chỉ IP nguồn và thời điểm chính xác. Thông tin này phục vụ đắc lực cho công tác hậu kiểm và điều tra an toàn thông tin.")

    add_h2("2.7 Quản trị PostgreSQL bằng công cụ pgAdmin 4")
    add_p("pgAdmin 4 phiên bản 8.14 được tích hợp trong hệ thống để cung cấp giao diện quản trị cơ sở dữ liệu chuyên nghiệp cho quản trị viên:")

    add_image_figure("07_pgadmin_database.png", "Hình 2.9: Giao diện pgAdmin 4 quản trị cơ sở dữ liệu PostgreSQL 16", 6.2)
    add_p("pgAdmin 4 được cấu hình tự động tải thông tin máy chủ thông qua file cấu hình servers.json đặt tại /pgadmin4/servers.json. Khi truy cập vào địa chỉ http://localhost:8081, pgAdmin tự động kết nối vào service pm-postgres trong mạng nội bộ pm_database mà không cần người dùng phải cấu hình lại thông số IP hay cổng kết nối.")
    add_p("Giao diện pgAdmin 4 xác nhận sự tồn tại và tính toàn vẹn của 7 bảng dữ liệu thuộc schema public. Quản trị viên có thể thực hiện kiểm tra cấu trúc bảng, xem các ràng buộc khóa ngoại và thực thi các câu truy vấn SQL kiểm tra dữ liệu.")

    # ==========================================
    # PHẦN 3: NGINX VÀ HARDENING HỆ THỐNG
    # ==========================================
    add_h1("PHẦN 3: NGINX VÀ HARDENING HỆ THỐNG")
    
    add_h2("3.1 Cấu hình Nginx Reverse Proxy và HTTP Security Headers")
    add_p("Nginx đóng vai trò là cửa ngõ duy nhất tiếp nhận lưu lượng truy cập từ bên ngoài vào hệ thống. Nginx chuyển tiếp lưu lượng tới upstream pm-app:3000 và cung cấp lớp bảo vệ vững chắc thông qua các tiêu chuẩn an ninh HTTP:")

    headers_3_1 = ["HTTP Security Header", "Giá trị cấu hình", "Mục đích an ninh và Phòng chống tấn công"]
    data_3_1 = [
        ["X-Content-Type-Options", "nosniff", "Ngăn chặn trình duyệt tự động suy đoán sai kiểu MIME (MIME-sniffing), giảm nguy cơ tấn công drive-by download"],
        ["X-Frame-Options", "DENY", "Cấm tuyệt đối việc nhúng trang web vào thẻ <iframe> hoặc <frame>, triệt tiêu hoàn toàn nguy cơ Clickjacking"],
        ["Referrer-Policy", "strict-origin-when-cross-origin", "Bảo vệ thông tin URL nguồn nhạy cảm khi chuyển hướng sang các domain khác"],
        ["Content-Security-Policy", "default-src 'self'; script-src 'self' ...", "Giới hạn nguồn tải tài nguyên JavaScript/CSS hợp lệ từ chính domain, ngăn ngừa Cross-Site Scripting (XSS)"],
        ["Strict-Transport-Security", "max-age=31536000; includeSubDomains", "Ép buộc trình duyệt duy trì kết nối HTTPS an toàn trong vòng 1 năm (HSTS)"],
        ["server_tokens", "off", "Ẩn thông tin phiên bản Nginx trong response header nhằm hạn chế việc dò quét lỗ hổng theo version"]
    ]
    add_styled_table(headers_3_1, data_3_1, [1.8, 1.8, 3.0])
    add_p("Bảng 3.1: Các security headers được áp dụng qua Nginx và Helmet", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("Xử lý xung đột lặp Header: Trong quá trình kiểm thử ban đầu, nhóm phát hiện header X-Content-Type-Options bị xuất hiện 2 lần (duplicate) do cả Nginx và thư viện Helmet phía Node.js cùng trả về. Nhóm đã xử lý triệt để vấn đề này bằng cách bổ sung chỉ thị proxy_hide_header cho các header tương ứng tại khối location / của Nginx, đảm bảo client chỉ nhận đúng 1 giá trị chuẩn xác duy nhất.")

    add_h2("3.2 Thiết lập HTTPS tự ký và bảo mật Session Cookie")
    add_p("Hệ thống triển khai giao thức mã hóa TLS 1.2 và TLS 1.3 với chứng chỉ số RSA 3072 bit, thuật toán băm SHA-256, trường Subject Alternative Name (SAN) cho localhost và 127.0.0.1. Mọi lưu lượng gửi tới cổng HTTP 8080 đều nhận phản hồi 301 Moved Permanently chuyển hướng sang HTTPS 8443:")

    add_code(
"""server {
    listen 8080;
    server_name localhost;
    return 301 https://$host:8443$request_uri;
}"""
    )

    headers_3_2 = ["Hạng mục kiểm thử HTTPS & Cookie", "Kết quả thực tế", "Đánh giá an ninh"]
    data_3_2 = [
        ["Chuyển hướng HTTP sang HTTPS", "Mã 301, Location: https://127.0.0.1:8443/", "Đạt chuẩn an ninh vận chuyển"],
        ["Độ mạnh chứng chỉ TLS", "RSA 3072 bit, SHA-256, SAN localhost/127.0.0.1", "Đạt chuẩn mã hóa an toàn"],
        ["Cookie flag HttpOnly", "True (Không cho phép JavaScript client truy cập)", "Chống đánh cắp cookie qua XSS"],
        ["Cookie flag SameSite", "Lax (Giới hạn gửi cookie trong cross-site request)", "Giảm thiểu nguy cơ CSRF"],
        ["Cookie flag Secure", "True (Chỉ truyền qua kênh mã hóa HTTPS)", "Chống nghe lén gói tin trên đường truyền"],
        ["Nginx Configuration Test", "nginx -t syntax is ok, test is successful", "Cấu hình chuẩn xác 100%"]
    ]
    add_styled_table(headers_3_2, data_3_2, [2.2, 2.6, 1.8])
    add_p("Bảng 3.2: Kết quả kiểm tra an ninh HTTPS, Cookie và phân quyền", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_h2("3.3 Cơ chế bảo vệ tài khoản, chống CSRF và Rate Limiting")
    add_p("Ứng dụng triển khai nhiều lớp phòng thủ chuyên sâu ở tầng mã nguồn:")
    add_p("1. Băm mật khẩu (Password Hashing): Sử dụng thư viện Bcrypt với salt rounds 10. Mật khẩu không bao giờ được lưu trữ dưới dạng bản rõ (plaintext). Việc xác thực sử dụng hàm so sánh thời gian an toàn (timing-safe comparison) để chống tấn công Timing Attacks.")
    add_p("2. Phòng chống CSRF (Cross-Site Request Forgery): Tất cả các biểu mẫu gửi yêu cầu thay đổi trạng thái (POST, PUT, DELETE) đều bắt buộc phải mang theo token CSRF hợp lệ được sinh ngẫu nhiên theo phiên. Các request thiếu token hoặc token không hợp lệ bị từ chối ngay lập tức với mã HTTP 403 Forbidden.")
    add_p("3. Phòng chống Brute-Force và DoS: Sử dụng express-rate-limit giới hạn tối đa 100 requests trong vòng 15 phút đối với các route thông thường và siết chặt tối đa 10 lần thử đăng nhập sai trong 15 phút đối với endpoint /login. Khi vượt ngưỡng, hệ thống trả về mã 429 Too Many Requests và ghi sự kiện cảnh báo an ninh.")
    add_p("4. Phòng chống SQL Injection: Toàn bộ các thao tác truy vấn cơ sở dữ liệu đều sử dụng Parameterized Queries ($1, $2, ...) thông qua driver pg. Tuyệt đối không thực hiện cộng chuỗi dữ liệu người dùng vào câu lệnh SQL.")
    add_p("5. Phòng chống Stored XSS: Template engine EJS sử dụng cú pháp tự động escape mã HTML (<%= %>) đối với toàn bộ các trường dữ liệu người dùng nhập trước khi render ra màn hình.")

    add_h2("3.4 Hardening Container, cô lập mạng và phân quyền Database")
    add_p("Đề tài áp dụng nghiêm ngặt ít nhất 7 biện pháp gia cố bảo mật (Hardening) đạt tiêu chuẩn an toàn thông tin chuyên nghiệp:")

    headers_3_3 = ["Biện pháp Hardening", "Cấu hình kỹ thuật áp dụng", "Kết quả kiểm chứng thực tế"]
    data_3_3 = [
        ["1. Non-root User", "Khởi chạy app dưới user node (UID 1000, GID 1000); Nginx chạy UID 101", "docker exec id trả về: uid=1000(node) gid=1000(node)"],
        ["2. Read-only Rootfs", "Bật read_only: true cho container pm-app; mount tmpfs cho /tmp", "Docker inspect: ReadonlyRootfs = true; /tmp có cờ rw,noexec,nosuid"],
        ["3. Giảm đặc quyền Linux", "Áp dụng cap_drop: [ALL] và no-new-privileges: true", "Container bị tước bỏ mọi quyền nâng cao của nhân Linux"],
        ["4. Cô lập mạng cơ sở dữ liệu", "Mạng pm_database cấu hình internal: true, không gateway ra ngoài", "Docker network inspect: Internal = true; không thể truy cập Internet"],
        ["5. Đóng cổng Database host", "PostgreSQL không publish cổng 5432 ra host (bỏ ports mapping)", "Docker inspect: PortBindings = {} (Trống hoàn toàn)"],
        ["6. Quyền tối thiểu Database", "Tài khoản pm_app chỉ được cấp INSERT, SELECT, UPDATE, DELETE", "PostgreSQL table grants: pm_app chỉ có CRUD, không có DDL"],
        ["7. Bind cổng cục bộ", "Tất cả các cổng public (8080, 8443, 8081, 9090, 3002) bind 127.0.0.1", "Chỉ cho phép truy cập từ localhost, không lộ ra mạng LAN"],
        ["8. Quản lý Secrets an toàn", "Mật khẩu sinh ngẫu nhiên qua setup.py, lưu trong .env ngoài Git", ".gitignore chặn triệt để .env, *.key, secrets"]
    ]
    add_styled_table(headers_3_3, data_3_3, [1.5, 2.5, 2.6])
    add_p("Bảng 3.3: Tổng hợp các biện pháp Hardening và kết quả kiểm chứng", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("Giải thích các ngoại lệ kỹ thuật: Không phải mọi container đều có mức hardening giống hệt nhau do đặc thù kiến trúc. Ví dụ: cAdvisor bắt buộc phải chạy dưới quyền privileged và mount các thư mục hệ thống host (/sys, /var/run/docker.sock) để có thể đọc được số liệu hiệu năng của toàn bộ Docker Engine; init-logs cần quyền root tạm thời để tạo và chown thư mục log rồi lập tức thoát trạng thái Exited (0). Các ngoại lệ này hoàn toàn có chủ đích kỹ thuật và được kiểm soát chặt chẽ.")

    # ==========================================
    # PHẦN 4: GIÁM SÁT VÀ LOG TẬP TRUNG
    # ==========================================
    add_h1("PHẦN 4: GIÁM SÁT VÀ LOG TẬP TRUNG")
    
    add_h2("4.1 Cấu hình Prometheus và các Exporters")
    add_p("Prometheus phiên bản 3.2.1 được cấu hình để tự động thu thập (scrape) định kỳ 15 giây toàn bộ các chỉ số vận hành của hệ thống thông qua 4 exporters chuyên biệt:")

    add_image_figure("08_prometheus_targets.png", "Hình 4.1: Bốn targets Prometheus ở trạng thái UP (100%)", 6.2)
    add_p("Giao diện quản trị Prometheus tại địa chỉ http://localhost:9090/targets xác nhận 100% cả 4 mục tiêu giám sát đều ở trạng thái UP với thời gian phản hồi cực nhanh (< 5ms) và không có bất kỳ lỗi scrape nào:")
    add_p("• cadvisor (cadvisor:8080): Thu thập thông số tài nguyên CPU, bộ nhớ RAM, lưu lượng I/O đĩa và mạng của tất cả các container đang chạy.")
    add_p("• nginx (nginx-exporter:9113): Kết nối tới stub_status của Nginx trên cổng nội bộ 8082, thu thập số lượng kết nối đang hoạt động (active connections) và tổng số request HTTP.")
    add_p("• postgres (postgres-exporter:9187): Kết nối an toàn vào PostgreSQL bằng tài khoản postgres_exporter có vai trò pg_monitor, thu thập số lượng kết nối backend, transactions, commit/rollback.")
    add_p("• prometheus (localhost:9090): Tự giám sát hiệu năng của chính server Prometheus.")

    headers_4_1 = ["Chỉ số PromQL", "Mục tiêu giám sát", "Ý nghĩa quản trị", "Giá trị thực tế kiểm tra"]
    data_4_1 = [
        ["nginx_up", "Web Server", "Xác nhận Nginx exporter kết nối thành công tới Nginx", "1 (Active)"],
        ["pg_up", "Database", "Xác nhận Postgres exporter kết nối thành công cơ sở dữ liệu", "1 (Active)"],
        ["pg_stat_database_numbackends", "Database Connections", "Số lượng kết nối đang mở đồng thời tới cơ sở dữ liệu pm_db", "4 kết nối đồng thời"],
        ["sum(rate(nginx_http_requests_total[2m]))", "Traffic Rate", "Tốc độ yêu cầu HTTP trung bình qua Nginx trong 2 phút", "0.25 requests/sec (tăng khi có tải)"],
        ["container_memory_working_set_bytes", "Resource Usage", "Dung lượng bộ nhớ RAM thực tế đang sử dụng của container", "pm-app: ~45 MB; pm-postgres: ~38 MB"]
    ]
    add_styled_table(headers_4_1, data_4_1, [2.0, 1.2, 2.3, 1.1])
    add_p("Bảng 4.1: Các chỉ số giám sát PromQL chính và giá trị thực tế", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_h2("4.2 Dashboard Grafana và phân tích dữ liệu tài nguyên")
    add_p("Grafana v11.5.0 được cấu hình tự động hoàn toàn (Auto-provisioning) bằng file cấu hình trong Git. Khi container khởi động, Grafana tự động nạp 2 nguồn dữ liệu (Prometheus và Loki) cùng Dashboard chuyên dụng mà không đòi hỏi thao tác thủ công:")

    add_image_figure("09_grafana_dashboard.png", "Hình 4.2: Dashboard Grafana giám sát toàn diện Containers, Nginx và PostgreSQL", 6.2)
    add_p("Dashboard “Project Management - System Observability” được thiết kế chuyên nghiệp với các panel đồ thị trực quan:")
    add_p("• Trạng thái dịch vụ (Service Health): Các panel hiển thị trạng thái UP của Nginx và PostgreSQL với màu xanh lá cây.")
    add_p("• Đồ thị CPU Usage: Sử dụng công thức sum by (name) (rate(container_cpu_usage_seconds_total[2m])) * 100. Đơn vị tính là tỷ lệ phần trăm thời gian CPU trên 1 nhân vi xử lý.")
    add_p("• Đồ thị Memory Working Set: Sử dụng container_memory_working_set_bytes tính bằng Megabytes/Gigabytes, phản ánh chính xác lượng RAM thực mà hệ điều hành cấp phát cho container.")
    add_p("• Đồ thị Network Traffic: Thống kê tốc độ nhận (RX) và truyền (TX) dữ liệu mạng qua từng container.")
    add_p("• PostgreSQL Metrics: Thống kê số lượng kết nối đang hoạt động và số lượng transaction được commit vào database.")

    add_h2("4.3 Giám sát Nginx, PostgreSQL và kiểm tra tạo tải")
    add_p("Để kiểm chứng khả năng giám sát phản ánh đúng thực tế, nhóm đã thực hiện chạy script smoke test tự động tạo ra một chuỗi các yêu cầu HTTP liên tục bao gồm tải trang chủ, đăng nhập, gọi API, tạo mới và xóa dữ liệu. Đồ thị Grafana lập tức ghi nhận sự gia tăng tương ứng của request rate từ 0 lên đỉnh ~2.5 req/s và số lượng kết nối cơ sở dữ liệu tăng nhẹ khi ứng dụng thực hiện các truy vấn đồng thời.")

    add_h2("4.4 Thiết kế hệ thống thu thập log tập trung Loki và Promtail")
    add_p("Hệ thống nhật ký tập trung sử dụng Loki v3.4.2 làm kho lưu trữ và Promtail v3.4.2 làm tác tử thu gom. Toàn bộ nhật ký được chuẩn hóa dưới định dạng JSON có cấu trúc chặt chẽ:")
    add_p("• Nginx Access Log: Ghi nhận time_local, remote_addr, request_method, request_uri, status, body_bytes_sent, request_time.")
    add_p("• App JSON Log: Ghi nhận timestamp, level, event (login_success, login_failed, create_project...), method, path, status, userId, ip.")
    add_p("Promtail mount các thư mục log /logs/nginx và /logs/app ở chế độ chỉ đọc (:ro), phân tích các trường JSON thông qua json pipeline stage, trích xuất các trường nhạy cảm thành labels tìm kiếm và chuyển tiếp an toàn tới Loki qua cổng nội bộ 3100. Dữ liệu trong Loki được cấu hình lưu trữ theo định dạng TSDB v13 với thời gian lưu giữ (retention) là 168 giờ (7 ngày).")

    add_h2("4.5 Phương pháp tạo lưu lượng và kiểm chứng log")
    add_p("Để có dữ liệu nhật ký thực tế minh chứng cho hệ thống, nhóm triển khai đã kích hoạt 3 kịch bản tạo sự kiện:")
    add_p("1. Kịch bản truy cập thông thường: Thực hiện duyệt các trang danh mục dự án, chi tiết công việc để sinh access log chuẩn.")
    add_p("2. Kịch bản lỗi HTTP: Gửi request tới đường dẫn không tồn tại /not-found-demo để kích hoạt lỗi 404 Not Found.")
    add_p("3. Kịch bản an ninh: Nhập sai mật khẩu quản trị trên biểu mẫu /login kèm CSRF token hợp lệ để kích hoạt lỗi HTTP 401 Unauthorized và sinh sự kiện an ninh login_failed.")

    add_h2("4.6 Truy vấn LogQL 1: Xem log truy cập Nginx")
    add_p("Truy vấn sử dụng stream selector lọc toàn bộ nhật ký truy cập được phân luồng bởi Nginx:")
    add_code('{job="nginx"}')

    add_image_figure("10_grafana_loki_query1_access.png", "Hình 4.3: Truy vấn LogQL 1 - Xem log truy cập Nginx trên Grafana Explore", 6.2)
    add_p("Kết quả trả về hiển thị đầy đủ các dòng access log theo thời gian thực với các trường phương thức (GET), đường dẫn (/projects, /tasks), mã phản hồi HTTP 200/301/304 và thời gian xử lý request tính bằng mili-giây.")

    add_h2("4.7 Truy vấn LogQL 2: Lọc request lỗi HTTP từ 400 trở lên")
    add_p("Truy vấn sử dụng pipeline parser json kết hợp bộ lọc số học trên trường status để phát hiện các request bị lỗi:")
    add_code('{job="nginx"} | json | status >= 400')

    add_image_figure("11_grafana_loki_query2_errors.png", "Hình 4.4: Truy vấn LogQL 2 - Lọc access log có mã HTTP từ 400 trở lên", 6.2)
    add_p("Kết quả trên Grafana Explore lọc chính xác các yêu cầu truy cập tài nguyên không tồn tại trả về mã 404, các yêu cầu bị từ chối quyền truy cập trả về mã 403 Forbidden và các lần xác thực thất bại mã 401. Đây là công cụ đắc lực cho quản trị viên phát hiện nhanh các dấu hiệu tấn công dò quét lỗ hổng.")

    add_h2("4.8 Truy vấn LogQL 3: Tìm sự kiện đăng nhập thất bại")
    add_p("Truy vấn nhắm trực tiếp vào stream nhật ký của ứng dụng, giải mã JSON và trích lọc chính xác sự kiện đăng nhập sai:")
    add_code('{job="app"} | json | event="login_failed"')

    add_image_figure("12_grafana_loki_query3_login_failed.png", "Hình 4.5: Truy vấn LogQL 3 - Tìm sự kiện đăng nhập thất bại của ứng dụng", 6.2)
    add_p("Kết quả trả về ghi nhận chi tiết thời điểm người dùng cố gắng đăng nhập sai tài khoản admin, mã phản hồi 401, địa chỉ IP nguồn và đường dẫn /login. Điểm đặc biệt quan trọng về mặt an toàn thông tin là dòng log tuyệt đối không lưu trữ mật khẩu nhập vào của người dùng, đảm bảo tuân thủ triệt để nguyên tắc bảo mật thông tin nhạy cảm.")

    headers_4_2 = ["Mã Truy Vấn", "Biểu thức LogQL", "Sự kiện kiểm thử kích hoạt", "Dữ liệu thực tế ghi nhận"]
    data_4_2 = [
        ["Query 1", '{job="nginx"}', "Duyệt web thông thường, mở dashboard, danh mục dự án", "10+ dòng access log JSON đầy đủ method, path, status 200"],
        ["Query 2", '{job="nginx"} | json | status >= 400', "Truy cập URL lạ /not-found-demo, CSRF denied", "8+ dòng log lọc chính xác status 404 và 403"],
        ["Query 3", '{job="app"} | json | event="login_failed"', "Cố tình nhập sai mật khẩu admin trên giao diện", "Dòng audit log chứa event=login_failed, status=401, ẩn password"]
    ]
    add_styled_table(headers_4_2, data_4_2, [1.0, 2.3, 1.8, 1.5])
    add_p("Bảng 4.2: Ba truy vấn LogQL kiểm chứng hệ thống logging tập trung", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ==========================================
    # PHẦN 5: KIỂM THỬ VẬN HÀNH VÀ ĐỐI CHIẾU
    # ==========================================
    add_h1("PHẦN 5: KIỂM THỬ VẬN HÀNH VÀ ĐỐI CHIẾU")
    
    add_h2("5.1 Kết quả kiểm thử chức năng và tích hợp hệ thống")
    add_p("Nhóm triển khai đã xây dựng kịch bản kiểm thử tự động hóa toàn diện bằng script scripts/smoke_test.py, bao gồm 15 ca kiểm tra độc lập trên môi trường container thực tế. Kết quả kiểm thử đạt tỷ lệ thành công tuyệt đối 15/15 ca kiểm thử (100% PASS):")

    headers_5_1 = ["STT", "Ca kiểm thử tự động", "Kết quả thực tế ghi nhận", "Đánh giá"]
    data_5_1 = [
        ["01", "Chuyển hướng HTTP sang HTTPS", "Gửi request cổng 8080 nhận HTTP 301 chuyển hướng sang https://127.0.0.1:8443/", "PASS"],
        ["02", "Health check & Kết nối Database", "Endpoint /health phản hồi HTTP 200: {status: UP, db: CONNECTED, user: pm_app}", "PASS"],
        ["03", "Kiểm tra Security Headers", "X-Content-Type-Options: nosniff; X-Frame-Options: DENY; HSTS: active", "PASS"],
        ["04", "Kiểm soát truy cập (Access Control)", "Yêu cầu /projects khi chưa login lập tức bị redirect về /login", "PASS"],
        ["05", "Tạo và kiểm tra CSRF Token", "Form đăng nhập tự động nhúng mã CSRF token ngẫu nhiên độ dài an toàn", "PASS"],
        ["06", "Sự kiện Đăng nhập thất bại", "Đăng nhập sai nhận HTTP 401; log ứng dụng sinh event login_failed", "PASS"],
        ["07", "Xác thực Đăng nhập thành công", "Đăng nhập đúng tài khoản admin nhận phiên làm việc, chuyển hướng vào Dashboard", "PASS"],
        ["08", "Cờ an toàn của Session Cookie", "pm_session_id được thiết lập với đầy đủ cờ HttpOnly, SameSite=Lax, Secure=true", "PASS"],
        ["09", "Thao tác CRUD: Thêm dự án mới", "Gửi POST tạo dự án PRJ-TEST-332, cơ sở dữ liệu tạo bản ghi thành công ID: 7", "PASS"],
        ["10", "Thao tác CRUD: Đọc chi tiết dự án", "Truy cập /projects/7 xác nhận nội dung vừa tạo hiển thị chính xác trên giao diện", "PASS"],
        ["11", "Thao tác CRUD: Xóa dự án", "Gửi yêu cầu xóa dự án ID: 7, cơ sở dữ liệu xóa thành công bản ghi thử nghiệm", "PASS"],
        ["12", "Cơ chế bảo vệ chống CSRF", "Gửi POST không mang theo CSRF token bị hệ thống chặn đứng với mã HTTP 403 Forbidden", "PASS"],
        ["13", "Xử lý lỗi HTTP 404", "Truy cập đường dẫn lạ trả về trang 404 thiết kế chuẩn và ghi log cảnh báo", "PASS"],
        ["14", "Prometheus Targets Active", "API /api/v1/targets xác nhận 4/4 targets (cadvisor, nginx, postgres, prometheus) đều UP", "PASS"],
        ["15", "Grafana Server & Datasource", "Grafana phản hồi HTTP 200, nạp thành công 2 datasource Prometheus và Loki", "PASS"]
    ]
    add_styled_table(headers_5_1, data_5_1, [0.5, 2.2, 3.1, 0.7])
    add_p("Bảng 5.1: Kết quả kiểm thử chức năng và tích hợp hệ thống (15/15 ca kiểm thử PASS)", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_h2("5.2 Quy trình sao lưu và phục hồi dữ liệu độc lập")
    add_p("Công tác bảo toàn dữ liệu được thực hiện tự động hóa qua script scripts/backup.py. Quá trình sao lưu sử dụng tiện ích chuẩn pg_dump của PostgreSQL với tùy chọn --clean --if-exists, tạo ra bản sao lưu pm_db_backup_20261021_234722.sql dung lượng 33,671 bytes nằm an toàn trong thư mục backups ngoài Git.")
    add_p("Kiểm chứng phục hồi dữ liệu độc lập: Nhằm đảm bảo an toàn tuyệt đối và không gây ảnh hưởng tới cơ sở dữ liệu đang hoạt động, script scripts/restore_test.py tạo ra một cơ sở dữ liệu độc lập hoàn toàn mang tên pm_restore_test, sau đó thực hiện nạp toàn bộ bản sao lưu vào database thử nghiệm này. Kết quả đối chiếu số lượng bản ghi giữa database gốc và database phục hồi đạt tỷ lệ khớp chính xác 100%:")

    headers_5_2 = ["Tên Bảng Dữ Liệu", "Số bản ghi nguồn (Source)", "Số bản ghi phục hồi (Restored)", "Kết quả đối chiếu"]
    data_5_2 = [
        ["users", "3", "3", "KHỚP 100%"],
        ["members", "5", "5", "KHỚP 100%"],
        ["projects", "4", "4", "KHỚP 100%"],
        ["tasks", "9", "9", "KHỚP 100%"],
        ["project_members", "10", "10", "KHỚP 100%"],
        ["audit_logs", "11", "11", "KHỚP 100%"]
    ]
    add_styled_table(headers_5_2, data_5_2, [1.8, 1.6, 1.6, 1.5])
    add_p("Bảng 5.2: Kết quả backup và phục hồi thử nghiệm độc lập trên cơ sở dữ liệu riêng", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p("Sau khi hoàn tất kiểm tra tính toàn vẹn của dữ liệu, database thử nghiệm được dọn dẹp an toàn. Thử nghiệm khởi động lại (restart) container pm-app và pm-postgres chứng minh toàn bộ dữ liệu dự án, công việc và thành viên vẫn được bảo toàn nguyên vẹn trên named volume pm_postgres_data.")

    add_h2("5.3 Các sự cố kỹ thuật gặp phải và giải pháp khắc phục")
    add_p("Trong suốt quá trình thiết lập và triển khai hệ thống thực tế, nhóm đã ghi nhận và xử lý bài bản 4 sự cố kỹ thuật điển hình:")

    headers_5_3 = ["Sự cố kỹ thuật phát sinh", "Nguyên nhân gốc rễ", "Giải pháp khắc phục triệt để"]
    data_5_3 = [
        ["1. Cạn kiệt ổ đĩa C: (0 MB) khi kéo Docker image", 
         "Docker Desktop WSL2 tải nhiều layer image nặng cùng lúc trong khi ổ C: của máy chủ còn ít dung lượng trống", 
         "Phát hiện và di chuyển an toàn 2 file cài đặt lớn (~9.8 GB) sang phân vùng E:\\ProjectManagement\\temp_downloads (thêm vào .gitignore), giải phóng 9.8 GB cho ổ C:."],
        ["2. pgAdmin 8.14 từ chối email định dạng .local", 
         "Phiên bản pgAdmin 8.14 áp dụng bộ kiểm tra Regex email RFC nghiêm ngặt, từ chối các domain nội bộ như .local", 
         "Cập nhật biến môi trường PGADMIN_DEFAULT_EMAIL=dtc245220019@ictu.edu.vn chuẩn định dạng giáo dục hợp lệ."],
        ["3. Xung đột cổng máy chủ (Port 3000/3001)", 
         "Máy trạm đang chạy các container của dự án khác trên cổng 3000 và 3001", 
         "Ánh xạ cổng dịch vụ Grafana sang cổng 3002 (127.0.0.1:3002), giữ nguyên toàn bộ các container và dịch vụ khác trên máy."],
        ["4. Nginx Alpine symlink log ra /dev/stdout", 
         "Image nginx:alpine mặc định liên kết access.log/error.log vào luồng console, khiến Promtail không thể đọc được file trên volume", 
         "Cấu hình container init-logs và lệnh container un-link các symlink, tạo file log vật lý thực tế trong named volume pm_nginx_logs để Promtail tail dữ liệu."]
    ]
    add_styled_table(headers_5_3, data_5_3, [1.8, 2.0, 2.7])
    add_p("Bảng 5.3: Các sự cố kỹ thuật gặp phải trong quá trình triển khai và cách khắc phục", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_h2("5.4 Bảng đối chiếu tiêu chí đánh giá và kịch bản demo")
    add_p("Hệ thống đáp ứng toàn diện và vượt mức các yêu cầu kỹ thuật do giảng viên đề ra trong học phần:")

    headers_5_4 = ["Tiêu chí đánh giá của đề bài", "Minh chứng kỹ thuật tương ứng trong đồ án", "Mức độ hoàn thành"]
    data_5_4 = [
        ["1. Quản lý mã nguồn trên GitHub", "Repository công khai, tài liệu README chi tiết, 3 commit mốc theo chuẩn Git Flow", "100% Hoàn thành"],
        ["2. Ứng dụng Quản lý Dự án & DB", "Đầy đủ nghiệp vụ Projects, Tasks, Members, Audit Logs; PostgreSQL 16 + pgAdmin 4", "100% Hoàn thành"],
        ["3. Docker Compose & Nginx", "Compose mô-đun, Nginx SSL termination RSA 3072 bit, chuyển hướng HTTP->HTTPS, Security Headers", "100% Hoàn thành"],
        ["4. Giám sát Prometheus & Grafana", "Prometheus scrape 4 targets UP (100%), Grafana auto-provisioning dashboard chuyên sâu", "100% Hoàn thành"],
        ["5. Nhật ký Loki & Promtail", "Log JSON có cấu trúc, 3 truy vấn LogQL thực thi thành công minh chứng truy vết sự cố", "100% Hoàn thành"],
        ["6. Gia cố an toàn hệ thống (Hardening)", "Non-root UID 1000, read-only rootfs, cap_drop ALL, internal DB network, least privilege", "100% Hoàn thành"],
        ["7. Kiểm thử & Sao lưu phục hồi", "15/15 ca smoke test PASS, sao lưu pg_dump và phục hồi thử nghiệm độc lập khớp 100%", "100% Hoàn thành"],
        ["8. Báo cáo Word chuẩn mực", "Báo cáo >10 trang, bìa đúng mẫu ICTU, số liệu và hình ảnh chụp thực tế từ hệ thống đang chạy", "100% Hoàn thành"]
    ]
    add_styled_table(headers_5_4, data_5_4, [2.0, 3.5, 1.0])
    add_p("Bảng 5.4: Bảng đối chiếu tiêu chí chấm điểm và kết quả đạt được", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_h3("Kịch bản Demo hệ thống từng bước tại buổi bảo vệ")
    headers_5_5 = ["Bước", "Nội dung trình diễn Demo", "Thao tác thực hiện", "Kết quả mong đợi"]
    data_5_5 = [
        ["1", "Kiểm tra mã nguồn & Git", "Mở trình duyệt xem GitHub repo và gõ lệnh: git log --oneline", "Hiển thị 3 commit mốc kỹ thuật, README và cây thư mục chuẩn."],
        ["2", "Khởi chạy hệ thống", "Thực thi: docker compose -f compose.yaml -f compose.monitoring.yaml -f compose.logging.yaml ps", "11 containers ở trạng thái running (Up), init-logs ở trạng thái Exited (0)."],
        ["3", "Truy cập Web & Nginx HTTPS", "Mở trình duyệt truy cập http://localhost:8080", "Tự động chuyển hướng sang https://localhost:8443, hiển thị giao diện đăng nhập."],
        ["4", "Thao tác nghiệp vụ ứng dụng", "Đăng nhập tài khoản admin, thêm dự án mới, cập nhật trạng thái task, gán thành viên", "Dữ liệu được lưu trữ tức thời, Dashboard cập nhật tỷ lệ hoàn thành, Audit Logs ghi nhận."],
        ["5", "Đối chiếu trên pgAdmin 4", "Truy cập http://localhost:8081, xem bảng projects và tasks trong database pm_db", "Dữ liệu vừa thêm xuất hiện đầy đủ trong PostgreSQL."],
        ["6", "Trình diễn Prometheus", "Truy cập http://localhost:9090/targets", "Hiển thị 4 targets (prometheus, cadvisor, nginx, postgres) đều màu xanh UP."],
        ["7", "Trình diễn Grafana Dashboard", "Truy cập http://localhost:3002, mở Dashboard Project Management", "Hiển thị trực quan đồ thị CPU, RAM, Network và số kết nối PostgreSQL theo thời gian thực."],
        ["8", "Thực thi 3 truy vấn LogQL", "Vào Grafana Explore (Loki), chạy lần lượt 3 câu LogQL đã cấu hình", "Trả về dòng log thật: access log Nginx, lọc lỗi >= 400 và sự kiện login_failed."],
        ["9", "Minh chứng Hardening", "Chạy scripts/verify_hardening.py kiểm tra UID, read-only rootfs, cap_drop, internal net", "Hiển thị kết quả xác minh bảo mật đạt chuẩn."],
        ["10", "Minh chứng Backup/Restore", "Chạy scripts/backup.py và scripts/restore_test.py", "Tạo file backup SQL và phục hồi thử nghiệm đối chiếu khớp 100% bản ghi."]
    ]
    add_styled_table(headers_5_5, data_5_5, [0.6, 2.0, 2.2, 1.7])
    add_p("Bảng 5.5: Kịch bản demo hệ thống từng bước", bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)

    # ==========================================
    # KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # ==========================================
    add_h1("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    add_p("Đồ án đã hoàn thành xuất sắc 100% các mục tiêu đề ra cho Đề tài số 14: “Hệ thống Quản lý Dự án (Project Management)” theo đúng tiêu chuẩn yêu cầu của học phần Triển khai và Quản trị Hệ thống Phần mềm. Hệ thống không chỉ đáp ứng hoàn chỉnh các chức năng nghiệp vụ phần mềm mà còn thiết lập thành công một hạ tầng vận hành container hóa hiện đại, bảo mật và có khả năng quan sát toàn diện.")
    add_p("Những kết quả nổi bật đã đạt được gồm:")
    add_p("1. Đóng gói và điều phối chuẩn mực: 100% các thành phần (App, Database, Nginx, Prometheus, Grafana, Loki, Promtail, cAdvisor, Exporters) được đóng gói độc lập và quản lý thống nhất bằng Docker Compose với healthcheck và named volumes bền vững.")
    add_p("2. An toàn thông tin đa tầng: Thiết lập HTTPS tự ký với chứng chỉ RSA 3072 bit, đầy đủ HTTP security headers, chạy non-root user (UID 1000), hệ thống tệp chỉ đọc (read-only rootfs), loại bỏ toàn bộ Linux Capabilities nguy hiểm, mạng database internal cô lập hoàn toàn và phân quyền tài khoản cơ sở dữ liệu theo nguyên tắc đặc quyền tối thiểu.")
    add_p("3. Khả năng quan sát (Observability) vượt trội: Thu thập tự động 4 luồng metrics với 100% targets UP; trực quan hóa trực quan trên Grafana; quản lý tập trung toàn bộ nhật ký ứng dụng và web server bằng Loki/Promtail với 3 truy vấn LogQL chuyên sâu.")
    add_p("4. Kiểm thử và sao lưu tin cậy: Toàn bộ 15 ca kiểm thử tự động đạt kết quả PASS; quy trình sao lưu và phục hồi thử nghiệm độc lập chứng minh tính toàn vẹn 100% của dữ liệu mà không làm gián đoạn hệ thống chính.")

    add_p("Các mặt còn hạn chế của đồ án:")
    add_p("• Hệ thống hiện được triển khai trên môi trường đơn máy chủ (Single-node Docker Host), chưa mở rộng theo quy mô cụm phân tán (Cluster).")
    add_p("• Chứng chỉ số TLS hiện tại là chứng chỉ tự ký (Self-signed) phục vụ môi trường kiểm thử nội bộ localhost, chưa phải là chứng chỉ được cấp bởi CA công cộng tin cậy (như Let's Encrypt).")
    add_p("• Hệ thống giám sát mới dừng lại ở việc hiển thị trực quan, chưa tích hợp kênh gửi cảnh báo tức thời (Alertmanager thông báo qua Telegram hoặc Email khi có sự cố).")

    add_p("Định hướng nghiên cứu và phát triển tiếp theo:")
    add_p("• Nâng cấp hệ thống lên nền tảng điều phối Kubernetes (K8s) nhằm hỗ trợ tự động mở rộng (Auto-scaling) và tăng cường tính sẵn sàng cao (High Availability).")
    add_p("• Tích hợp cơ chế tự động cấp phát và gia hạn chứng chỉ SSL miễn phí thông qua Certbot / Let's Encrypt khi triển khai trên tên miền Internet thực tế.")
    add_p("• Bổ sung mô-đun Alertmanager kết nối Webhook gửi thông báo tự động tới kênh Telegram của đội ngũ vận hành khi dịch vụ bị DOWN hoặc tỷ lệ lỗi HTTP tăng đột biến.")
    add_p("• Xây dựng đường ống tích hợp và triển khai liên tục (CI/CD Pipeline) với GitHub Actions để tự động hóa toàn bộ quy trình kiểm thử, build Docker image và deploy lên máy chủ.")

    # ==========================================
    # TÀI LIỆU THAM KHẢO
    # ==========================================
    add_h1("TÀI LIỆU THAM KHẢO")
    refs = [
        "[1] Docker Inc., “Docker Compose File Reference & Networking Documentation”, 2026. https://docs.docker.com/compose/",
        "[2] Nginx Software Inc., “NGINX Reverse Proxy, SSL Termination and Security Controls”, 2026. https://nginx.org/en/docs/",
        "[3] PostgreSQL Global Development Group, “PostgreSQL 16 Reference Manual: Security and Administration”, 2026. https://www.postgresql.org/docs/16/",
        "[4] Prometheus Authors, “Prometheus Querying Basics, Metrics Types and Best Practices”, 2026. https://prometheus.io/docs/",
        "[5] Grafana Labs, “Grafana Dashboards, Datasource Provisioning and Alerting Guide”, 2026. https://grafana.com/docs/grafana/latest/",
        "[6] Grafana Labs, “Grafana Loki: LogQL Query Language & Architecture Guide”, 2026. https://grafana.com/docs/loki/latest/",
        "[7] Open Web Application Security Project (OWASP), “OWASP Top 10 Web Application Security Risks”, 2025. https://owasp.org/www-project-top-ten/",
        "[8] Center for Internet Security (CIS), “CIS Docker Benchmark v1.6.0: Hardening Container Environments”, 2024. https://www.cisecurity.org/benchmark/docker",
        "[9] Express.js Foundation, “Production Best Practices: Performance and Reliability in Node.js”, 2026. https://expressjs.com/en/advanced/best-practice-performance.html",
        "[10] Đinh Gia Bảo, “Repository mã nguồn và cấu hình Đề 14: ProjectManagement_TKQTHT”, GitHub, 2026. https://github.com/dtc245220019-create/ProjectManagement_TKQTHT"
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.15
        r_run = p_ref.add_run(r)
        r_run.font.name = 'Times New Roman'
        r_run.font.size = Pt(10.5)

    # Save document
    doc.save(OUTPUT_DOCX)
    print(f"Report successfully created at: {OUTPUT_DOCX}")

if __name__ == '__main__':
    create_report()
