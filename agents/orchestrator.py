"""
Astra — Master Orchestrator Agent
Receives complex tasks, reasons about them, routes to specialist agents
Shows live thinking process in Streamlit
"""

import os
import time
from dotenv import load_dotenv
from groq import Groq
import httpx

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    http_client=httpx.Client()
)

AGENTS = {
    "hr": "Handles HR policy questions, leave requests, compensation queries",
    "sales": "Handles revenue analysis, pipeline questions, deal insights",
    "finance": "Handles P&L, budget, cost analysis, financial forecasting",
    "sdr": "Handles lead finding, company research, outreach drafting",
    "research": "Handles web research, market analysis, competitor intel",
    "general": "Handles general enterprise questions not covered by specialists",
}

ORCHESTRATOR_PROMPT = """You are the Astra Master Orchestrator. You receive complex enterprise tasks and:
1. Break them into subtasks
2. Assign each subtask to the right specialist agent
3. Synthesize results into a final response

Available agents:
- HR Agent: HR policies, leave, compensation
- Sales Agent: Revenue, pipeline, deal analysis  
- Finance Agent: P&L, budget, forecasting
- SDR Agent: Lead finding, research, outreach
- Research Agent: Web research, market intel
- General Agent: Everything else

For each task, respond in this exact format:
THINKING: [your reasoning about the task]
PLAN:
- [Agent Name]: [specific subtask]
- [Agent Name]: [specific subtask]
EXECUTING: [what you're doing now]
RESULT: [final synthesized answer]"""

def route_to_agent(task: str, agent: str) -> str:
    """Route a subtask to the appropriate specialist agent"""
    
    if agent == "hr":
        from agents.ask_hr import ask_hr
        result = ask_hr(task)
        return result["answer"]
    
    elif agent == "sales":
        from agents.sales_copilot import ask_sales
        result = ask_sales(task)
        return result["answer"]
    
    elif agent == "research":
        try:
            from tavily import TavilyClient
            tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            result = tavily.search(task, max_results=3)
            snippets = [r.get("content", "") for r in result.get("results", [])]
            return "\n".join(snippets[:3])
        except Exception as e:
            return f"Research result: {task} (web search unavailable: {e})"
    
    else:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are an enterprise AI specialist handling {agent} tasks. Be specific and data-driven."},
                {"role": "user", "content": task}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content

def orchestrate(task: str, stream_container=None) -> dict:
    """
    Main orchestration function
    stream_container: Streamlit container for live updates
    """
    
    steps = []
    
    def update(msg: str, step_type: str = "info"):
        steps.append({"msg": msg, "type": step_type})
        if stream_container:
            if step_type == "thinking":
                stream_container.info(f"🧠 {msg}")
            elif step_type == "routing":
                stream_container.warning(f"⚡ {msg}")
            elif step_type == "result":
                stream_container.success(f"✅ {msg}")
            else:
                stream_container.write(msg)
        time.sleep(0.3)

    # Step 1 — Analyze task
    update(f"Analyzing task: '{task}'", "thinking")
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": ORCHESTRATOR_PROMPT},
            {"role": "user", "content": f"Task: {task}"}
        ],
        temperature=0.2,
        max_tokens=1000
    )
    
    orchestrator_response = response.choices[0].message.content
    
    # Parse thinking
    thinking = ""
    if "THINKING:" in orchestrator_response:
        thinking = orchestrator_response.split("THINKING:")[1].split("PLAN:")[0].strip()
        update(f"Reasoning: {thinking}", "thinking")
    
    # Parse plan
    agent_tasks = []
    if "PLAN:" in orchestrator_response:
        plan_section = orchestrator_response.split("PLAN:")[1].split("EXECUTING:")[0].strip()
        for line in plan_section.split("\n"):
            line = line.strip().lstrip("- ")
            if ":" in line:
                parts = line.split(":", 1)
                agent_name = parts[0].strip().lower()
                subtask = parts[1].strip()
                
                # Map to agent key
                if "hr" in agent_name:
                    agent_key = "hr"
                elif "sales" in agent_name:
                    agent_key = "sales"
                elif "finance" in agent_name:
                    agent_key = "finance"
                elif "sdr" in agent_name:
                    agent_key = "sdr"
                elif "research" in agent_name:
                    agent_key = "research"
                else:
                    agent_key = "general"
                
                agent_tasks.append((agent_key, subtask))
    
    # If no plan parsed, use general agent
    if not agent_tasks:
        agent_tasks = [("general", task)]
    
    # Step 2 — Execute subtasks
    results = {}
    for agent_key, subtask in agent_tasks:
        update(f"Routing to {agent_key.upper()} Agent: {subtask[:60]}...", "routing")
        try:
            result = route_to_agent(subtask, agent_key)
            results[agent_key] = result
            update(f"{agent_key.upper()} Agent completed", "result")
        except Exception as e:
            results[agent_key] = f"Error: {e}"
    
    # Step 3 — Synthesize
    update("Synthesizing results from all agents...", "thinking")
    
    combined = "\n\n".join([f"[{k.upper()} Agent]\n{v}" for k, v in results.items()])
    
    final_response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are Astra, synthesizing results from multiple specialist agents into one clear, executive-ready response. Be concise and structured."},
            {"role": "user", "content": f"Original task: {task}\n\nAgent results:\n{combined}\n\nProvide a unified, actionable response."}
        ],
        temperature=0.2,
        max_tokens=1200
    )
    
    final = final_response.choices[0].message.content
    update("Final response ready!", "result")
    
    return {
        "thinking": thinking,
        "plan": agent_tasks,
        "agent_results": results,
        "final": final,
        "steps": steps
    }