import requests 

def selecting_channels(dict_headers, str_baseRequest, str_botId, str_teamId):
    """
    собрать каналы, которые соотвествуют требованиям 
    """

    # Все каналы у бота
    get_url = f"{str_baseRequest}/users/{str_botId}/teams/{str_teamId}/channels"
            
    # Отправка GET запроса на сервер
    response = requests.get(get_url, headers=dict_headers)
       
    # Проверка успешности запроса
    if response.status_code == 200:
        print("Каналы успешно собраны")
    else:
        raise IOError(f"Ошибка при получении информации по каналам : {response.text}")

    jsonEl_channels = response.json()
    
    # Отсеить личные чаты ("") и default
    list_jsonChannelsInfo = [
    el for el in jsonEl_channels
    if el.get("display_name") not in ["", "Off-Topic", "ex Town Square"]
    ]
    
    #Список каналов к удалению
    list_channelsToDelete = []
    
    # Цикл для каждого канала
    for jsonEl_channel in list_jsonChannelsInfo:
        # Id канала
        str_chatId = jsonEl_channel.get("id")
        
        # Количество участников канала
        get_url = f"{str_baseRequest}/channels/{str_chatId}/stats"

        # Отправка GET запроса на сервер
        response = requests.get(get_url, headers=dict_headers)
       
        # Проверка успешности запроса
        if response.status_code == 200:
            print("Информация об участниках канала успешно собраны")
        else:
            raise IOError(f"Ошибка при получении информации об участников каналу: {response.text}")

        jsonEl_channelMembers = response.json()

        # Если количество участников канала == 1
        if int(jsonEl_channelMembers.get("member_count")) == 1:
            list_channelsToDelete.append(jsonEl_channel)
        elif response.status_code != 200:
            raise IOError("Ошибка при получении информации об участников каналу")
    
    # Убрать каналы на удаление
    list_jsonChannelsInfo = [item for item in list_jsonChannelsInfo if item not in list_channelsToDelete]

    return list_jsonChannelsInfo

    