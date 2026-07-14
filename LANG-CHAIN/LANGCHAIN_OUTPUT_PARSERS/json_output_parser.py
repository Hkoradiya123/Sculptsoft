# this hugging face models doesnt give structured output
# so we need to use output parser to convert the output to structured format
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser  

dotenv.load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
)

model = ChatHuggingFace(llm=llm)

parser = JsonOutputParser()

template = PromptTemplate(
    template="Give me the name, age and city of a fictional person \n {format_instruction}",
    input_variables=[],
    partial_variables=
        {
            "format_instruction": parser.get_format_instructions() # json structure in output is decided my llm
            
        }   
    
)
# without chain 

### prompt = template.format()
### result = model.invoke(prompt)

### final_result = parser.parse(result.content) 
### print(final_result) 
### print(type(final_result)) 


# with chain
chain = template | model | parser
result = chain.invoke({})
print(result)
print(type(result))

