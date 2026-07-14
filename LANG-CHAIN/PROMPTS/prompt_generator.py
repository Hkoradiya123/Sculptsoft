from langchain_core.prompts import PromptTemplate

tempelate = PromptTemplate(
    input_variables=["paper", "style", "length"],
    template="""
    You are a helpful assistant that summarizes academic papers.
    Paper: {paper}
    Style: {style}
    Length: {length}
    """
)

tempelate.save("prompt_template.json")