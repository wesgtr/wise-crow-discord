from openai import OpenAI
import os
import importlib
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

MODEL_CONFIG = os.getenv('MODEL_CONFIG')

config_module = importlib.import_module(f'gpt_models.{MODEL_CONFIG}_config')
MODEL_NAME = config_module.MODEL_NAME
MODEL_METHOD = config_module.MODEL_METHOD


def get_response(conversation):
    if MODEL_METHOD == "ChatCompletion":
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation
        )
    else:
        raise ValueError(f"Unknown MODEL_METHOD: {MODEL_METHOD}")
    return response
