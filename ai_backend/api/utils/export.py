import csv, re
from io import StringIO, BytesIO
from weasyprint import HTML

def generate_csv(prompt):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['Prompt', 'Response'])
    text = re.sub(r'(\*|\*\*)', '', prompt.prompt_text)
    response = re.sub(r'(\*|\*\*)', '', prompt.prompt_response)
    writer.writerow([text, response])
    buffer.seek(0)
    return buffer.getvalue()

def generate_pdf(prompt):
    text = re.sub(r'(\*|\*\*)', '', prompt.prompt_text)
    response = re.sub(r'(\*|\*\*)', '', prompt.prompt_response)
    html = f"""
    <html>
        <body>
            <h1>Prompt</h1>
            <p>{text}</p>
            <h2>Response</h2>
            <p>{response}</p>
        </body>
    </html>
    """
    pdf_file = HTML(string=html).write_pdf()
    return pdf_file