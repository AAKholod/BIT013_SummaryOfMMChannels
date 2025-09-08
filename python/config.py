
# Ссылка на сервер [без / в конце]
str_MM_mmURL = "https://mm.1bit.support".rstrip('/')

# База для запроса к ММ [без / в конце]
str_MM_baseRequest = f"{str_MM_mmURL}/api/v4".rstrip('/')

# Id команды BI&RPA в ММ
str_MM_teamId = "j5xmb3iie3n6txowdfu8adn3ma"

# Id Бота в ММ
# str_MM_botId = "rs94jpsgsjyn9jk4waha1q5n3o"
str_MM_botId = "rs94jpsgsjyn9jk4waha1q5n3o"

# Токен бота в ММ
str_MM_token = "w47rsnizppdxu8a7wexx5hc45a"

# Пример списка допустимых рабочих дней (в зависимости от дня недели будет браться разная хронология постов в ММ)
list_acceptableWorkingDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]



# X-PROXY-AUTH ИИ
str_LLM_auth = "8d10b6d4-2e40-42fc-a66a-c9c6bf20c92c"

# База для запроса к ИИ [без / в конце]
str_LLM_baseRequest = "https://llm.1bitai.ru/api/chat"

# Модель ИИ
str_MM_model = "llama3.3:70b"