from flask import Flask, render_template, request
import csv
from redmail import outlook
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
            
            self.__credentials = service_account.Credentials.from_service_account_file('creds.json', 
                                                                                        scopes=SCOPES)
            self.__spreadsheet_service = build('sheets', 'v4', 
                                            credentials=self.__credentials)
            self.__drive_service = build('drive', 'v3', 
                                        credentials=self.__credentials)
            
            self.__authenticated = True
            
            return self.__authenticated, self.__spreadsheet_service
            print ("Session authenticated")
        except Exception as e:
            print ("ERROR EN PROCESO DE AUTENTICACION : {}".format(e))
    
    def get_last_row(self):
        """ get the last row of our_clients for append a new row"""
        response = self.__spreadsheet_service.spreadsheets().values().get(
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
        
        self.__spreadsheet_service.spreadsheets().values().update(
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
    Kind_place = SelectField('Actividad', choices = [('1', 'Gym') , 
                                                     ('2', 'Baile'), 
                                                     ('3', 'Boxeo'),
                                                     ('4', 'Karate'),
                                                     ('5', 'Ingles')] )    
    Date_start = DateField('Fecha Inicio', validators=[InputRequired('A birth date is required!')])    
    Bank_sel = SelectField('Banco', 
                            choices = [('NEQUI', 'Nequi') , 
                                      ('DAVIPLATA', 'Daviplata'), 
                                      ('BANK ACCOUNT', 'Otro Banco')], 
                            validate_choice=True)   
    
    member_time = SelectField('Plan Seleccionado', choices = [('1', 'Mensual') , 
                                                              ('2', 'Semestral'), 
                                                              ('3', 'Anual')] )
    
    matriculas = SelectField('Plan Matriculas', choices = [('0', 'No matriculas') , 
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
        send_report(data['name'], str(data['phone']) , data['message'], data['email'], )         
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




def send_report(name, phone:str, message, email_to):
    
    with open('classy2.txt', 'rb') as file:
        text = file.read()
    
    new_text = text.decode().replace('USUARIO_REPORTE',name)
    new_text = new_text.replace('TELEFONO_REPORTE', phone).replace('MENSAJE_REPORTE', message)
    
    with open('classy2.html', 'w') as file:
        file.write(new_text)
        
    outlook.username = "serviciosknr@outlook.com"
    outlook.password = "KikeDaniRichie123"

    outlook.send(
        receivers=[email_to],
        subject='Gracias por comunicarte',
        html=new_text,
        body_images={
         'image1': 'images/KR_LOGO.png',
         'image11': 'images/t7_image11.jpg',
         'ico_contact' : 'images/t7_ico_phone.jpg',
         'ico1': 'images/t7_ico1.jpg',
         'ico2': 'images/t7_ico2.jpg',
         'ico3': 'images/t7_ico3.jpg',
         'ico_email': 'images/t7_ico_email.jpg',
         'ico_facebook': 'images/t7_ico_facebook.jpg',
         'ico_instagram': 'images/t7_ico_instagram.jpg',
         'ico_linkedin': 'images/t7_ico_linkedin.jpg',
         'ico_phone': 'images/t7_ico4.jpg',
         'ico_twitter': 'images/t7_ico_twitter.jpg',
         'image12': 'images/t7_image12.jpg'
        }
    )
    

        
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