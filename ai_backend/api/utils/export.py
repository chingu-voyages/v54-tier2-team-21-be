import csv, re
from io import StringIO, BytesIO
from weasyprint import HTML
from django.core.mail import EmailMessage

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
    <html>
    <body style="font-size: 16px; font-family: Arial, sans-serif; color: #333333; line-height: 1.6;">
        <p style="font-size: 18px; font-weight: bold;">Hi there 👋,</p>
        
        <p style="font-size: 16px;">Thanks for using our service! Here's the prompt you submitted:</p>

        <p><strong style="font-size: 18px; color: #0056b3;">📝 Your Prompt:</strong><br>
        <span style="font-size: 16px; color: #333333;">{prompt}</span></p>

        <p><strong style="font-size: 18px; color: #0056b3;">🤖 Gemini's Response:</strong><br>
        <span style="font-size: 18px; font-weight: bold; color: #333333;">{response}</span></p>

        <br>
        <p style="font-size: 16px;">Best regards,<br>
        <strong>The 5 Star AI Team</strong></p>
    </body>
    </html>
    """
    
    from_email = "denysmelnyk262626@gmail.com"
    email_message = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[email]
    )
    email_message.content_subtype = "html" 
    email_message.send(fail_silently=False)