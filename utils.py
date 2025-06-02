import configparser
import httpx
from openai import AzureOpenAI

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

async def call_openai_api_async(prompt, model):
    config = load_config()

    async with httpx.AsyncClient(verify=False, timeout=60.0) as http_client:
        client = AzureOpenAI(
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"],
            azure_endpoint=config["azure_openai"]["endpoint"],
            http_client=http_client,
        )

        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print("[❌] OpenAI API error:", e)
            return None
