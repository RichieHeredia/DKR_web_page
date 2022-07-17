import pandas as pd
from datetime import timedelta, date
import hashlib

class create_data():
    def __init__(self, dictionary, digi):
        self.dictionary = dictionary
        self.digi = digi
        
    def prepare_data(self):
        df = pd.DataFrame(data = [self.dictionary.values()], 
                          columns = self.dictionary.keys())
        
        
        self.digi = str(self.digi + 1)
        df['PersonID'] = self.digi
        df['gender'] = df.loc[0,'radio']
        df['username'] = str(df.loc[0,'name'][:4]) + str(df.loc[0,'cedula'][-4:])
        df['edad'] = date.today().year - int(df.loc[0,'birthdate'][:4])
        df['Date_start'] = pd.to_datetime(df['Date_start'], 
                                  infer_datetime_format=True)  

        if df.loc[0,'member_time'] == '1' :
            df['Date_end'] = df['Date_start'] + timedelta(days=30) # 1 Mes
            df['Amount_payed'] = '120000'
            df['State_mark'] = 'PREMIUM'
            
        elif df.loc[0,'member_time'] == '2':
            df['Date_end'] = df['Date_start'] + timedelta(weeks=26.0715) # 1 Semestre
            df['Amount_payed'] = '660000'
            df['State_mark'] = 'PREMIUM'
            
        elif df.loc[0,'member_time'] == '3':
            df['Date_end'] = df['Date_start'] + timedelta(weeks=56.4882) # 1 Año
            df['Amount_payed'] = '1320000'
            df['State_mark'] = 'PREMIUM'
        else :            
            df['Date_end'] = '0'
            df['Amount_payed'] = '0'
            df['State_mark'] = 'FREE'
    
        df['Pay_state'] = '1'
        df['FingerPrint'] = '0'
        df['Id_contract'] = '0'
        df['Date_ver_insta'] = date.today()
        df['Version_installed'] = '1.0.0.0'
            
        df['Date_payed'] = date.today()
        
        df['State_pay'] = '1'
        df['SheetId'] = '0'
        
        df['Data_updated'] = '0'
        df['Matriculas'] = df.loc[0,'matriculas']
        df['Image_Test'] = '0'
        df['Date_start'] = df.loc[0,'Date_start'].strftime('%Y-%m-%d')
        df['Date_end'] = df.loc[0,'Date_end'].strftime('%Y-%m-%d')
        df['Date_ver_insta'] = df.loc[0,'Date_ver_insta'].strftime('%Y-%m-%d')
        df['Date_payed'] = df.loc[0,'Date_payed'].strftime('%Y-%m-%d')
        
        df['password'] = hashlib.md5(df.loc[0,'password'].encode()).hexdigest()
        
        df = df[['PersonID','apellidos', 'name', 'gender', 'password', 
            'username','FingerPrint' ,'Membership_kind','phone', 'cedula', 'Adress_city',
            'City', 'placename', 'Date_start','Date_end', 'Pay_state',
            'Id_contract', 'edad', 'birthdate', 'email', 'Bank_sel', 
            'Version_installed', 'Date_ver_insta', 'Amount_payed', 'Date_payed', 	
            'State_pay', 'SheetId', 'State_mark', 'Kind_place', 'Data_updated', 'Image_Test',
            'Matriculas', 'member_time']]
        
        df = list(df.itertuples(index=False, name=None))
        return df






