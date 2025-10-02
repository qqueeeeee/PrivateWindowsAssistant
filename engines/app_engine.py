from llama_index.core.tools import FunctionTool
from AppOpener import open as open_app

def open_application(app_name: str):
    """
    Opens the app specified in the command string.
    Example command: "open <app_name>"
    """
    try:
        open_app(app_name, match_closest=True)
        return f"Opened {app_name} successfully"
    except Exception:
        return f"Could not find an installed app named '{app_name}'."

# Wrap as a tool for the agent
app_engine = FunctionTool.from_defaults(
    fn=open_application,
    name="app_opener",
    description="Opens any application installed on your system when given a command like 'open <app_name>'"
)
