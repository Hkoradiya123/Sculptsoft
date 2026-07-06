from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client (uses OPENAI_API_KEY from .env)
client = OpenAI()
model = "gpt-4o-mini"  # You can change to "gpt-4", "gpt-4o", etc.

def add_user_message(conversation, content):
    """Appends a user message to the conversation history."""
    conversation.append({
        "role": "user",
        "content": content  
    })

def add_assistant_message(conversation, content):
    """Appends an assistant message to the conversation history, cleaning up formatting."""
    cleaned_content = content.replace("**", "").replace("##", " ")
    conversation.append({
        "role": "assistant",
        "content": cleaned_content
    })

def chat(conversation, system=None, stop_sequences=None, stream=False):
    """
    Sends conversation history to OpenAI.
    Returns the full response text string (if stream=False) or streams the response.
    """
    # Build messages array with system prompt if provided
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.extend(conversation)

    # Prepare parameters
    params = {
        "model": model,
        "max_tokens": 500,
        "messages": messages,
    }
    if stop_sequences:
        params["stop"] = stop_sequences  # OpenAI uses 'stop' not 'stop_sequences'

    if stream:
        # Streaming response
        full_response = ""
        stream_obj = client.chat.completions.create(**params, stream=True)
        for chunk in stream_obj:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                full_response += text
        print()  # New line after streaming
        add_assistant_message(conversation, full_response)
        return full_response
    else:
        # Non-streaming response
        response = client.chat.completions.create(**params)
        response_text = response.choices[0].message.content
        add_assistant_message(conversation, response_text)
        return response

def ask_ai(conversation, question, system=None, stop_sequences=None, stream=False):
    """Helper to add a user question and get OpenAI's response."""
    add_user_message(conversation, question)
    return chat(conversation, system=system, stop_sequences=stop_sequences, stream=stream)

if __name__ == "__main__":
    conversation = []
    
    prompt = input("Enter your prompt: ")

    print("Sending prompt to OpenAI...")
    print("-" * 50)

    # Add user message
    add_user_message(conversation, prompt)

    # Add initial assistant message to start the code block
    # add_assistant_message(conversation, "```json")

    # Run the non-streaming chat call with stop sequence
    chat_response = chat(
        conversation,
    )

    print("\n" + "-" * 50)
    print("Full Response:")
    print("-" * 50)

    # Print the response content
    if hasattr(chat_response, 'choices'):
        # If we got the full response object
        print(chat_response.choices[0].message.content)
    else:
        # If we got just the text
        print(chat_response)

    print("\n" + "-" * 50)
    print("Conversation History:")
    print("-" * 50)
    for msg in conversation:
        print(f"{msg['role'].upper()}: {msg['content'][:100]}...")
