from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate

import smtplib
from string import Template
from pathlib import Path

from flask import Flask, render_template, request
import csv
from flask_wtf import FlaskForm

#%%
from wtforms import StringField, TextAreaField, BooleanField
from wtforms import PasswordField, SubmitField, RadioField, DateField
from wtforms import IntegerField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo
from forms import create_data
#%%
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os


curr_path = os.path.dirname(os.path.abspath(__file__))
curr_path = str(curr_path) + "\\" + '..\\'

# curr_path = ""
print ("CURRENT PATH :  {}".format(curr_path))
#%%

class connexion_our_clients():

    def __init__(self):
        self.__authenticated = False
        self.sheetId_OUR_CLIENTS = '1YPlzUXTHdrJjMwYzPRrYVU0_xCM7-F0jONDFCWe13-0'


    def auth_account (self):
        '''
        Authentication function
        Get the credentials and autenticate into API
        Create the Services for execute the actions into spreadsheet
        Build service to made actions into Google Drive
        '''
        try:
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive']

            self.credentials = service_account.Credentials.from_service_account_file('/home/serviciosdkr/DKR_web_page/creds.json',
                                                                                        scopes=SCOPES)
            self.spreadsheet_service = build('sheets', 'v4',
                                            credentials=self.credentials)
            self.drive_service = build('drive', 'v3',
                                        credentials=self.credentials)

            self.__authenticated = True

            return self.__authenticated, self.__spreadsheet_service
            print ("Session authenticated")
        except Exception as e:
            print ("ERROR EN PROCESO DE AUTENTICACION : {}".format(e))

    def get_last_row(self):
        """ get the last row of our_clients for append a new row"""
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive']

        self.credentials = service_account.Credentials.from_service_account_file('/home/serviciosdkr/DKR_web_page/creds.json',
                                                                                        scopes=SCOPES)
        self.spreadsheet_service = build('sheets', 'v4',
                                            credentials=self.credentials)
        response = self.spreadsheet_service.spreadsheets().values().get(
            spreadsheetId = self.sheetId_OUR_CLIENTS,
            range='Cli_Vig!A1:A'
            ).execute()

        self.last_row = len(response['values']) + 1
        return response['values'][-1]

    def write_data(self, values):
        """Write data inputed in form or web page """

        value = values

        value_range_body = {
            'majorDimension': 'ROWS',
            'values': value
            }

        self.spreadsheet_service.spreadsheets().values().update(
            spreadsheetId = self.sheetId_OUR_CLIENTS,
            valueInputOption = 'USER_ENTERED',
            range = 'Cli_Vig!A' + str(self.last_row),
            body = value_range_body
            ).execute()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thematrix'

class MyForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired('A name is required!')])
    apellidos = StringField('Apellidos', validators=[InputRequired('A last name is required!')])
    birthdate = DateField('birth date', validators=[InputRequired('A birth date is required!')])
    radio = RadioField('Gender', default = 'Male' , choices = [('Male', 'Male') ,
                                                                 ('Female', 'Female')])
    kind_id = StringField('Tipo Identificación', validators=[InputRequired('A Id card is required!')])
    cedula = IntegerField('N° Identificación', validators=[InputRequired('A Id card is required!')])
    phone = IntegerField('Celular', validators=[InputRequired('A Celular is required!')])
    email = StringField('Correo', validators=[InputRequired('A Correo is required!')])
    pais = SelectField('Pais', choices = [('co', 'Colombia') , ('pe', 'Perú'), ('Mex', 'Mexico')] )
    City = SelectField('Ciudad', choices = [('bogota', 'Bogotá') , ('cali', 'Cali'), ('medellin', 'Medellín')] )
    Adress_city = StringField('Dirección', validators=[InputRequired('A name is required!')])
    placename = StringField('Nombre Lugar', validators=[InputRequired('A name is required!')])
    Kind_place = SelectField('Tipo de Academia', choices = [('1', 'Gym') ,
                                                     ('2', 'Baile'),
                                                     ('3', 'Boxeo'),
                                                     ('4', 'Karate'),
                                                     ('5', 'Ingles'),
                                                     ('6', 'Otro')] )
    Date_start = DateField('Fecha Inicio', validators=[InputRequired('A birth date is required!')])
    Bank_sel = SelectField('Metodo de Pago',
                            choices = [('NEQUI', 'Nequi') ,
                                      ('DAVIPLATA', 'Daviplata'),
                                      ('BANK ACCOUNT', 'Otro Banco')],
                            validate_choice=True)

    member_time = SelectField('Suscripcion a DK&R', choices = [('1', 'Mensual') ,
                                                              ('2', 'Semestral'),
                                                              ('3', 'Anual'), ('4', 'Free')] )

    matriculas = SelectField('Cuentas con Matriculas', choices = [('0', 'No matriculas') ,
                                                              ('1', 'Mensual'),
                                                              ('6', 'Semestral'),
                                                              ('12', 'Anual')] )

    Membership_kind = SelectField('Tipo de pagos', choices = [('1', 'Fechas') ,
                                                              ('1', 'Asistencias'),
                                                              ('3', 'Asistencias y Tiempo'),
                                                              ('4', 'Dias')] )

    facebook = StringField('Facebook', validators=[InputRequired('A name is required!')])
    insta = StringField('Instagram', validators=[InputRequired('A name is required!')])
    password = PasswordField('Contraseña', validators=[InputRequired('Password is required!'),
                                                       EqualTo('password_2',
                                                       message='Passwords must match'),
                                                       Length(min=8, max=15)])

    password_2 = PasswordField('Repita contraseña', validators=[InputRequired('Password is required!')])
    condiciones =  BooleanField('conditions', validators=[InputRequired('A Id card is required!')])



@app.route('/')
def Principal():
    return render_template('index_.html')

@app.route('/conocenos')
def Biblioteca():
    return render_template('about_us.html')

@app.route('/servicios')
def Inscripcion():
    return render_template('services.html')

@app.route('/blog')
def Blog():
    return render_template('blog.html')

@app.route('/terms_conditions')
def Terms_Conditions():
    return render_template('politics.html')

class Info_form(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired('A name is required!')])
    email = StringField('Email', validators=[InputRequired('A Correo is required!')])
    phone = IntegerField('Celular', validators=[InputRequired('A Celular is required!')])
    message = TextAreaField('Ingrese Mesansaje', validators=[InputRequired('A last name is required!')])

@app.route('/contactanos', methods=['GET', 'POST'])
def Contact():
    form_cli = Info_form()
    if form_cli.validate_on_submit():
        data =  form_cli.data
        send_mail(data)
        return render_template('index_.html')
    return render_template('contact_us.html', form = form_cli)

@app.route('/Clientes', methods=['GET', 'POST'])
def form():
    form = MyForm()
    print('Mostrando la pagina')
    if form.validate_on_submit():
        data = request.form.to_dict()
        prueba = connexion_our_clients()
        prueba.auth_account()
        last = prueba.get_last_row()
        prepare = create_data(data, int(last[0]))
        tupl = prepare.prepare_data()
        prueba.write_data(tupl)
        return render_template('about_us.html', form = form)

    return render_template('_index.html', form = form)




def send_mail(data,
              subject = 'Gracias por comunicarte con nosotros',
              send_from = 'serviciosknr@gmail.com',
              server='smtp.gmail.com',
              port=587,
              username='serviciosknr@gmail.com',
              password='pxfmffaylisptntc',
              use_tls=True):

    curr_path = os.path.dirname(os.path.abspath(__file__))
    ruta_template = '/home/serviciosdkr/DKR_web_page/classy2.html'

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = data['email']
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    # Record the MIME types of both parts - text/plain and text/html.
    html_ = Template(Path(ruta_template).read_text(encoding='Utf-8',))
    html_fin  = html_.substitute({'USUARIO': data['name'],
                                  'TELEFONO':data['phone'],
                                  'MENSAJE':data['message']})

    part3 = MIMEText(html_fin, 'html')
    """
    src = ['<logo>', '<icon_ben_1>', '<icon_ben_2>',
     '<icon_ben_3>', '<right_ima>', '<con_ico_1>', '<con_ico_3>',
     '<map_img>', '<ico_row>', '<ico_fb>', '<ico_ig>', '<ico_link>', '<ico_tw>']
    """

    src = ['<image1>', '<image11>', '<ico_contact>',
     '<ico1>', '<ico2>', '<ico3>', '<ico_email>',
     '<ico_facebook>', '<ico_instagram>', '<ico_linkedin>', '<ico_phone>', '<ico_twitter>', '<image12>']

    dic_src = {}


    image_email = ['/home/serviciosdkr/DKR_web_page/images/KR_LOGO.png',
                   '/home/serviciosdkr/DKR_web_page/images/t7_image11.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico_phone.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico1.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico2.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico3.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico_email.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico_facebook.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico_instagram.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico_linkedin.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico4.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_ico_twitter.jpg',
                   '/home/serviciosdkr/DKR_web_page/images/t7_image12.jpg']

    for i in range(len(image_email)):
        dic_src[src[i]] = image_email[i]

    for cid, ruta in dic_src.items():
        fp = open(ruta, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        # modify the HTML file in SRC image and change for ---cid:image1---
        msgImage.add_header('Content-ID', cid)
        msgImage.add_header('Content-Disposition',
                            'inline',
                            filename=os.path.basename(ruta))
        msgImage.add_header("Content-Transfer-Encoding", "base64")
        msg.attach(msgImage)

    msg.attach(part3)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, data['email'], msg.as_string())
    smtp.quit()
    return True



def write_database_csv(data):
    with open('database2.csv', mode='a',newline = '') as database2:
        nombre = data["nombre"]
        email = data["email"]
        telefono = data["telefono"]
        ciudad = data["ciudad"]
        ocupacion = data["ocupacion"]
        quien = data["quien"]
        csv_writer = csv.writer(database2, delimiter = ',',quotechar="'", quoting= csv.QUOTE_MINIMAL)
        csv_writer.writerow([nombre,email,telefono,ciudad,ocupacion,quien])




class SignUpForms(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Sing Up')

if __name__ == '__main__':
    app.run(debug = True)
