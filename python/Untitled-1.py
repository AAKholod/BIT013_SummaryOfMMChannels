import csv
import datetime

date = f"{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year}T{datetime.datetime.now().hour}:{datetime.datetime.now().minute}" 


list_a = [{"key": "value1"}, {"key": "value2"}]
list_b = []
lst = ['Преобразование', 'через', 'метод', 'join()']

result = [item for item in list_a if item not in list_b]
for i in result:
    print(f"{i.keys()} {i.values()}")  # [{'key': 'value1'}]

str_pathFile = r'C:\Users\AAKholodnova\Documents\Pix\Внутренний\Ежедневная сводка по каналам ММ\BIT013_SummaryOfMMChannels\python\file\file.csv'
str_result = ','.join(lst)

with open(str_pathFile, 'w') as file:
        file.write(str_result)