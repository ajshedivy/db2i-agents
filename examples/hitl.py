from agents.services.ptf.get_ptf_info import ptf_agent
from agno.utils import pprint

next(
    (tool for tool in ptf_agent.tools if tool.name == "get_ptf_currency_info"), None
).requires_confirmation = True

ptf_agent.monitoring = True
ptf_agent.print_response("Are there any PTF group updates available?", stream=True)


# Handle confirmation
if ptf_agent.is_paused:
    for tool in ptf_agent.run_response.tools_requiring_confirmation:
        # Get user confirmation
        print(f"Tool {tool.tool_name}({tool.tool_args}) requires confirmation")
        confirmed = input(f"Confirm? (y/n): ").lower() == "y"
        tool.confirmed = confirmed

response = ptf_agent.continue_run()
pprint.pprint_run_response(response)
