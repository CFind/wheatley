import click  # Our command-line interface framework - makes terminal apps smooth as chrome
import requests  # For making API calls - like sending signals through the NET
from typing import Optional  # Helps us keep our data types clean and clear
from rich import print as rprint  # Makes our terminal output pop like neon in the rain
from rich.console import Console  # More tools for making our output look preem
from rich.theme import Theme  # For customizing our colors, because style matters on the streets

# Set up our color scheme - like picking the neon for your cyberdeck
custom_theme = Theme({
    "success": "green",
    "error": "red",
    "info": "cyan"
})

console = Console(theme=custom_theme)  # Initialize our styled console

@click.group()
def cli():
    """
    Your personal NET interface - lets you jack into AI models straight from your terminal.
    Think of this as your deck's command center.
    """
    pass

@cli.command()
@click.option('--model', '-m', help='Which AI model you wanna connect to', required=True)
@click.option('--prompt', '-p', help='What you wanna ask the AI', required=True)
@click.option('--api-url', help='Where to find the AI (default: local)', 
              default='http://localhost:11434/api/generate')
def query(model: str, prompt: str, api_url: Optional[str]):
    """
    Sends your message to an AI and brings back what it says.
    Like having a conversation through the NET.
    """
    try:
        # Package up our data - like prepping a data packet for the NET
        payload = {
            "model": model,  # Which AI we're talking to
            "prompt": prompt  # What we're asking it
        }
        
        # Send it through the wires
        console.print("[info]Sending data through the NET...[/info]")
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Check if something went wrong
        
        # Unpack what we got back
        result = response.json()
        console.print(
            f"[success]NET Response: {result.get('response', 'No data came back')}[/success]"
        )
        
    except requests.exceptions.RequestException as e:
        # When the connection dies - like getting disconnected mid-run
        console.print(f"[error]Connection flatlined: {str(e)}[/error]")
    except ValueError as e:
        # When the data comes back corrupted - like hitting ICE in the NET
        console.print(f"[error]Data corruption detected: {str(e)}[/error]")

if __name__ == '__main__':
    cli()