import os
import datetime

# Дата сохранения файла дд.мм.ггггТччмм
str_date = f"{datetime.datetime.now().day}{datetime.datetime.now().month}{datetime.datetime.now().year}T{datetime.datetime.now().hour}{datetime.datetime.now().minute}" 

# Место сохранения CSV файла
str_pathFile = os.path.join(os.getcwd(), "files", f"file_{str_date}.csv")

def saveCsv(list_channels):
    
    string = ''
    for el in list_channels:
        string += f"{str(el)} |" #Превращаем каждый элемент списка в строку

    with open(str_pathFile, 'w') as file:
        file.write(string)
   