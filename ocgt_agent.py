import os
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

os.environ["ANTHROPIC_API_KEY"] = "api-key"

@tool
def validate_ocgt_data(query: str) -> str:
    """Validate OCGT turbine data from two documents and check for inconsistencies."""
    doc_a = {"rated_power_MW": 150, "efficiency_pct": 38.5, "co2_kg_per_mwh": 490}
    doc_b = {"rated_power_MW": 152, "efficiency_pct": 37.8, "co2_kg_per_mwh": 495}
    inconsistencies = []
    for key in doc_a:
        if doc_a[key] != doc_b[key]:
            inconsistencies.append(f"{key}: Document A = {doc_a[key]}, Document B = {doc_b[key]}")
    if not inconsistencies:
        return "All parameters consistent."
    return "INCONSISTENCIES FOUND:\n" + "\n".join(inconsistencies)

llm = ChatAnthropic(model="claude-sonnet-4-5")
agent = create_react_agent(llm, [validate_ocgt_data])
result = agent.invoke({"messages": [("human", "Please validate the OCGT turbine data and generate a report.")]})
print(result["messages"][-1].content)