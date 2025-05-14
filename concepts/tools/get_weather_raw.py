#!/usr/bin/env python3
"""
Minimal agentic loop using:
* Ollama (local LLM)            – chat completion endpoint
* Function-calling ("tools")    – single tool: get_weather
* wttr.in                       – real weather data, no API key
"""

import json
import typing as t
from dataclasses import dataclass
import requests
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint


# Set up console for rich debugging output
console = Console()


# ─────────────────── 1.  TOOL DEFINITIONS ────────────────────
@dataclass
class Tool:
    name: str
    description: str
    schema: dict
    handler: t.Callable[[dict], str]


def weather_tool(args: dict) -> str:
    """Return current conditions from wttr.in in plain English."""
    city = args["city"]
    console.print(f"[bold cyan]🔍 Fetching weather data for:[/] [yellow]{city}[/]")

    url = f"https://wttr.in/{city}?format=j1"
    console.print(f"[dim]API Request: {url}[/dim]")

    response = requests.get(url, timeout=10)
    console.print(f"[dim]Response status: {response.status_code}[/dim]")

    data = response.json()
    cond = data["current_condition"][0]
    temp_f = cond["temp_F"]
    desc = cond["weatherDesc"][0]["value"]

    result = f"{temp_f} °F, {desc} in {city.capitalize()}"
    console.print(f"[bold green]✓ Weather result:[/] {result}")
    return result


TOOL_REGISTRY: dict[str, Tool] = {
    "get_weather": Tool(
        name="get_weather",
        description="Get the current weather for a given city name.",
        schema={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
        handler=weather_tool,
    )
}

# Pre-serialize the schema list once
TOOLS_PAYLOAD = [
    {
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description,
            "parameters": t.schema,
        },
    }
    for t in TOOL_REGISTRY.values()
]

console.print("[bold magenta]📋 Tools registered:[/]")
for tool in TOOL_REGISTRY.values():
    console.print(f"  - [bold]{tool.name}[/]: {tool.description}")


# ─────────────────── 2.  OLLAMA CHAT CALL ────────────────────
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
MODEL = "llama3.1"


def ollama_chat(messages: list[dict]) -> dict:
    """One wrapper around Ollama's /chat/completions."""
    console.print(f"\n[bold blue]🤖 Sending request to Ollama ({MODEL})...[/]")

    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS_PAYLOAD,
        "tool_choice": "auto",
        "temperature": 0,
    }

    console.print("[dim]Request payload summary:[/]")
    console.print(f"  - Messages: {len(messages)}")
    console.print(f"  - Available tools: {len(TOOLS_PAYLOAD)}")

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
        console.print("[bold green]✓ Received response from Ollama[/]")
        return resp.json()
    except requests.RequestException as e:
        console.print(f"[bold red]✗ Error calling Ollama: {str(e)}[/]")
        raise


# ─────────────────── 3.  ORCHESTRATOR LOOP ───────────────────
SYSTEM_PROMPT = """You are a helpful weather assistant.
When users ask about the weather in a location:
1. Call the get_weather function with the appropriate city name
2. Format your response in a friendly, concise way
3. Always include both the temperature and weather conditions
4. Add a relevant emoji that matches the weather condition (☀️ for sunny, 🌧️ for rain, etc.)
5. Don't explain that you're using a tool or API - just provide the weather information directly

For example: "☀️ It's 75°F and sunny in New York today. Perfect day to be outside!"
"""


def chat_with_agent(user_msg: str) -> str:
    console.print(Panel(f"[yellow]{user_msg}[/]", title="[bold]User Input[/]"))

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    iteration = 0
    while True:
        iteration += 1
        console.print(f"[bold purple]🔄 Agent iteration {iteration}[/]")

        reply = ollama_chat(messages)["choices"][0]["message"]

        # A. tool call?
        if "tool_calls" in reply and reply["tool_calls"]:
            console.print("[bold orange]🛠️  Tool calls detected![/]")

            for call in reply["tool_calls"]:
                tool_name = call["function"]["name"]
                args_str = call["function"]["arguments"]

                console.print(f"[bold]Tool:[/] [cyan]{tool_name}[/]")
                console.print(f"[bold]Arguments:[/] {args_str}")

                tool = TOOL_REGISTRY[tool_name]
                args = json.loads(args_str)

                console.print("[bold yellow]⚙️ Executing tool...[/]")
                result = tool.handler(args)

                # echo the call & its result back to the LLM
                messages.append(
                    {
                        "role": "assistant",
                        "tool_call_id": call["id"],
                        "content": None,
                        "tool_calls": [call],
                    }
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": result,
                    }
                )

                console.print(f"[dim]Added tool call and result to message history[/]")

            console.print("[bold yellow]Sending updated context back to LLM...[/]")
            continue  # let the LLM reason with the observation

        # B. no tool calls → final answer
        console.print("[bold green]✅ Final answer received![/]")
        return reply["content"]


# ─────────────────── 4.  DRIVE IT ────────────────────────────
if __name__ == "__main__":
    console.print(
        Panel.fit(
            "[bold cyan]Educational Agent Example[/]\n"
            "[yellow]This example demonstrates a simple agent loop with tool calling.[/]\n"
            "Try asking about the weather in different cities!",
            title="[bold]Weather Agent[/]",
        )
    )

    while True:
        try:
            # Fix the input prompt formatting
            user_input = input("\nAsk me: ")
            q = user_input
            result = chat_with_agent(q)
            console.print(Panel(result, title="[bold green]Final Answer[/]"))
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Exiting...[/]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")
