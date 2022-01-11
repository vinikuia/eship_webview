import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EmailHandler():

    def __init__(self):
        # The mail addresses and password
        self.sender_address = 'vinicius.pinheiro@eship.com.br'
        self.sender_pass = 'SHL@7554'
        self.receiver_address = 'vinicius.pinheiro@eship.com.br'
        self.mail_content = '''Hello,
        This is a test mail.
        In this mail we are sending some attachments.
        The mail is sent using Python SMTP library.
        Thank You
        '''


    def sendEmail(self, fileName):
        # Setup the MIME

        self.message = MIMEMultipart()
        self.message['From'] = self.sender_address
        self.message['To'] = self.receiver_address
        self.message['Subject'] = 'A test mail sent by Python. It has an attachment.'
        # The subject line
        # The body and the attachments for the mail
        self.message.attach(MIMEText(self.mail_content, 'plain'))
        self.attach_file_name = fileName
        attach_file = open(self.attach_file_name, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        # add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=self.attach_file_name)
        self.message.attach(payload)
        # Create SMTP session for sending the mail
        self.session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        self.session.starttls()  # enable security
        self.session.login(self.sender_address, self.sender_pass)  # login with mail_id and password
        text = self.message.as_string()
        self.session.sendmail(self.sender_address, self.receiver_address, text)
        self.session.quit()
        print('Mail Sent')

