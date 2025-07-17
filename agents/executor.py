import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from tools.toolkit import tools
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Ensure LangSmith tracing is enabled
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

LOG_FILE = "logs/react_agent_trace.log"
os.makedirs("logs", exist_ok=True)

def log_to_file(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}]\n{text}\n{'-'*80}\n")

def create_agent_executor():
    """Creates the ReAct agent and its executor."""
    prompt = hub.pull("hwchase17/react")
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        callbacks=[lambda x: log_to_file(str(x))]  # Logs each intermediate step
    )
    return agent_executor

def run_agent_analysis(query: str):
    """Runs the agent with a given query and returns the final output."""
    agent_executor = create_agent_executor()
    result = agent_executor.invoke({"input": query})
    log_to_file(f"Final Output: {result.get('output', 'No output generated.')}")
    return result.get("output", "No output generated.")
