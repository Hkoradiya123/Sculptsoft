from openai import OpenAI
import os
import openai
from dotenv import load_dotenv
load_dotenv()

# # Initialize the client
# client = OpenAI()

# # Call the Responses API with the web_search tool enabled
# response = client.responses.create(
#     model="gpt-5.5", # Example supported model
#     tools=[{"type": "web_search"}],
#     input="What is the latest todays 20-7-25 headline?"
# )

# print(os.environ.get("OPENAI_API_KEY"))
