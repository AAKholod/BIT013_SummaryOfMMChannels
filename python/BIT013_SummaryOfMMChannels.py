import MM_Api
import SaveAsCsv
import config
from datetime import datetime
from ChatAPIClient import ChatAPIClient

def checkingDate():
    # Получение текущего дня недели
    str_currentDayOfWeek = datetime.now().strftime("%A")  # Получаем название дня недели

    # Проверка, что все дни в списке не равны текущему дню недели
    if all(day != str_currentDayOfWeek for day in config.list_acceptableWorkingDays) == True:
        
        raise Exception("Запуск не предусмотрен в данный день недели")
        
checkingDate()

MM_Api.selecting_channels()

# Инициализируем клиента ChatAPIClient
client = ChatAPIClient("8d10b6d4-2e40-42fc-a66a-c9c6bf20c92c")

LLM_Api.createRequest

        



    

