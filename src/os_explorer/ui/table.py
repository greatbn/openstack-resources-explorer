from rich.table import Table
from rich.console import Console
from typing import Dict, Any, List

def render_table(graph_json: Dict[str, Any], resource_type: str) -> None:
    console = Console()
    nodes = [n for n in graph_json.get('nodes', []) if n['type'] == resource_type]
    
    if not nodes:
        console.print(f"No resources of type '{resource_type}' found.")
        return

    table = Table(title=f"{resource_type.capitalize()} List")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Status", style="magenta") # Assuming status in meta

    for node in nodes:
        status = node['meta'].get('status', 'UNKNOWN')
        table.add_row(node['id'], node['name'], str(status))

    console.print(table)
