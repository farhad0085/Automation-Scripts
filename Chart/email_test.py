import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from email.mime.base import MIMEBase
from email import encoders

MY_ADDRESS = 'farhadhossain0085@gmail.com'
PASSWORD = 'rwwcpcarnddkpjrg'

def main():

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()       # create a message

    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']='farhadhossain0085@gmail.com'
    msg['Subject']="This is TEST"
    
    # add in the message body
    msg.attach(MIMEText("Hello this is test", 'plain'))

    part = MIMEBase('application', "octet-stream")
    with open('report.png', 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="{}"'.format(Path('report.png').name))
    msg.attach(part)
    
    # send the message via the server set up earlier.
    s.send_message(msg)
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()