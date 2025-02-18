from typing import List, Dict
import aiohttp

class ChatService:
    def __init__(self):
        self.deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"
        self.deepseek_api_key = "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"

    async def get_movie_recommendations(self, user_message: str) -> Dict:
        try:
            print(f"Procesando mensaje: {user_message}")  # Debug
            
            # Hacer una simple llamada a Deepseek para obtener una respuesta
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.deepseek_api_url,
                    headers={
                        "Authorization": f"Bearer {self.deepseek_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {
                                "role": "system",
                                "content": "Eres un experto en cine amigable. Recomienda películas basadas en lo que pide el usuario."
                            },
                            {
                                "role": "user",
                                "content": user_message
                            }
                        ]
                    }
                ) as response:
                    if response.status != 200:
                        text = await response.text()
                        print(f"Error de Deepseek: {text}")  # Debug
                        raise Exception(f"Error al obtener respuesta: {text}")

                    data = await response.json()
                    response_text = data["choices"][0]["message"]["content"]
                    
                    return {
                        "response": response_text,
                        "movies": []  # Por ahora dejamos la lista de películas vacía
                    }

        except Exception as e:
            print(f"Error en get_movie_recommendations: {str(e)}")
            raise e 