import click
import requests 
from typing import Optional 
from rich import print as rprint 
from rich.console import Console 
from rich.theme import Theme 

custom_theme = Theme({
    "success": "green",
    "error": "red",
    "info": "cyan"
})

console = Console(theme=custom_theme)   # Style!

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
    """
    try:

        payload = {
            "model": model,   # Which AI we're talking to
            "prompt": prompt   # What we're asking it
        }
        

        console.print("[info]Sending data through the NET...[/info]")
        response = requests.post(api_url, json=payload)
        response.raise_for_status()   
        

        result = response.json()
        console.print(
            f"[success]NET Response: {result.get('response', 'No data came back')}[/success]"
        )
        
    except requests.exceptions.RequestException as e:
        console.print(f"[error]Connection flatlined: {str(e)}[/error]")
    except ValueError as e:
        console.print(f"[error]Data corruption detected: {str(e)}[/error]")

if __name__ == '__main__':
    cli()
