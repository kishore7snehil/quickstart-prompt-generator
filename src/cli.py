#!/usr/bin/env python3
"""Main CLI module for Quickstart Prompt Generator."""

import os
import json
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from typing import Dict, List, Optional

from .prompts import PromptGenerator

console = Console()

# Session data storage
SESSION_FILE = ".qpg_session.json"

class SessionManager:
    """Manages CLI session data."""
    
    def __init__(self):
        self.session_data = {
            "sdk_name": "",
            "sdk_language": "",
            "sdk_repository": "",
            "reference_links": [],
            "target_framework": ""
        }
        self.load_session()
    
    def load_session(self):
        """Load existing session if available."""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    self.session_data.update(json.load(f))
            except (json.JSONDecodeError, FileNotFoundError):
                pass
    
    def save_session(self):
        """Save current session data."""
        with open(SESSION_FILE, 'w') as f:
            json.dump(self.session_data, f, indent=2)
    
    def get_data(self) -> Dict:
        """Get current session data."""
        return self.session_data.copy()
    
    def update_data(self, **kwargs):
        """Update session data with new values."""
        self.session_data.update(kwargs)
        self.save_session()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Quickstart Prompt Generator - Generate LLM prompts for SDK quickstart documentation.
    
    This tool helps SDK and documentation teams create structured prompts for LLM-based
    quickstart documentation generation across any programming language or platform.
    """
    pass


@cli.command()
def init():
    """Initialize a new prompt generation session."""
    console.print(Panel.fit(
        "[bold blue]Quickstart Prompt Generator[/bold blue]\n"
        "Initialize your SDK quickstart prompt generation session",
        title="🚀 Welcome"
    ))
    
    session = SessionManager()
    
    # Collect SDK information
    sdk_name = click.prompt(
        "\n🔧 Which SDK/library are you using?",
        default=session.session_data.get("sdk_name", ""),
        show_default=bool(session.session_data.get("sdk_name"))
    )
    
    sdk_language = click.prompt(
        "📝 What is the SDK language?",
        default=session.session_data.get("sdk_language", ""),
        show_default=bool(session.session_data.get("sdk_language"))
    )
    
    sdk_repository = click.prompt(
        "🔗 SDK repository or documentation link? (optional)",
        default=session.session_data.get("sdk_repository", ""),
        show_default=bool(session.session_data.get("sdk_repository"))
    )
    
    # Get reference quickstarts
    console.print("\n📚 [bold]Reference Quickstart Documents[/bold]")
    console.print("Enter reference quickstart links or file paths (one per line).")
    console.print("Press Enter on empty line to finish:")
    
    reference_links = []
    while True:
        link = click.prompt("  Reference", default="", show_default=False)
        if not link.strip():
            break
        reference_links.append(link.strip())
    
    # If no new references provided, keep existing ones
    if not reference_links and session.session_data.get("reference_links"):
        reference_links = session.session_data["reference_links"]
    
    target_framework = click.prompt(
        "\n🎯 Which framework/platform is your target?",
        default=session.session_data.get("target_framework", ""),
        show_default=bool(session.session_data.get("target_framework"))
    )
    
    # Update session
    session.update_data(
        sdk_name=sdk_name,
        sdk_language=sdk_language,
        sdk_repository=sdk_repository,
        reference_links=reference_links,
        target_framework=target_framework
    )
    
    console.print(Panel.fit(
        f"✅ Session initialized successfully!\n"
        f"SDK: [bold]{sdk_name}[/bold] ({sdk_language})\n"
        f"References: {len(reference_links)} document(s)\n"
        f"Target: [bold]{target_framework}[/bold]\n\n"
        f"Run [bold green]quickstart-prompt-generator generate[/bold green] to create your prompts!",
        title="🎉 Ready to Generate"
    ))


@cli.command()
@click.option('--format', '-f', type=click.Choice(['console', 'markdown', 'text']), 
              default='console', help='Output format for prompts')
@click.option('--output', '-o', help='Output file path (optional)')
def generate(format: str, output: Optional[str]):
    """Generate all three LLM prompts for your quickstart documentation."""
    session = SessionManager()
    data = session.get_data()
    
    # Validate session data
    required_fields = ['sdk_name', 'sdk_language', 'target_framework']
    missing = [field for field in required_fields if not data.get(field)]
    
    if missing:
        console.print(f"❌ [red]Missing required information: {', '.join(missing)}[/red]")
        console.print("Run [bold]quickstart-prompt-generator init[/bold] first to set up your session.")
        return
    
    generator = PromptGenerator()
    
    console.print(Panel.fit(
        f"Generating prompts for [bold]{data['sdk_name']}[/bold] → [bold]{data['target_framework']}[/bold]",
        title="🔄 Generating Prompts"
    ))
    
    # Generate all three prompts
    prompts = {
        'sdk_analysis': generator.generate_sdk_analysis_prompt(data),
        'style_extraction': generator.generate_style_extraction_prompt(data),
        'synthesis': generator.generate_synthesis_prompt(data)
    }
    
    if format == 'console':
        _display_prompts_console(prompts)
    elif format in ['markdown', 'text']:
        content = _format_prompts_for_file(prompts, format)
        if output:
            Path(output).write_text(content, encoding='utf-8')
            console.print(f"✅ Prompts saved to [bold]{output}[/bold]")
        else:
            console.print(content)


@cli.command()
def status():
    """Show current session status."""
    session = SessionManager()
    data = session.get_data()
    
    if not any(data.values()):
        console.print("❌ [red]No active session found.[/red]")
        console.print("Run [bold]quickstart-prompt-generator init[/bold] to get started.")
        return
    
    console.print(Panel.fit(
        f"SDK: [bold]{data.get('sdk_name', 'Not set')}[/bold] ({data.get('sdk_language', 'Not set')})\n"
        f"Repository: {data.get('sdk_repository', 'Not provided')}\n"
        f"References: {len(data.get('reference_links', []))} document(s)\n"
        f"Target Framework: [bold]{data.get('target_framework', 'Not set')}[/bold]",
        title="📊 Current Session"
    ))


@cli.command()
def reset():
    """Reset the current session."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    console.print("✅ [green]Session reset successfully![/green]")
    console.print("Run [bold]quickstart-prompt-generator init[/bold] to start a new session.")


def _display_prompts_console(prompts: Dict[str, str]):
    """Display prompts in the console with clean, copyable formatting."""
    
    stages = [
        ('sdk_analysis', "🔍 Stage 1: SDK Deep Analysis", 
         "Copy this prompt to your LLM to analyze the SDK capabilities and structure."),
        ('style_extraction', "📝 Stage 2: Reference Style Extraction", 
         "Copy this prompt + your reference documents to extract writing style and structure."),
        ('synthesis', "🎯 Stage 3: Quickstart Synthesis", 
         "Copy this prompt + outputs from stages 1 & 2 to generate your final quickstart.")
    ]
    
    for key, title, instruction in stages:
        console.print(f"\n{title}")
        console.print(f"[dim]{instruction}[/dim]")
        
        # Display clean copyable text with clear boundaries
        console.print("\n" + "="*80)
        console.print("📋 [bold]COPY FROM HERE[/bold] ⬇️")
        console.print("="*80)
        
        # Print the raw prompt text without Rich formatting
        print(prompts[key])  # Use plain print() to avoid Rich formatting
        
        console.print("="*80)
        console.print("📋 [bold]COPY TO HERE[/bold] ⬆️")
        console.print("="*80)
        
        if key != 'synthesis':  # Don't pause after last prompt
            console.print("\n[yellow]⏸️  Paste this prompt into your LLM, then press Enter to continue...[/yellow]")
            click.pause(info="")


def _format_prompts_for_file(prompts: Dict[str, str], format_type: str) -> str:
    """Format prompts for file output."""
    if format_type == 'markdown':
        content = "# Quickstart Prompt Generator Output\n\n"
        content += "## Stage 1: SDK Deep Analysis Prompt\n\n"
        content += "**Instructions:** Copy this prompt to your LLM to analyze the SDK capabilities and structure.\n\n"
        content += f"```\n{prompts['sdk_analysis']}\n```\n\n"
        content += "---\n\n"
        content += "## Stage 2: Reference Style Extraction Prompt\n\n"
        content += "**Instructions:** Copy this prompt + your reference documents to extract writing style and structure.\n\n"
        content += f"```\n{prompts['style_extraction']}\n```\n\n"
        content += "---\n\n"
        content += "## Stage 3: Quickstart Synthesis Prompt\n\n"
        content += "**Instructions:** Copy this prompt + outputs from stages 1 & 2 to generate your final quickstart.\n\n"
        content += f"```\n{prompts['synthesis']}\n```\n\n"
    else:  # text format
        content = "QUICKSTART PROMPT GENERATOR OUTPUT\n"
        content += "=" * 50 + "\n\n"
        content += "STAGE 1: SDK DEEP ANALYSIS PROMPT\n"
        content += "Instructions: Copy this prompt to your LLM to analyze the SDK capabilities and structure.\n\n"
        content += prompts['sdk_analysis'] + "\n\n"
        content += "-" * 50 + "\n\n"
        content += "STAGE 2: REFERENCE STYLE EXTRACTION PROMPT\n"
        content += "Instructions: Copy this prompt + your reference documents to extract writing style and structure.\n\n"
        content += prompts['style_extraction'] + "\n\n"
        content += "-" * 50 + "\n\n"
        content += "STAGE 3: QUICKSTART SYNTHESIS PROMPT\n"
        content += "Instructions: Copy this prompt + outputs from stages 1 & 2 to generate your final quickstart.\n\n"
        content += prompts['synthesis'] + "\n\n"
    
    return content


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
