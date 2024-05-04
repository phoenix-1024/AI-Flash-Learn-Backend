from dotenv import load_dotenv
from openai import AsyncOpenAI
from os import getenv
load_dotenv()


class llama_model:
    # gets API Key from environment variable OPENAI_API_KEY
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
    )
    
    general_config = {
        "model_name": "meta-llama/llama-3-70b-instruct"
        "temperature": 0,
    }
    def __init__(self) -> None:
        pass

    async def generate_content(self, content,**kwargs):
        config = self.general_config.copy()
        # if key word arguments are supplied we overwrite the general config
        if len(kwargs) > 0:
            for k,v in kwargs.items():
                config[k] = v
        
        completion = await self.client.chat.completions.create(
                messages=[
                    {
                    "role": "user",
                    "content": content,
                    },
                ],
                **config
            )
        return completion.choices[0].message.content
model = llama_model()
