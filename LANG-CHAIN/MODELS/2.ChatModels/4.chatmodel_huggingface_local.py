from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline  
# by using HuggingFacePipeline we can use models by downloading it in our local machine which takes lot of time and lot of gpu

llm = HuggingFacePipeline(
    model_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    pipeline_kwargs={"temperature": 0.5,"max_new_tokens": 100 }
)

chat_model = ChatHuggingFace(llm=llm)

result = chat_model.invoke("What is the capital of India?")
print(result.content)