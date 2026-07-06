from openai1 import OpenAI
import dotenv
dotenv.load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a short bedtime story about a unicorn."}],
)

print(response.choices[0].message.content)
