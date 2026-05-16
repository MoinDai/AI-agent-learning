import os
from pypdf import PdfReader
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

os.environ["ANTHROPIC_API_KEY"] = "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"

def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

doc_a_text = read_pdf("C:/ocgt/OCGT_Document_A_OEM_Specification.pdf")
doc_b_text = read_pdf("C:/ocgt/OCGT_Document_B_Maintenance_Report.pdf")

@tool
def validate_ocgt_data(query: str) -> str:
    """Read and validate OCGT turbine data from two PDF documents."""
    return f"DOCUMENT A:\n{doc_a_text}\n\nDOCUMENT B:\n{doc_b_text}"

llm = ChatAnthropic(model="claude-sonnet-4-5")
agent = create_react_agent(llm, [validate_ocgt_data])
result = agent.invoke({"messages": [("human", "Please read both OCGT documents, compare all technical parameters, identify inconsistencies and generate a validation report.")]})
print(result["messages"][-1].content)