import smtplib
from pathlib import Path
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
from email import encoders
import os

def send_mail(send_to, 
              name:str, 
              ruta_template, 
              image_email, 
              logo, 
              files=[],
              subject = 'Informe Mensual - PDF y Excel',
              send_from = 'serviciosknr@gmail.com',
              server='smtp.gmail.com', port=587, 
              username='serviciosknr@gmail.com', 
              password='pxfmffaylisptntc',
              use_tls=True):
    
    """Compose and send email with provided info and attachments.
    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
     
    # Record the MIME types of both parts - text/plain and text/html.
    html_ = Template(Path(ruta_template).read_text())
    html_fin  = html_.substitute({'name': name})   

    part3 = MIMEText(html_fin, 'html')
    
    logo = logo
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    fp = open(image_email, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()    
    # modify the HTML file in SRC image and change for ---cid:image1---
    msgImage.add_header('Content-ID', '<image1>')
    msgImage.add_header('Content-Disposition', 
                        'inline', 
                        filename=os.path.basename(logo))
    msgImage.add_header("Content-Transfer-Encoding", "base64")
    msg.attach(part3)
    msg.attach(msgImage)
    


    for path in files:
       part = MIMEBase('application', "octet-stream")
       with open(path, 'rb') as file:
           part.set_payload(file.read())
       encoders.encode_base64(part)
       part.add_header('Content-Disposition',
                       'attachment; filename={}'.format(Path(path).name))
       msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    return True
    


if __name__ == "__main__":
    print ("TESTING CORREOS")
    curr_path = os.path.dirname(os.path.abspath(__file__))
    curr_path = str(curr_path) + "\\"
    
    # curr_path = ""
    print ("CURRENT PATH :  {}".format(curr_path))
    BUILD_PDF_ROUTE = curr_path + "../Correo_informe_clientes"
    
    send_mail('serviciosknr@gmail.com',
            'RICHIE', 
            '/home/serviciosdkr/DKR_web_page/correos/index.html',
            '/home/serviciosdkr/DKR_web_page/correos/images/person_2.jpg',
            '/home/serviciosdkr/DKR_web_page/correos/images/person_2.jpg')
    print('Email sended')


