
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()
model = "gpt-5.5"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

instructions = """
You are a helpful assistant. Please provide clear and concise responses to the user's queries.
you only respond in plain/text format, without any markdown or code blocks.
you should not provide any explanations or additional information unless explicitly asked by the user.

"""

def chat(messages: list, instructions: str =instructions, model: str =model,stream: bool =False) -> str:
    params = {
        "model": model,
        "input": messages,
    }

    if instructions:  
        params["instructions"] = instructions
    if stream:
        params["stream"] = stream

    message = client.responses.create(**params)
    return message if stream else message.output_text



messages = []

add_assistant_message(messages, "Hello, How can I assist you today ?")
print("Assistant > Hello, How can I assist you today ?")
    
while True:
    try :
        user_input = input("You       > ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        add_user_message(messages, user_input)
        
        stream = chat(messages, model=model, stream=True)
        
        print("Assistant > ", end="", flush=True)

        full_response = ""

        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta.replace("\n", "\n" + " " * len("Assistant > ")), end="", flush=True)
                full_response += event.delta
        print()
        # formatted_reply = full_response.replace("\n", "\n" + " " * len("Assistant > "))

        # print(f"Assistant > {formatted_reply}")
        
        add_assistant_message(messages, full_response)
    except KeyboardInterrupt:
        print("\nExiting the chat. Goodbye!")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
    
    
# while True:
#         try :
#             user_input = input("\nYou       > \n") 
#             if user_input.lower() in ["exit", "quit"]:
#                 print("Exiting the chat. Goodbye!")
#                 break

#             add_user_message(messages, user_input)
            
#             stream = chat(messages, model=model, stream=True)
            
#             print("\nAssistant > \n", end="", flush=True)

#             full_response = ""

#             for event in stream:
#                 if event.type == "response.output_text.delta":
#                     print(event.delta, end="", flush=True)
#                     full_response += event.delta
#             print()
#             # formatted_reply = full_response.replace("\n", "\n" + " " * len("Assistant > "))

#             # print(f"Assistant > {formatted_reply}")
            
#             add_assistant_message(messages, full_response)
#         except KeyboardInterrupt:
#             print("\nExiting the chat. Goodbye!")
#             break
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         break