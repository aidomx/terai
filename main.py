"""
Terminal AI - AI Chat Assistant using Google Gemini
Author: Aidomx
Version: 1.0
"""

import os
import sys
from google import genai as google_genai
from google.genai import types as google_types
from openai import OpenAI as OpenAIClient
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich import print as rprint
import time

class AIClients:
    """Manager for both Gemini and OpenAI clients"""
    def __init__(self):
        self.gemini_client = None
        self.openai_client = None
        self.setup_clients()

    def setup_clients(self):
        """Setup both Gemini and OpenAI clients"""
        load_dotenv()

        # Setup Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                self.gemini_client = google_genai.Client(api_key=gemini_key)
                print("✅ Gemini client initialized")
            except Exception as e:
                print(f"❌ Gemini setup failed: {e}")

        # Setup OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                self.openai_client = OpenAIClient(api_key=openai_key)
                print("✅ OpenAI client initialized")
            except Exception as e:
                print(f"❌ OpenAI setup failed: {e}")

        if not self.gemini_client and not self.openai_client:
            print("❌ No AI providers configured! Please set at least one API key.")
            sys.exit(1)

def get_available_models(provider):
    """Return available models for each provider"""
    gemini_models = {
        "1": {"name": "gemini-2.0-flash", "description": "Fast & efficient"},
        "2": {"name": "gemini-1.5-flash", "description": "Balanced performance"},
        "3": {"name": "gemini-1.5-pro", "description": "Most capable"},
        "4": {"name": "gemini-2.0-flash-exp", "description": "Experimental"}
    }

    openai_models = {
        "1": {"name": "gpt-4o", "description": "Latest GPT-4 model"},
        "2": {"name": "gpt-4o-mini", "description": "Fast & cost-effective"},
        "3": {"name": "gpt-4-turbo", "description": "Previous generation"},
        "4": {"name": "gpt-3.5-turbo", "description": "Legacy model"}
    }

    if provider == "gemini":
        return gemini_models
    elif provider == "openai":
        return openai_models
    else:
        return {}

def get_available_providers(clients):
    """Return available AI providers"""
    providers = {}
    if clients.gemini_client:
        providers["1"] = "gemini"
    if clients.openai_client:
        providers["2"] = "openai"
    return providers

def print_welcome(console, clients):
    """Print welcome message with rich formatting"""
    welcome_text = Text()
    welcome_text.append("🤖 Terminal AI - Hybrid AI Assistant", style="bold cyan")

    console.print(Panel(welcome_text, style="green"))

    # Show available providers
    providers = get_available_providers(clients)
    console.print("[bold yellow]Available AI Providers:[/bold yellow]")
    for key, provider in providers.items():
        status = "✅" if provider else "❌"
        console.print(f"  {status} [cyan]{key}. {provider.upper()}[/cyan]")

    console.print("[bold yellow]=" * 50)
    console.print("[bold green]Commands:[/bold green]")
    console.print("  • [cyan]quit[/cyan] - Exit application")
    console.print("  • [cyan]clear[/cyan] - Clear conversation history")
    console.print("  • [cyan]help[/cyan] - Show this help")
    console.print("  • [cyan]model[/cyan] - Change AI model")
    console.print("  • [cyan]provider[/cyan] - Switch AI provider")
    console.print("  • [cyan]markdown on/off[/cyan] - Toggle markdown rendering")
    console.print("[bold yellow]=" * 50)
    console.print()

def print_help(console):
    """Print help message"""
    help_text = """
[bold cyan]📖 Terminal AI Help:[/bold cyan]

[bold green]Chat Commands:[/bold green]
  • Type normal messages to chat with AI
  • AI responses will be displayed in beautiful markdown format

[bold green]Special Commands:[/bold green]
  • [cyan]quit[/cyan] - Exit application
  • [cyan]clear[/cyan] - Clear conversation history
  • [cyan]help[/cyan] - Show this help
  • [cyan]model[/cyan] - Change AI model
  • [cyan]provider[/cyan] - Switch between Gemini and OpenAI
  • [cyan]markdown on[/cyan] - Enable markdown rendering (default)
  • [cyan]markdown off[/cyan] - Disable markdown (plain text)

[bold green]Supported AI Providers:[/bold green]
  • 🤖 Google Gemini - Free tier available
  • 🎯 OpenAI GPT - Powerful models

[bold green]Markdown Features:[/bold green]
  • 📝 **Bold** and *italic* text
  • 📋 Lists and numbered items
  • 🎯 Code blocks with syntax highlighting
  • 📚 Quotes and blockquotes
  • ━━━ Horizontal rules and headers
"""
    console.print(Panel(help_text, title="📖 Help", border_style="blue"))

def change_provider(console, clients, current_provider):
    """Change AI provider"""
    providers = get_available_providers(clients)

    if len(providers) <= 1:
        console.print("ℹ️ [yellow]Only one provider available[/yellow]")
        return current_provider

    console.print("\n[bold cyan]🔄 Switch AI Provider:[/bold cyan]")
    for key, provider in providers.items():
        status = " ✅" if provider == current_provider else ""
        console.print(f"  [yellow]{key}.[/yellow] {provider.upper()}{status}")

    choice = input("\n🔢 Select provider or 'cancel': ").strip()

    if choice in providers:
        new_provider = providers[choice]
        console.print(f"🔄 [green]Switched to: {new_provider.upper()}[/green]")
        return new_provider
    elif choice.lower() == 'cancel':
        console.print("❌ [yellow]Provider change cancelled[/yellow]")
        return current_provider
    else:
        console.print("❌ [red]Invalid selection![/red]")
        return current_provider

def change_model(console, current_provider, current_model):
    """Change AI model"""
    models = get_available_models(current_provider)

    if not models:
        console.print("❌ [red]No models available for current provider[/red]")
        return current_model

    console.print(f"\n[bold cyan]🤖 Available {current_provider.upper()} Models:[/bold cyan]")
    for key, model_info in models.items():
        status = " ✅" if model_info["name"] == current_model else ""
        console.print(f"  [yellow]{key}.[/yellow] {model_info['name']} - {model_info['description']}{status}")

    choice = input("\n🔢 Select model or 'cancel': ").strip()

    if choice in models:
        new_model = models[choice]["name"]
        console.print(f"🔄 [green]Model changed to: {new_model}[/green]")
        return new_model
    elif choice.lower() == 'cancel':
        console.print("❌ [yellow]Model change cancelled[/yellow]")
        return current_model
    else:
        console.print("❌ [red]Invalid selection![/red]")
        return current_model

def stream_gemini_response(client, contents, model, console, use_markdown=True):
    """Stream response from Gemini"""
    full_response = ""
    accumulated_text = ""

    try:
        chunks = client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=google_types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2000,
            )
        )

        if use_markdown:
            with Live(console=console, refresh_per_second=10) as live:
                for chunk in chunks:
                    if chunk.text:
                        full_response += chunk.text
                        accumulated_text += chunk.text
                        try:
                            md = Markdown(accumulated_text)
                            live.update(md)
                        except Exception:
                            live.update(Text(accumulated_text, style="cyan"))
                md = Markdown(full_response)
                live.update(md)
        else:
            console.print("[italic cyan]", end="")
            for chunk in chunks:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    full_response += chunk.text
            console.print("[/italic cyan]")

        return full_response

    except Exception as e:
        console.print(f"❌ [red]Gemini Error: {e}[/red]")
        return None

def stream_openai_response(client, messages, model, console, use_markdown=True):
    """Stream response from OpenAI"""
    full_response = ""
    accumulated_text = ""

    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            stream=True
        )

        if use_markdown:
            with Live(console=console, refresh_per_second=10) as live:
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        accumulated_text += content
                        try:
                            md = Markdown(accumulated_text)
                            live.update(md)
                        except Exception:
                            live.update(Text(accumulated_text, style="green"))
                md = Markdown(full_response)
                live.update(md)
        else:
            console.print("[italic green]", end="")
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            console.print("[/italic green]")

        return full_response

    except Exception as e:
        console.print(f"❌ [red]OpenAI Error: {e}[/red]")
        return None

def chat_loop(clients, console):
    """Main chat loop with dual AI support"""
    history = []
    current_provider = "gemini" if clients.gemini_client else "openai"
    current_model = "gemini-2.0-flash" if current_provider == "gemini" else "gpt-4o"
    use_markdown = True

    print_welcome(console, clients)

    while True:
        try:
            user_input = input("\n👤 You: ").strip()

            # Handle commands
            if user_input.lower() == 'quit':
                console.print("\n👋 [bold yellow]Goodbye! Thanks for using Terminal AI![/bold yellow]")
                break

            elif user_input.lower() == 'clear':
                history.clear()
                console.print("🗑️ [green]Conversation history cleared![/green]")
                continue

            elif user_input.lower() == 'help':
                print_help(console)
                continue

            elif user_input.lower() == 'model':
                current_model = change_model(console, current_provider, current_model)
                continue

            elif user_input.lower() == 'provider':
                current_provider = change_provider(console, clients, current_provider)
                # Reset to default model for new provider
                if current_provider == "gemini":
                    current_model = "gemini-2.0-flash"
                else:
                    current_model = "gpt-4o"
                continue

            elif user_input.lower() in ['markdown on', 'md on']:
                use_markdown = True
                console.print("🔤 [green]Markdown rendering enabled![/green]")
                continue

            elif user_input.lower() in ['markdown off', 'md off']:
                use_markdown = False
                console.print("🔤 [yellow]Markdown rendering disabled![/yellow]")
                continue

            elif not user_input:
                continue

            # Process AI response
            console.print(f"\n🤖 [bold blue]{current_provider.upper()}:[/bold blue]")

            full_response = ""

            try:
                if current_provider == "gemini" and clients.gemini_client:
                    contents = history + [user_input]
                    full_response = stream_gemini_response(
                        clients.gemini_client, contents, current_model, console, use_markdown
                    )

                elif current_provider == "openai" and clients.openai_client:
                    # Convert history to OpenAI format
                    messages = []
                    for i, msg in enumerate(history):
                        role = "user" if i % 2 == 0 else "assistant"
                        messages.append({"role": role, "content": msg})
                    messages.append({"role": "user", "content": user_input})

                    full_response = stream_openai_response(
                        clients.openai_client, messages, current_model, console, use_markdown
                    )
                else:
                    console.print("❌ [red]Selected provider not available![/red]")
                    continue

                if full_response is None:
                    console.print("🔄 [yellow]Please try again...[/yellow]")
                    continue

            except Exception as e:
                console.print(f"\n❌ [red]API Error: {e}[/red]")
                console.print("🔄 [yellow]Please try again...[/yellow]")
                continue

            # Update history
            history.append(user_input)
            history.append(full_response)
            history = history[-20:]  # Keep last 10 exchanges

            console.print()  # Empty line for spacing

        except KeyboardInterrupt:
            console.print("\n\n👋 [bold yellow]Interrupted by user. Goodbye![/bold yellow]")
            break
        except Exception as e:
            console.print(f"\n❌ [red]Error: {e}[/red]")
            console.print("🔄 [yellow]Please try again...[/yellow]")

def main():
    """Main function"""
    try:
        # Initialize rich console
        console = Console()

        console.print("[bold green]🚀 Starting Terminal AI with Dual AI Support...[/bold green]")

        # Setup clients
        clients = AIClients()

        # Start chat
        chat_loop(clients, console)

    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
