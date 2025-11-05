import requests
from fastapi import HTTPException


class LLMService:
    def __init__(
        self,
        api_url: str = "http://llm1.um.ac.ir:8000/v1/chat/completions",
        model_name: str = "qwen2.5-32b",
        temperature: float = 0.7,
        timeout: int = 90,
    ):
        self.api_url = api_url.rstrip("/")
        self.model_name = model_name
        self.temperature = temperature
        self.timeout = timeout

    def query(self, system_prompt: str, query: str, temperature: float | None = None) -> dict:
        """
        ارسال پرامپت به مدل داخلی و دریافت پاسخ
        """
        temp = temperature if temperature is not None else self.temperature
        payload = {
            "model": self.model_name,
            "temperature": temp,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            return {
                "response": data["choices"][0]["message"]["content"],
                "usage": data.get("usage", {}),
                "model": self.model_name,
            }

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"LLM API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise HTTPException(status_code=500, detail=f"Malformed LLM response: {str(e)}")
