from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

dotenv.load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(gt = 18,description="Age of the person")
    city: str = Field(description="City of the person") # gt = greater than

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template = "Give me the name, age and city of a fictional {place} person.\n{format_instruction}\nIMPORTANT: Return ONLY the JSON object. Do not include markdown formatting, code blocks, or any other text.",
    # here i need to define it to give in json format because llm gives other content likr here is your answer and etc so define to give only json as answer
    input_variables=["place"],
    partial_variables={
        "format_instruction": parser.get_format_instructions()
    }
)

chain = template | model | parser
result = chain.invoke({"place":"indian"})


print(result)