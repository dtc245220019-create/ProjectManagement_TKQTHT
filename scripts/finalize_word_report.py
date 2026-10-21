import os
import sys
import win32com.client

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

docx_path = r"E:\ProjectManagement\Bao_cao_De14_Dinh_Gia_Bao_DTC245220019.docx"
pdf_path = r"E:\ProjectManagement\Bao_cao_De14_Dinh_Gia_Bao_DTC245220019.pdf"

word = None
doc = None
try:
    print("Launching Microsoft Word Application...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False

    print(f"Opening document: {docx_path}")
    doc = word.Documents.Open(docx_path)

    print("Updating fields and Table of Contents...")
    try:
        if doc.TablesOfContents.Count > 0:
            doc.TablesOfContents(1).Update()
            print("Table of Contents updated!")
    except Exception as e:
        print(f"Note on TOC update: {e}")

    try:
        doc.Fields.Update()
    except Exception as e:
        print(f"Note on Fields update: {e}")

    pages = doc.ComputeStatistics(2) # 2 = wdStatisticPages
    words = doc.ComputeStatistics(0) # 0 = wdStatisticWords
    paras = doc.ComputeStatistics(4) # 4 = wdStatisticParagraphs

    print(f"\n==========================================")
    print(f"DOCUMENT METRICS VIA MS WORD COM:")
    print(f"  • Total Pages: {pages}")
    print(f"  • Total Words: {words}")
    print(f"  • Total Paragraphs: {paras}")
    print(f"==========================================\n")

    print(f"Saving updated document...")
    doc.Save()

    print(f"Exporting to PDF: {pdf_path}...")
    doc.SaveAs(pdf_path, FileFormat=17) # 17 = wdFormatPDF
    print("PDF successfully generated!")

except Exception as err:
    print(f"Error during Word processing: {err}")
finally:
    if doc:
        try:
            doc.Close(False)
        except Exception:
            pass
    if word:
        try:
            word.Quit()
        except Exception:
            pass
    print("Word Application closed.")
