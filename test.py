import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

sender_email = "eventyess2023@gmail.com"
receiver_email = "eventyess2023@gmail.com"
password = "wakycmkffmdbvwhj"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
jjjjjjjjjjjj"""
html = """\
<!DOCTYPE html>
<html>
<head>
    <title>Arrival Confirmation - Wedding</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }

        h1 {
            color: #333;
            text-align: center;
        }

        p {
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 10px;
        }

        .button {
            display: inline-block;
            background-color: #333;
            color: #fff;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 20px;
        }

        .button:hover {
            background-color: #555;
        }
    </style>
</head>
<body>
    <h1>Arrival Confirmation - Wedding</h1>
    
    <p>Dear Guest,</p>
    
    <p>We are delighted to invite you to our wedding ceremony. Please confirm your arrival by clicking the link below:</p>
    
    <a href="attachment.py" class="button">Confirm Arrival</a>
    
    <p>We look forward to celebrating this special day with you!</p>
    
    <p>Best regards,</p>
    
    <p>The Bride and Groom</p>
    
    <p>If you need further information, please download our wedding brochure:</p>
    
    <a href="attachment.py" download>
        <img src="cid:image1" alt="Wedding Brochure" width="300" height="200">
    </a>
</body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Attach the image as an attachment
with open("sunflower.jpeg", "rb") as image_file:
    image = MIMEImage(image_file.read())
    image.add_header("Content-ID", "<image1>")
    message.attach(image)

# Attach the file "attachment.py"
filename = "attachment.py"
with open(filename, "rb") as file:
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", f"attachment; filename={filename}")
    message.attach(attachment)

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
