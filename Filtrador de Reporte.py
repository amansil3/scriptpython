import pandas as pd
from io import StringIO
#from tabulate import tabulate

File2 = pd.ExcelFile(r'C:\Users\CIL - Andres\Desktop\Reporte Unificado (5).xls')
df2 = File2.parse('Sheet0')
Report = df2.iloc[:,[0,1,2]]

Report.to_excel(r'Reporte_Filtrado.xlsx', index=False, encoding='utf-8')

#%USERPROFILE%\AppData\Local\Microsoft\WindowsApps
#C:\Users\CIL - Andres\AppData\Local\Programs\Microsoft VS Code\bin