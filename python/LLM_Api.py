import config
import requests 

class ChatAPIClient:
    def __init__(self, str_LLM_auth, str_MM_model, str_LLM_baseRequest):
        self.token = str_LLM_auth
        self.model = str_MM_model
        self.url = url
        self.headers = {
            "X-PROXY-AUTH": self.token,
            "Content-Type": "application/json"
        }

    def get_response(self, user_text):
     payload = {
        "model": self.model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": user_text
            }
        ]
     }
     response = requests.post(self.url, headers=self.headers, json=payload)
     if response.status_code == 200:
        try:
            data = response.json()
            return data["message"]["content"]
        except (ValueError, KeyError):
            return response.text
     else:
        response.raise_for_status()
          
    def build_create_json_prompt_from_products(self, user_text):
        prompt = ( 
            f"Проанализируй переписку и извлеки следующее:
            краткое резюме обсуждения, включающее основные темы и ключевые реплики участников.
            предстоящие мероприятия и следующие действия, шаги"
     )
     return prompt
    