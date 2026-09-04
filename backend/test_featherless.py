from openai import OpenAI 
import os 
from dotenv import load_dotenv 
load_dotenv()
client = OpenAI( api_key=os.getenv("FEATHERLESS_API_KEY"), base_url="https://api.featherless.ai/v1" )
response = client.chat.completions.create( model="Qwen/Qwen2.5-7B-Instruct", messages=[{"role": "user", "content": "Say hello in one sentence."}] ) 
print(response.choices[0].message.content) 
