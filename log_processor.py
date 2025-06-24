# log_processor.py
import requests
import os


#model_name="llama3.1"
model_name="deepseek-r1"

def analyze_logs_with_ollama(prompt: str, model_name=model_name, options=None) -> str:
    if options is None:
        options = {}

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 2048,
            "num_ctx": 4096
        }
    }

    # Обновляем параметры из options
    payload["options"].update(options)

    api_base = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
    url = f"{api_base}/api/generate"

    try:
        response = requests.post(url, json=payload, timeout=300)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Не удалось подключиться к Ollama по адресу {api_base}. Запущена ли она?")
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Запрос к Ollama превысил время ожидания ({payload.get('timeout', 300)}) секунд")
    except Exception as e:
        raise Exception(f"Ошибка при обращении к Ollama: {str(e)}")