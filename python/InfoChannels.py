import requests 
import logging
import csv
from datetime import timedelta, datetime

def selecting_channels(dict_headers, str_baseRequest, str_botId, str_teamId):
    """
    собрать каналы, которые соотвествуют требованиям 
    """

    # Запрос на сервер - Все каналы у бота
    get_url = f"{str_baseRequest}/users/{str_botId}/teams/{str_teamId}/channels"
            
    # Отправка GET запроса на сервер
    response = requests.get(get_url, headers=dict_headers)
       
    # Проверка успешности запроса
    if response.status_code == 200:
        logging.info("Каналы успешно собраны")
    else:
        logging.error(f"Ошибка при получении информации по каналам: {response.text}")
        raise Exception(f"Error {response.status_code}: {response.text}")
    
    jsonEl_channels = response.json()
    
    # Отсеить личные чаты ("") и default
    list_jsonChannelsInfo = [
    el for el in jsonEl_channels
    if el.get("display_name") not in ["", "Off-Topic", "ex Town Square"]
    ]
    
    #Список каналов к удалению (default)
    list_channelsToDelete = []
    
    # Цикл для каждого канала
    for jsonEl_channel in list_jsonChannelsInfo:
        
        # Id канала
        str_chatId = jsonEl_channel.get("id")
        
        # Запрос на сервер - Количество участников канала
        get_url = f"{str_baseRequest}/channels/{str_chatId}/stats"

        # Отправка GET запроса на сервер
        response = requests.get(get_url, headers=dict_headers)
       
        # Проверка успешности запроса
        if response.status_code == 200:
            logging.info(f"Информация об участниках канала <{jsonEl_channel.get("display_name")}> успешно собраны")
        else:
            logging.error(f"Ошибка при получении информации об участниках канала <{jsonEl_channel.get("display_name")}>:\n{response.text}")
            raise Exception(f"Error {response.status_code}: {response.text}")

        jsonEl_channelMembers = response.json()

        # Если количество участников канала == 1
        if int(jsonEl_channelMembers.get("member_count")) == 1:
            list_channelsToDelete.append(jsonEl_channel)
        elif response.status_code != 200:
            logging.error(f"Количество участников канала <{jsonEl_channel.get("display_name")}> равно 1")
            raise Exception(f"Error {response.status_code}: {response.text}")
    
    # Убрать каналы на удаление
    list_jsonChannelsInfo = [item for item in list_jsonChannelsInfo if item not in list_channelsToDelete]

    return list_jsonChannelsInfo

def selecting_infoChannels(dict_headers, str_baseRequest, list_jsonChannelsInfo):
    
    """
    собрать информацию о каналах (участники канала - ФИО, посты канала)
    """
    # Список отсортированной информации по каналам (default)
    list_sortedChannelsInfo = []

    # Цикл для каждого канала
    for jsonEl_channel in list_jsonChannelsInfo:

        # Все участники канала (default)
        list_channelMembers = []

        # Запрос на сервер -  Id всех участников канала
        get_url = f"{str_baseRequest}/channels/{jsonEl_channel.get("id")}/members?per_page=1000"

        # Отправка GET запроса на сервер
        response = requests.get(get_url, headers=dict_headers)
       
        # Проверка успешности запроса
        if response.status_code == 200:
            logging.info(f"Информация по участникам канала <{jsonEl_channel.get("display_name")}> успешно собрана")
        else:
            logging.error(f"Ошибка при получении участников канала <{jsonEl_channel.get("display_name")}>:\n{response.text}")
            raise Exception(f"Error {response.status_code}: {response.text}")
        
        jsonEl_members = response.json()

        # Цикл для каждого участника
        for jsonEl_member in jsonEl_members:

            # Запрос на сервер - Id всех участников канала
            get_url = f"{str_baseRequest}/users/{jsonEl_member.get("user_id")}"

            # Отправка GET запроса на сервер
            response = requests.get(get_url, headers=dict_headers)
       
            # Проверка успешности запроса
            if response.status_code != 200:
                logging.error(f"Ошибка при получении информации об участнике канала <{jsonEl_channel.get("display_name")}>:\n{response.text}")
                raise Exception(f"Error {response.status_code}: {response.text}")
            
            jsonEl_channelMembers = response.json()

            # Участники канала
            dict_member = {
                'UserId': str(jsonEl_channelMembers.get("id")),
                'UserName': str(f"{jsonEl_channelMembers.get('first_name')} {jsonEl_channelMembers.get('last_name')}"),
                'UserNickname': str(jsonEl_channelMembers.get("username")),
                }

            list_channelMembers.append(dict_member)

        logging.info("Информация об участниках успешно собрана")

        # Запрос на сервер - Все посты канала
        get_url = f"{str_baseRequest}/channels/{jsonEl_channel.get("id")}/posts?per_page=1000"

        # Отправка GET запроса на сервер
        response = requests.get(get_url, headers=dict_headers)
       
        # Проверка успешности запроса
        if response.status_code == 200:
            logging.info(f"Посты канала <{jsonEl_channel.get("display_name")}> успешно собраны")
        else:
            logging.error(f"Ошибка при получении постов канала <{jsonEl_channel.get("display_name")}>:\n{response.text}")
            raise Exception(f"Error {response.status_code}: {response.text}")

        jsonEl_posts = response.json()

        # Все посты канала (default)
        list_channelPosts = []

        # Список свойств постов
        list_namePropertiesOfPosts = list(jsonEl_posts.get("posts").keys())

        # Кол-во дней минус (default)
        int_days = 0
        
        # Если день запуска понедельник 
        if datetime.now().strftime("%A") == "Monday":
            int_days = 7
        elif datetime.now().strftime("%A") == "Wednesday":
            int_days = 14
        elif datetime.now().strftime("%A") != "Wednesday" and datetime.now().strftime("%A") != "Monday":
            int_days = 7

        date = datetime.now() - timedelta(days=int_days)

        # Список постов сообщений
        list_sortedPostsInfo = [
            {
                "CreateAt": datetime.fromtimestamp(
                    jsonEl_posts['posts'][property]['create_at'] / 1000
                    ), 
                "RootId": str(jsonEl_posts['posts'][property]['root_id']),
                "UserId": str(jsonEl_posts['posts'][property]['user_id']),
                "Property": property
            }
                for property in list_namePropertiesOfPosts
                if datetime.fromtimestamp(jsonEl_posts['posts'][property]['create_at'] / 1000) >= date
            ]
        
        # 
        if len(list_sortedPostsInfo) != 0:
            # Отсортировать согласно хронологии
            list_sortedPostsInfo = sorted(list_sortedPostsInfo, key=lambda post: post['CreateAt'])

            # Для каждого поста
            for dict_post in list_sortedPostsInfo:

                # Посты текущей ветки (default)
                str_messages = ""

                # Если НЕ пустое И встречается Property встречается у других RootId => обсуждение (ветка)
                if dict_post["RootId"] == "" and any(post["RootId"] == dict_post["Property"] for post in list_sortedPostsInfo):

                    # Первый пост
                    str_messages = f"UserId [ {dict_post["UserId"]} ] CreateAt : {dict_post["CreateAt"]} Message - {jsonEl_posts.get("posts").get(dict_post["Property"]).get("message")}"      
                    
                    # Все последующие в последовательной хронологии
                    list_othersMessages = [
                        {
                            "Message": f"{jsonEl_posts.get("posts").get(post["Property"]).get("message")}",
                            "UserId": f"{post["UserId"]}",
                            "Property": f"{post["Property"]}",
                            "CreateAt": f"{post["CreateAt"]}"
                        } 
                        for post in list_sortedPostsInfo
                        if post["RootId"] == dict_post["Property"]
                    ]
                    
                    # Отсортировать согласно хронологии
                    list_othersMessages = sorted(list_othersMessages, key=lambda post: post['CreateAt'])

                    #Получить строку с постами под первым постом
                    str_otherMessages = '\n'.join(
                        f"UserId [ {post['UserId']} ] CreateAt : {post['CreateAt']} Message - {jsonEl_posts['posts'][post['Property']]['message']}"
                        for post in list_othersMessages
                    )

                    #Получить всё обсуждение (всю ветку)
                    str_messages = f"{str_messages}\n{str_otherMessages}"
                    
                    list_channelPosts.append(str_messages)
                
                elif dict_post["RootId"] == "" and all(post["RootId"] == dict_post["Property"] for post in list_sortedPostsInfo) == False:
                    # Пост
                    str_messages = f"UserId [ {dict_post["UserId"]} ] CreateAt : {dict_post["CreateAt"]} Message - {jsonEl_posts.get("posts").get(dict_post["Property"]).get("message")}"      
                    
                    list_channelPosts.append(str_messages)
         
        else:
            list_channelPosts.append("За требуемый промежуток времени нет новых сообщений")
        
        # Сформировать данные о канале
        dict_infoChannel = [
            "ChannelName", f"{jsonEl_channel.get("display_name")}",
            "URL", f"https://mm.1bit.support/birpa/channels/{jsonEl_channel.get("name")}",
            "Purpose", f"{jsonEl_channel.get("purpose")}",
            "Members", list_channelMembers,
            "Messages", list_channelPosts
        ]
        
        list_sortedChannelsInfo.append(dict_infoChannel)
    
    
    return list_sortedChannelsInfo

