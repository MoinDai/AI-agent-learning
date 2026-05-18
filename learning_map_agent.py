import os
import json
import glob
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

os.environ["ANTHROPIC_API_KEY"] = "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"

DATA_ANALYSIS_PATH = r"D:\非常非常重要的文件！！！！！\Desktop\engineering-system-data-analysis"
AGENT_PATH = r"D:\非常非常重要的文件！！！！！\Desktop\AI-agent learning"

@tool
def read_notebooks(query: str) -> str:
    """Read all .ipynb files and extract code content."""
    result = ""
    files = glob.glob(f"{DATA_ANALYSIS_PATH}/**/*.ipynb", recursive=True)
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            nb = json.load(file)
            result += f"\n\n=== {os.path.basename(f)} ===\n"
            for cell in nb.get("cells", []):
                if cell["cell_type"] == "code":
                    result += "".join(cell["source"]) + "\n"
    return result[:8000]

@tool
def read_python_files(query: str) -> str:
    """Read all .py files and extract code content."""
    result = ""
    files = glob.glob(f"{AGENT_PATH}/**/*.py", recursive=True)
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            result += f"\n\n=== {os.path.basename(f)} ===\n"
            result += file.read()
    return result[:4000]

llm = ChatAnthropic(model="claude-sonnet-4-5")
agent = create_react_agent(llm, [read_notebooks, read_python_files])

result = agent.invoke({"messages": [("human", """
Read all my Python learning files using the available tools.
Then generate a mindmap in Markmap markdown format showing everything I have learned.
Structure it as:
# My Python Learning Journey
## Data Analysis
### (libraries and methods found in notebooks)
## AI Agent
### (libraries and methods found in .py files)

Only output the markdown, nothing else.
""")]})

output = result["messages"][-1].content
print(output)

with open("learning_map.md", "w", encoding="utf-8") as f:
    f.write(output)

print("\nSaved to learning_map.md")