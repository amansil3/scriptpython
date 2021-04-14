#! /usr/bin/env python3
from tkinter import ttk, Label, LabelFrame, Entry, StringVar, Tk, CENTER, W, E, END, Toplevel, filedialog
import pandas as pd
import numpy as np
from io import StringIO
import psycopg2
from psycopg2 import Error
from sqlalchemy import create_engine

class Product:

    def __init__(self, window):
        self.df = ''
        self.window = window
        self.window.title('Filtrador de reportes unificados')

        #Frame
        frame = LabelFrame(self.window, text = 'Menu principal')
        frame.grid(row = 0, column = 0, columnspan = 8, pady = 20)

        # Botonera
        ttk.Button(frame, text = "Importar archivo", command = self.UploadAction).grid(row = 1, column = 4, columnspan = 2, sticky = W + E)

        # Mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 2, column = 0, columnspan = 2, sticky = W + E)

        # Segundo frame
        frame2 = LabelFrame(self.window, text = 'Procesar archivo')
        frame2.grid(row = 3, column = 0, columnspan = 8, pady = 20)

        # Segunda botonera
        ttk.Button(frame2, text = "Procesar archivo", command = self.ProcessReport).grid(row = 4, column = 4, columnspan = 2, sticky = W + E)
        query = 'SELECT * FROM cliente JOIN cliente_particular ON cliente.id=cliente_particular.id_cliente ORDER BY id ASC'

    def UploadAction(self, event=None):
        '''Ventana para examinar archivo'''
        self.filename = filedialog.askopenfilename()
        try: 
            self.message['text'] = 'Archivo seleccionado:',self.filename
        except AssertionError:
            self.message['text'] = 'Por favor, seleccione un archivo'
            return

    def ProcessReport(self):
        '''Procesador de reporte'''
        #Paso 1: Seleccionar el archivo
        try: 
            File = pd.ExcelFile(self.filename)
            self.message['text'] = ''
            self.message['text'] = '25% completado'
            print ('25% completado')
        except AttributeError:
            self.message['text'] = 'Error! Elija un archivo'
            print ('Error!')
            return
        except AssertionError:
            self.message['text'] = 'Error! Elija un archivo'
            print ('Error!')
            return
        
        #Paso 2: Seleccionar la hoja 0
        try:
            self.df = File.parse('Sheet0')
            self.message['text'] = ''
            self.message['text'] = '50% completado'
            print ('50% completado')
        except ValueError:
            self.message['text'] = 'Error durante el proceso, verifique que haya elegido un reporte unificado'
            print ('Error!')
            self.filename = ''
            return
        except AttributeError:
            self.message['text'] = 'Error durante el proceso, verifique que haya elegido un reporte unificado'
            self.filename = ''
            print ('Error!')
            return

        #Paso3: Exportar a la BD
        try:
            #Report.to_excel(r'C:\Users\CIL - Andres\Desktop\Reporte_Filtrado.xlsx', index=False, encoding='utf-8')
            #Conectarse a la BD
            db_string = "postgresql://postgres:cil123@192.168.0.251:5432/webservices"
            db = create_engine(db_string)
            #Dropeo la BD
            try:
                SQL_Query = db.execute("SELECT * FROM id_solicitudes").fetchall() #query
                df2 = pd.DataFrame(SQL_Query, columns=['id','nro','anio'])  #Dataframeo la query
                df2['EstaEnLaBD?'] = np.where(self.df['Id'] == df2['id'], 'True', 'False') #agrego columna al nuevo dataframe
                df3 = df2.loc[lambda df2: df2['EstaEnLaBD?'] == 'False'] #guardo en un nuevo dataframe los registros que no esten en la bd
                
                #Verifico que el DF originado no este vacío
                if not df3.empty:
                    try:
                        #Mando el DataFrame a la Base de Datos
                        df3.to_sql('id_solicitudes', con = db, if_exists = 'replace', chunksize = 1000, index=False, index_label=False)
                        self.message['text'] = ''
                        self.message['text'] = 'Operación finalizada correctamente'
                        self.filename = ''
                    except:
                        self.message['text'] = ''
                        self.message['text'] = 'Error cargando las solicitudes'
                        print ('Error cargando las solicitudes')
                        self.filename = ''
                        return
                else:
                    self.message['text'] = ''
                    self.message['text'] = 'No hay solicitudes nuevas a cargar. Proceso finalizado correctamente'
                    print ('No hay solicitudes nuevas a cargar. Proceso finalizado correctamente')
                    self.filename = ''
            except:
                print ('Error al volcar la base de datos')
                self.filename = ''
        except:
            self.message['text'] = ''
            self.message['text'] = 'Error durante el proceso'
            print ('Error!')
            self.filename = ''
            return

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()