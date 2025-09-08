import config
import InfoChannels
import SaveAsCsv

"""

[Схема запроса]

{http://your-mattermost-url.com}/api/v4/{request}


Информация по каналу:


Имя канала - display_name

https://mm.1bit.support/api/v4/channels


Ссылка - https://mm.1bit.support/birpa/channels/{name}

https://mm.1bit.support/api/v4/channels


Назначение канала - purpose

https://mm.1bit.support/api/v4/channels


Участники - 

https://mm.1bit.support/api/v4/channels/{str_teamId}/members => user_id 

=> https://mm.1bit.support/api/v4/users/{user_id} => ФИО


"""


# Список json с информацией каналов (default)
list_jsonChannelsInfo = []

# Список отсортированной информации по каналам
list_sortedChannelsInfo = []

# Заголовки запроса, включающие авторизацию через Bearer токен
dict_MM_headers = {"Authorization": f"Bearer {config.str_MM_token}"} 
 

def selecting_channels():

    global list_jsonChannelsInfo

    list_jsonChannelsInfo = InfoChannels.selecting_channels(dict_MM_headers, config.str_MM_baseRequest, config.str_MM_botId, config.str_MM_teamId)

    return list_jsonChannelsInfo

selecting_channels()

def selecting_infoChannels():

    global list_sortedChannelsInfo 

    list_sortedChannelsInfo = InfoChannels.selecting_infoChannels(dict_MM_headers, config.str_MM_baseRequest, list_jsonChannelsInfo)
    return list_sortedChannelsInfo

# Eсли список пуст 
if len(list_jsonChannelsInfo) == 0:
    raise Exception("Нет каналов, которые удовлетворяют требованиям.")

else:
    selecting_infoChannels()

    # Если список пуст 
    if len(list_sortedChannelsInfo) == 0:
        raise Exception("Пустой список с информацией по каналам")
    else:
        SaveAsCsv.saveCsv(list_sortedChannelsInfo)


