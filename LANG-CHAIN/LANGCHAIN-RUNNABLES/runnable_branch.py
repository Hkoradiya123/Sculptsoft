from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableBranch,RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal



load_dotenv()

llm1 = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
)


parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description="Sentiment of the feedback")

parser2 = PydanticOutputParser(pydantic_object=Feedback)

chat_model1 = ChatHuggingFace(llm=llm1)

prompt1 = PromptTemplate(
    template = "Classify the sentiment of the following feedback text into positive or negative. \n{feedback} \n{format_instructions}\nReturn only the JSON object. Do not generate Python code.",
    input_variables=["feedback"],
    partial_variables={"format_instructions": parser2.get_format_instructions()}
)

prompt2 = PromptTemplate(
    template = "Write an Appropriate response to the positive feedback text like you are a real customer support agent and customer is talking with you right now \n{feedback}",
    input_variables=["feedback"]
)
prompt3 = PromptTemplate(
    template = "Write an Appropriate response to the negative feedback text like you are a real customer support agent and customer is talking with you right now \n{feedback}",
    input_variables=["feedback"]
)

classifier_chain = prompt1 | chat_model1 | parser2


branch_chain = RunnableBranch(
    (lambda x:x.sentiment == "positive", prompt2 | chat_model1 | parser), # it is called langchains if-else statement logic
    (lambda x:x.sentiment == "negative", prompt3 | chat_model1 | parser),
    RunnableLambda(lambda x: "could not find sentiment")
)
chain = classifier_chain | branch_chain
result = chain.invoke({"feedback":"The product was good"})
print(result)
chain.get_graph().print_ascii()