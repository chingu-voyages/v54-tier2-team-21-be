import csv, re
from io import StringIO, BytesIO
from weasyprint import HTML
from django.core.mail import send_mail

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

def send_email(email, prompt, response):
    subject = "5 Star AI | Your AI Prompt and Response"
    
    message = f"""
Hi there 👋,

Thanks for using our service! Here's the prompt you submitted:

📝 Your Prompt:
{prompt}

🤖 Gemini's Response:

{response}

Best regards,  
The 5 Star AI Team
"""
    from_email = "denysmelnyk262626@gmail.com"
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[email],
        fail_silently=False,
    )