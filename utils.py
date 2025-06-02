import httpx
import configparser
from openai import AzureOpenAI

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def call_openai_api(prompt, model):
    custom_http_client = httpx.Client(verify=False)
    openai_config = load_config()
    openai_client = AzureOpenAI(
        api_key=openai_config["azure_openai"]["api_key"],
        api_version=openai_config["azure_openai"]["api_version"],
        azure_endpoint=openai_config["azure_openai"]["endpoint"],
        http_client=custom_http_client
    )
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": f"{prompt}"}]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        print("Error during API call:", e)
        return


updated///

import httpx
import configparser
from openai import AzureOpenAI
import json

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def call_openai_with_functions(model, messages, functions, function_call):
    custom_http_client = httpx.Client(verify=False)
    config = load_config()

    client = AzureOpenAI(
        api_key=config["azure_openai"]["api_key"],
        api_version=config["azure_openai"]["api_version"],
        azure_endpoint=config["azure_openai"]["endpoint"],
        http_client=custom_http_client
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call=function_call,
            temperature=0.2
        )
        # Parse and return the function call arguments
        arguments_str = response.choices[0].message.function_call.arguments
        return json.loads(arguments_str)
    except Exception as e:
        print("Function calling failed:", e)
        return None

