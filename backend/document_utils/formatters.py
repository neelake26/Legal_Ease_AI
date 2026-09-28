from io import BytesIO

from docx import Document
from reportlab.pdfgen import canvas


def as_txt(content):
    return content


def as_docx(content):
    doc = Document()
    doc.add_paragraph(content)

    buffer = BytesIO()
    doc.save(buffer)

    return buffer.getvalue()


def as_pdf(content):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)
    text_object = pdf.beginText(50, 800)
    text_object.setFont("Helvetica", 11)

    for line in content.splitlines():
        text_object.textLine(line)

    pdf.drawText(text_object)
    pdf.save()

    return buffer.getvalue()