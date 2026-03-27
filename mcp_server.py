from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_content",
    description="Read the contents of a file and return as string",
)
def read_document(
    doc_id: str = Field(description="Id of the document to read"),
) -> str | None:
    if doc_id not in docs:
        raise ValueError(f"Identification {doc_id} not found.")
    return docs[doc_id]


@mcp.tool(
    name="edit_doc_content",
    description="Edit the contents of a file and return as string",
)
def edit_document(
    doc_id: str = Field(description="Id of the document to modify"),
    old_str: str = Field(description="The text to replace"),
    new_str: str = Field(description="The text to be inserted"),
) -> None:
    if doc_id not in docs:
        raise ValueError(f"Identification {doc_id} not found.")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)


@mcp.resource(
    "docs://documents",
    mime_type="application/json",
    description="A list of all documents in the system",
)
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
    description="The contents of a particular document",
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Identification {doc_id} not found.")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(
    doc_id: str = Field(description="Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""

    return [base.UserMessage(prompt)]


# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
