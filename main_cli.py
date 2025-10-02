import asyncio
import os 
from dotenv import load_dotenv
from llama_index.core.agent.workflow import ReActAgent, AgentStream, ToolCallResult
from llama_index.core.workflow import Context
from llama_index.llms.ollama import Ollama
from engines.note_engine import note_engine
from engines.app_engine import app_engine
from engines.document_engine import document_tool  
from prompts import react_header
from tracker.tracker import GroqRequestTracker

load_dotenv()

# from llama_index.llms.groq import Groq
# llm = Groq(model="groq/compound", api_key=os.getenv("GROQ_API_KEY"))

llm = Ollama(
    model="qwen3:4b",
    request_timeout=30.0,
    context_window=8000,
)


agent = ReActAgent(
    tools=[note_engine, app_engine, document_tool],
    llm=llm,
    max_iterations=1
)

agent.update_prompts({"react_header": react_header})

async def prompt_agent(prompt):

        handler = agent.run(prompt)
        
        # ENABLE FOR DEBUGGING / READING AGENT THOUGHTS

        async for ev in handler.stream_events():
            if isinstance(ev, ToolCallResult):
                print(f"\n[DEBUG] Call {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
            if isinstance(ev, AgentStream):
                print(f"{ev.delta}", end="", flush=True)

        response = await handler

        return response


async def main():
    
    tracker = GroqRequestTracker()

    while (prompt := input("\nEnter a prompt (q to quit): ")) != "q":

        try:
            response = await tracker.send_request(prompt_agent, prompt)
            print(str(response))
        except Exception as e:
            print(e)

    print(tracker.get_stats())

if __name__ == "__main__":
    asyncio.run(main()) 


