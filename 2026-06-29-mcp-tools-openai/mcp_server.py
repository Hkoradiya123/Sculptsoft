import sys
import os
import traceback

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server_error.log")

try:
    from mcp.server.fastmcp.prompts import base
    from typing import Annotated
    from pydantic import Field
    from mcp.server.fastmcp import FastMCP
except Exception as e:
    with open(log_file_path, "w") as f:
        f.write("IMPORT ERROR:\n")
        f.write(traceback.format_exc())
    raise e

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation of ai call center.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

#  Write a tool to read a doc

@mcp.tool(
    name="read_doc_content",
    description="Read the content of document and return it as string.",
)
def read_doc_content(doc_id: Annotated[str, Field(description="id of document to read")]) -> str:
    if doc_id not in docs:
        raise ValueError(f"Could not find document with id: {doc_id}")
    return docs[doc_id]


#  Write a tool to edit a doc
    
@mcp.tool(
    name = "edit_document",
    description = "Edit a document by replacing a string in content with a new string."
)
def edit_document(
    doc_id: Annotated[str, Field(description="id of document to edit")],
    old_str: Annotated[str, Field(description="string to be replaced")],
    new_str: Annotated[str, Field(description="replacement string")],
) :
    if doc_id not in docs:
        raise ValueError(f"Could not find document with id: {doc_id}")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return docs[doc_id]

#  Write a resource to return all doc id's

@mcp.tool(
    name = "list_doc_ids",
    description = "List all the document ids."
)
def list_doc_ids() -> list[str]:
    return list(docs.keys())

@mcp.resource("docs://documents",mime_type="application/json")
def list_docs() ->   list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
    description="Get the content of a particular document.",
)
def get_document_content(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Could not find document with id: {doc_id}")
    return docs[doc_id]

#  Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name = "format",
    description = "reformat the document in proper markdown format"
)
def format_document(doc_id: str = Field(description="id of document to format")) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:

    {doc_id}


    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra formatting.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """
    
    return [
        base.UserMessage(prompt)
    ]
    


#  Write a prompt to summarize a doc
@mcp.prompt(
    name="summarize",
    description="Summarize a document.",
)
def summarize(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Could not find document with id: {doc_id}")
    return f"Please summarize the following document:\n\n{docs[doc_id]}"


if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write("RUN ERROR:\n")
            f.write(traceback.format_exc())
        raise e
