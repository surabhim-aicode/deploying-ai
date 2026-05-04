import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

sys.path.append('../../05_src/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, "../../.secrets")
load_dotenv('../../../05_src/.secrets')
API_GATEWAY_KEY = os.getenv("API_GATEWAY_KEY")
load_dotenv(dotenv_path)

#print(os.getenv("API_GATEWAY_KEY"))

client = OpenAI(base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
                api_key='any value',
                default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')})

class ToolService:
    def __init__(self):
        self.websearch_mcp = {
             "type": "mcp",
             "server_label": "openai-websearch-mcp",
             "description": "Useful for answering questions about current events or general knowledge. Can search the web for relevant information to include in the response.",
             "server_url": "https://glama.ai/mcp/servers/ConechoAI/openai-websearch-mcp"
      
        }

        #Local testing 
    # messages=[
    # {"role": "user", "content": "What's the latest news on AI?"},
    # {"role": "assistant", "content": "Let me check the web for the latest news on AI..."}
    # ]

    def handle(self, messages):
        response = client.responses.create(
    model="gpt-4o-mini",
    input=messages,
    #tools=[self.websearch_mcp],
    tool_choice="auto"
)
        return response.output_text
 
