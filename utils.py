import configparser
import httpx
from openai import AsyncAzureOpenAI

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

async def async_openai_chat(prompt, model):
    config = load_config()
    client = AsyncAzureOpenAI(
        api_key=config["azure_openai"]["api_key"],
        api_version=config["azure_openai"]["api_version"],
        azure_endpoint=config["azure_openai"]["endpoint"],
        http_client=httpx.AsyncClient(verify=False)
    )
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Async OpenAI API call failed:", e)
        return None
