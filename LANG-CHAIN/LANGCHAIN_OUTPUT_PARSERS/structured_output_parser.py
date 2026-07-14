from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser # only in old versions
from langchain.output_parsers import ResponseSchema
dotenv.load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
)

model = ChatHuggingFace(llm=llm)

schema = [
    ResponseSchema(name = "fact_1", description="first fact about the topic"),
    ResponseSchema(name = "fact_2", description="second fact about the topic"),
    ResponseSchema(name = "fact_3", description="third fact about the topic"),
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template = "Give 3 facts about {topic} \n {format_instruction}",
    input_variables=["topic"],
    partial_variables={
        "format_instruction": parser.get_format_instructions()
    }
)

chain = template | model | parser
result = chain.invoke({"topic":"black hole"})
print(result.content)   