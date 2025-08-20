#!/usr/bin/env python3
"""Main CLI module for Quickstart Prompt Generator."""

import click
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import tempfile
import webbrowser
from urllib.parse import urlparse
import time
import shutil
import traceback
from rich.console import Console
from rich.panel import Panel

from .prompts import PromptGenerator

console = Console()

# Session data storage
SESSION_FILE = ".qpg_session.json"
ANALYSIS_SESSION_FILE = ".qpg_analysis_session.json"

class SessionManager:
    """Manages CLI session data for generation mode."""
    
    def __init__(self):
        self.session_data = {
            "sdk_name": "",
            "sdk_language": "",
            "sdk_repository": "",
            "reference_links": [],
            "target_framework": "",
            "style_preference": ""
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


class AnalysisSessionManager:
    """Manages CLI session data for analysis mode."""
    
    def __init__(self):
        self.session_data = {
            "existing_doc_path": "",
            "existing_doc_content": "",
            "input_method": "",
            "sdk_name": "",
            "sdk_language": "", 
            "improvement_focus": [],
            "reference_links": [],
            "style_preference": ""
        }
        self.load_session()
    
    def load_session(self):
        """Load existing analysis session if available."""
        if os.path.exists(ANALYSIS_SESSION_FILE):
            try:
                with open(ANALYSIS_SESSION_FILE, 'r') as f:
                    self.session_data.update(json.load(f))
            except (json.JSONDecodeError, FileNotFoundError):
                pass
    
    def save_session(self):
        """Save current analysis session data."""
        with open(ANALYSIS_SESSION_FILE, 'w') as f:
            json.dump(self.session_data, f, indent=2)
    
    def get_data(self) -> Dict:
        """Get current analysis session data."""
        return self.session_data.copy()
    
    def update_data(self, **kwargs):
        """Update analysis session data with new values."""
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
    session = SessionManager()
    
    # Check for existing session
    if os.path.exists(SESSION_FILE) and any(session.session_data.values()):
        console.print(Panel.fit(
            "[yellow]⚠️  Existing session detected![/yellow]\n\n"
            f"SDK: {session.session_data.get('sdk_name', 'Not set')}\n"
            f"Language: {session.session_data.get('sdk_language', 'Not set')}\n"
            f"Target: {session.session_data.get('target_framework', 'Not set')}\n\n"
            "What would you like to do?",
            title="🔄 Session Management"
        ))
        
        choice = click.prompt(
            "Choose an option",
            type=click.Choice(['continue', 'reset', 'cancel']),
            show_choices=True
        )
        
        if choice == 'cancel':
            console.print("❌ [yellow]Initialization cancelled.[/yellow]")
            return
        elif choice == 'reset':
            session.session_data = {
                "sdk_name": "",
                "sdk_language": "",
                "sdk_repository": "",
                "reference_links": [],
                "target_framework": "",
                "style_preference": ""
            }
            console.print("✅ [green]Session reset. Starting fresh initialization.[/green]\n")
        else:  # continue
            console.print("✅ [green]Continuing with existing session. You can modify any values.[/green]\n")
    
    console.print(Panel.fit(
        "[bold blue]Quickstart Prompt Generator[/bold blue]\n"
        "Initialize your SDK quickstart prompt generation session\n\n"
        "[dim]💡 Tip: Type 'back' to return to previous question[/dim]",
        title="🚀 Welcome"
    ))
    
    # Interactive questionnaire with back functionality
    answers = _run_interactive_questionnaire(session)
    if not answers:
        console.print("❌ [red]Initialization cancelled.[/red]")
        return
        
    # Update session
    session.update_data(**answers)
    
    console.print(Panel.fit(
        f"✅ Session initialized successfully!\n"
        f"SDK: [bold]{answers['sdk_name']}[/bold] ({answers['sdk_language']})\n"
        f"References: {len(answers['reference_links'])} document(s)\n"
        f"Target: [bold]{answers['target_framework']}[/bold]\n\n"
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
    """Reset the current generation session."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    console.print("✅ [green]Generation session reset successfully![/green]")
    console.print("Run [bold]quickstart-prompt-generator init[/bold] to start a new session.")


# =============================================================================
# ANALYSIS COMMANDS 
# =============================================================================

@cli.group()
def analyze():
    """Analyze existing quickstart documentation for improvements.
    
    This mode works in parallel to the generation workflow, allowing you to
    analyze existing documentation while maintaining separate sessions.
    """
    pass


@analyze.command('init')
def analyze_init():
    """Initialize a new analysis session for existing documentation."""
    session = AnalysisSessionManager()
    
    # Check for existing analysis session
    if os.path.exists(ANALYSIS_SESSION_FILE) and any(session.session_data.values()):
        console.print(Panel.fit(
            "[yellow]⚠️  Existing analysis session detected![/yellow]\n\n"
            f"Document: {session.session_data.get('existing_doc_path', 'Not set')}\n"
            f"SDK: {session.session_data.get('sdk_name', 'Not set')}\n"
            f"Focus: {', '.join(session.session_data.get('improvement_focus', []))}\n\n"
            "What would you like to do?",
            title="🔄 Analysis Session Management"
        ))
        
        choice = click.prompt(
            "Choose an option",
            type=click.Choice(['continue', 'reset', 'cancel']),
            show_choices=True
        )
        
        if choice == 'cancel':
            console.print("❌ [yellow]Analysis initialization cancelled.[/yellow]")
            return
        elif choice == 'reset':
            session.session_data = {
                "existing_doc_path": "",
                "existing_doc_content": "",
                "input_method": "",
                "sdk_name": "",
                "sdk_language": "", 
                "improvement_focus": [],
                "reference_links": [],
                "style_preference": ""
            }
            console.print("✅ [green]Analysis session reset. Starting fresh initialization.[/green]\n")
        else:  # continue
            console.print("✅ [green]Continuing with existing analysis session. You can modify any values.[/green]\n")
    
    console.print(Panel.fit(
        "[bold blue]Quickstart Analysis Mode[/bold blue]\n"
        "Analyze existing quickstart documentation for improvements\n\n"
        "[dim]💡 Tip: Type 'back' to return to previous question[/dim]",
        title="🔍 Analysis Setup"
    ))
    
    # Interactive analysis questionnaire
    answers = _run_analysis_questionnaire(session)
    if not answers:
        console.print("❌ [red]Analysis initialization cancelled.[/red]")
        return
        
    # Update session
    session.update_data(**answers)
    
    console.print(Panel.fit(
        f"✅ Analysis session initialized successfully!\n"
        f"Document: [bold]{answers.get('existing_doc_path', 'Content provided')}[/bold]\n"
        f"SDK: [bold]{answers['sdk_name']}[/bold] ({answers['sdk_language']})\n"
        f"Focus Areas: {', '.join(answers['improvement_focus'])}\n"
        f"References: {len(answers['reference_links'])} document(s)\n\n"
        f"Run [bold green]quickstart-prompt-generator analyze generate[/bold green] to create analysis prompts!",
        title="🎉 Ready to Analyze"
    ))


@analyze.command('generate')
@click.option('--format', '-f', type=click.Choice(['console', 'markdown', 'text']), 
              default='console', help='Output format for analysis prompts')
@click.option('--output', '-o', help='Output file path (optional)')
def analyze_generate(format: str, output: Optional[str]):
    """Generate analysis prompts for existing documentation improvement."""
    session = AnalysisSessionManager()
    data = session.get_data()
    
    # Validate session data
    required_fields = ['existing_doc_content', 'sdk_name', 'sdk_language']
    missing = [field for field in required_fields if not data.get(field)]
    
    if missing:
        console.print(f"❌ [red]Missing required information: {', '.join(missing)}[/red]")
        console.print("Run [bold]quickstart-prompt-generator analyze[/bold] first to set up your analysis session.")
        return
    
    generator = PromptGenerator()
    
    console.print(Panel.fit(
        f"Generating analysis prompts for [bold]{data.get('existing_doc_path', 'provided content')}[/bold]",
        title="🔄 Generating Analysis Prompts"
    ))
    
    # Generate analysis prompts
    prompts = {
        'doc_analysis': generator.generate_doc_analysis_prompt(data),
        'improvement_gap': generator.generate_improvement_gap_prompt(data),
        'improvement_synthesis': generator.generate_improvement_synthesis_prompt(data)
    }
    
    if format == 'console':
        _display_analysis_prompts_console(prompts)
    elif format in ['markdown', 'text']:
        content = _format_analysis_prompts_for_file(prompts, format)
        if output:
            Path(output).write_text(content, encoding='utf-8')
            console.print(f"✅ Analysis prompts saved to [bold]{output}[/bold]")
        else:
            console.print(content)


@analyze.command('status')
def analyze_status():
    """Show current analysis session status."""
    session = AnalysisSessionManager()
    data = session.get_data()
    
    if not any(data.values()):
        console.print("❌ [red]No active analysis session found.[/red]")
        console.print("Run [bold]quickstart-prompt-generator analyze[/bold] to get started.")
        return
    
    console.print(Panel.fit(
        f"Document: [bold]{data.get('existing_doc_path', 'Content provided')}[/bold]\n"
        f"SDK: [bold]{data.get('sdk_name', 'Not set')}[/bold] ({data.get('sdk_language', 'Not set')})\n"
        f"Focus Areas: {', '.join(data.get('improvement_focus', []))}\n"
        f"References: {len(data.get('reference_links', []))} document(s)",
        title="📊 Current Analysis Session"
    ))


@analyze.command('reset')
def analyze_reset():
    """Reset the current analysis session."""
    if os.path.exists(ANALYSIS_SESSION_FILE):
        os.remove(ANALYSIS_SESSION_FILE)
    console.print("✅ [green]Analysis session reset successfully![/green]")
    console.print("Run [bold]quickstart-prompt-generator analyze[/bold] to start a new analysis session.")


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


def _run_interactive_questionnaire(session: SessionManager) -> Optional[Dict]:
    """Run interactive questionnaire with back functionality."""
    questions = [
        {
            'key': 'sdk_name',
            'prompt': '\n🔧 Which SDK/library are you using?',
            'required': True
        },
        {
            'key': 'sdk_language', 
            'prompt': '📝 What is the SDK language?',
            'required': True
        },
        {
            'key': 'sdk_repository',
            'prompt': '🔗 SDK repository or documentation link? (optional)',
            'required': False
        },
        {
            'key': 'reference_links',
            'prompt': 'reference_collection',  # Special handler
            'required': False
        },
        {
            'key': 'target_framework',
            'prompt': '\n🎯 Which framework/platform is your target? (or \'standalone\' for pure SDK usage)',
            'required': True
        }
    ]
    
    answers = {}
    current_q = 0
    
    while current_q < len(questions):
        question = questions[current_q]
        key = question['key']
        
        if key == 'reference_links':
            # Special handling for reference collection
            existing_refs = session.session_data.get('reference_links', [])
            result = _collect_references_with_back(session, existing_refs)
            if result == 'back':
                current_q = max(0, current_q - 1)
                continue
            elif result == 'cancel':
                return None
            else:
                answers['reference_links'] = result['links']
                answers['style_preference'] = result['style']
                current_q += 1
                continue
        
        # Regular question handling
        default_val = session.session_data.get(key, '') if key in session.session_data else ''
        show_default = bool(default_val)
        
        try:
            answer = click.prompt(
                question['prompt'],
                default=default_val,
                show_default=show_default
            )
            
            if answer.lower() == 'back':
                if current_q > 0:
                    current_q -= 1
                    continue
                else:
                    console.print('[yellow]Already at first question![/yellow]')
                    continue
            
            if answer.lower() == 'cancel':
                return None
                
            if question['required'] and not answer.strip():
                console.print('[red]This field is required. Please provide a value.[/red]')
                continue
                
            answers[key] = answer.strip()
            current_q += 1
            
        except click.Abort:
            return None
    
    return answers


def _collect_references_with_back(session: SessionManager, existing_refs: List[str]) -> Dict:
    """Collect reference links with back functionality."""
    console.print('\n📚 [bold]Reference Quickstart Documents[/bold]')
    
    # Show existing references if any
    if existing_refs:
        console.print(f'[dim]Existing references ({len(existing_refs)}):[/dim]')
        for i, ref in enumerate(existing_refs, 1):
            console.print(f'[dim]  {i}. {ref}[/dim]')
        console.print('[dim]\nAdd more references below, or press Enter on empty line to keep existing ones:[/dim]')
    else:
        console.print('Enter reference quickstart links or file paths (one per line).')
    
    console.print('Press Enter on empty line to finish, or type \'back\' to go to previous question:')
    
    reference_links = []
    
    while True:
        try:
            link = click.prompt('  Reference', default='', show_default=False)
            
            if link.lower() == 'back':
                return 'back'
            elif link.lower() == 'cancel':
                return 'cancel'
            elif not link.strip():
                break
            else:
                reference_links.append(link.strip())
        except click.Abort:
            return 'cancel'
    
    # If no new references provided, keep existing ones
    if not reference_links and existing_refs:
        reference_links = existing_refs
    
    # Handle style preference
    style_preference = _get_style_preference(reference_links, session)
    if style_preference == 'back':
        return 'back'
    elif style_preference == 'cancel':
        return 'cancel'
    
    return {
        'links': reference_links,
        'style': style_preference
    }


def _get_style_preference(reference_links: List[str], session: SessionManager) -> str:
    """Get style preference for multiple references."""
    if len(reference_links) <= 1:
        return reference_links[0] if reference_links else 'none'
    
    console.print(f'\n📝 [bold]Documentation Style Preference[/bold]')
    console.print(f'You provided {len(reference_links)} reference documents:')
    for i, link in enumerate(reference_links, 1):
        console.print(f'  {i}. {link}')
    console.print('\nWhich documentation style would you like to primarily emulate?')
    console.print('Enter the number (1, 2, etc.) or \'blend\' to combine all styles:')
    console.print('[dim]Type \'back\' to modify reference links[/dim]')
    
    try:
        style_choice = click.prompt(
            'Style preference',
            default=session.session_data.get('style_preference', 'blend'),
            show_default=bool(session.session_data.get('style_preference'))
        )
        
        if style_choice.lower() == 'back':
            return 'back'
        elif style_choice.lower() == 'cancel':
            return 'cancel'
        elif style_choice.isdigit() and 1 <= int(style_choice) <= len(reference_links):
            return reference_links[int(style_choice) - 1]
        else:
            return 'blend'
            
    except click.Abort:
        return 'cancel'


def _run_analysis_questionnaire(session: AnalysisSessionManager) -> Optional[Dict]:
    """Run interactive analysis questionnaire with back functionality."""
    questions = [
        {
            'key': 'existing_doc_input',
            'prompt': 'document_input',  # Special handler
            'required': True
        },
        {
            'key': 'sdk_name',
            'prompt': '\n🔧 Which SDK/library does this documentation cover?',
            'required': True
        },
        {
            'key': 'sdk_language', 
            'prompt': '📝 What is the SDK language?',
            'required': True
        },
        {
            'key': 'improvement_focus',
            'prompt': 'improvement_areas',  # Special handler
            'required': False
        },
        {
            'key': 'reference_links',
            'prompt': 'reference_collection',  # Special handler
            'required': False
        }
    ]
    
    answers = {}
    current_q = 0
    
    while current_q < len(questions):
        question = questions[current_q]
        key = question['key']
        
        if key == 'existing_doc_input':
            # Special handling for document input
            result = _get_existing_documentation_with_back(session)
            if result == 'back':
                current_q = max(0, current_q - 1)
                continue
            elif result == 'cancel':
                return None
            else:
                answers.update(result)
                current_q += 1
                continue
        
        if key == 'improvement_focus':
            # Special handling for improvement focus areas
            result = _get_improvement_focus_with_back(session)
            if result == 'back':
                current_q = max(0, current_q - 1)
                continue
            elif result == 'cancel':
                return None
            else:
                answers['improvement_focus'] = result
                current_q += 1
                continue
        
        if key == 'reference_links':
            # Special handling for reference collection
            existing_refs = session.session_data.get('reference_links', [])
            result = _collect_analysis_references_with_back(session, existing_refs)
            if result == 'back':
                current_q = max(0, current_q - 1)
                continue
            elif result == 'cancel':
                return None
            else:
                answers['reference_links'] = result['links']
                answers['style_preference'] = result['style']
                current_q += 1
                continue
        
        # Regular question handling
        default_val = session.session_data.get(key, '') if key in session.session_data else ''
        show_default = bool(default_val)
        
        try:
            answer = click.prompt(
                question['prompt'],
                default=default_val,
                show_default=show_default
            )
            
            if answer.lower() == 'back':
                if current_q > 0:
                    current_q -= 1
                    continue
                else:
                    console.print('[yellow]Already at first question![/yellow]')
                    continue
            
            if answer.lower() == 'cancel':
                return None
                
            if question['required'] and not answer.strip():
                console.print('[red]This field is required. Please provide a value.[/red]')
                continue
                
            answers[key] = answer.strip()
            current_q += 1
            
        except click.Abort:
            return None
    
    return answers


def _get_existing_documentation_with_back(session: AnalysisSessionManager) -> Dict:
    """Get existing documentation via file, URL, or paste with back functionality."""
    console.print('\n📋 [bold]Existing Documentation Input[/bold]')
    console.print('How would you like to provide the existing documentation?')
    
    try:
        input_method = click.prompt(
            'Input method',
            type=click.Choice(['file', 'url', 'paste']),
            default=session.session_data.get('input_method', 'file'),
            show_default=bool(session.session_data.get('input_method')),
            show_choices=True
        )
        
        if input_method.lower() == 'back':
            return 'back'
        elif input_method.lower() == 'cancel':
            return 'cancel'
            
    except click.Abort:
        return 'cancel'
    
    content = ''
    doc_path = ''
    
    if input_method == 'file':
        try:
            file_path = click.prompt(
                '📁 Path to existing documentation',
                default=session.session_data.get('existing_doc_path', ''),
                show_default=bool(session.session_data.get('existing_doc_path'))
            )
            
            if file_path.lower() == 'back':
                return 'back'
            elif file_path.lower() == 'cancel':
                return 'cancel'
                
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                doc_path = file_path
                console.print(f'✅ [green]Successfully loaded {len(content)} characters from file.[/green]')
            except FileNotFoundError:
                console.print(f'❌ [red]File not found: {file_path}[/red]')
                return 'back'  # Go back to retry
            except Exception as e:
                console.print(f'❌ [red]Error reading file: {str(e)}[/red]')
                return 'back'
                
        except click.Abort:
            return 'cancel'
    
    elif input_method == 'url':
        # Display warning about URL extraction limitations
        console.print(Panel.fit(
            "[yellow]⚠️  URL Content Extraction Warning[/yellow]\n\n"
            "• Most LLMs cannot directly browse websites\n"
            "• Dynamic JavaScript content may not be captured\n" 
            "• Code examples in interactive tabs/editors may be missed\n"
            "• You may need to manually add missing code content later\n\n"
            "[dim]The generated analysis will include placeholders for any missing content[/dim]",
            title="🌐 URL Mode Limitations"
        ))
        
        if not click.confirm("\nContinue with URL input?", default=True):
            return 'back'
        
        try:
            url = click.prompt(
                '🔗 URL to existing documentation',
                default=session.session_data.get('existing_doc_path', ''),
                show_default=bool(session.session_data.get('existing_doc_path'))
            )
            
            if url.lower() == 'back':
                return 'back'
            elif url.lower() == 'cancel':
                return 'cancel'
                
            # Store URL for LLM to process
            try:
                # Basic URL validation
                from urllib.parse import urlparse
                parsed = urlparse(url)
                if not parsed.scheme or not parsed.netloc:
                    raise ValueError("Invalid URL format")
                
                content = f"URL_TO_EXTRACT: {url}"
                doc_path = url
                console.print(f'✅ [green]URL saved. The LLM will extract content from: {url}[/green]')
            except Exception as e:
                console.print(f'❌ [red]Invalid URL: {str(e)}[/red]')
                return 'back'
                
        except click.Abort:
            return 'cancel'
    
    elif input_method == 'paste':
        console.print('📝 [bold]Paste your documentation content below:[/bold]')
        console.print('[dim]Type your content and press Ctrl+D (Unix) or Ctrl+Z (Windows) when finished:[/dim]')
        
        try:
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            content = '\n'.join(lines)
            doc_path = 'pasted_content'
            console.print(f'✅ [green]Successfully received {len(content)} characters of pasted content.[/green]')
            
        except KeyboardInterrupt:
            return 'cancel'
    
    if not content.strip():
        console.print('[red]No content was provided. Please try again.[/red]')
        return 'back'
    
    return {
        'existing_doc_content': content,
        'existing_doc_path': doc_path,
        'input_method': input_method
    }


def _get_improvement_focus_with_back(session: AnalysisSessionManager) -> List[str]:
    """Get improvement focus areas with back functionality."""
    console.print('\n🎯 [bold]Improvement Focus Areas[/bold]')
    console.print('What aspects would you like to focus on for improvement?')
    console.print('[dim]Select multiple areas by entering numbers separated by commas (e.g., 1,3,5)[/dim]')
    
    focus_options = [
        'Writing Style & Tone',
        'Content Structure & Flow',
        'Code Example Quality',
        'Developer Guidance & UX',
        'Visual & Formatting Elements',
        'Prerequisites & Environment Setup',
        'Configuration & External Service Setup',
        'Technology Currency & Practices',
        'Error Prevention & Troubleshooting',
        'Completeness & Accuracy',
        'All of the above'
    ]
    
    for i, option in enumerate(focus_options, 1):
        console.print(f'  {i}. {option}')
    
    existing_focus = session.session_data.get('improvement_focus', [])
    if existing_focus:
        console.print(f"\n[dim]Current selection: {', '.join(existing_focus)}[/dim]")
    
    try:
        selection = click.prompt(
            '\nSelect focus areas (comma-separated numbers)',
            default='11' if not existing_focus else '',
            show_default=bool(not existing_focus)
        )
        
        if selection.lower() == 'back':
            return 'back'
        elif selection.lower() == 'cancel':
            return 'cancel'
        
        # Parse selection
        try:
            selected_numbers = [int(x.strip()) for x in selection.split(',')]
            focus_areas = []
            
            for num in selected_numbers:
                if 1 <= num <= len(focus_options):
                    if num == 11:  # "All of the above"
                        focus_areas = focus_options[:-1]  # All except "All of the above"
                        break
                    else:
                        focus_areas.append(focus_options[num-1])
            
            if not focus_areas:
                console.print('[red]Invalid selection. Please try again.[/red]')
                return 'back'
                
            return focus_areas
            
        except ValueError:
            console.print('[red]Invalid format. Please enter numbers separated by commas.[/red]')
            return 'back'
            
    except click.Abort:
        return 'cancel'


def _collect_analysis_references_with_back(session: AnalysisSessionManager, existing_refs: List[str]) -> Dict:
    """Collect reference links for analysis with back functionality."""
    console.print('\n📚 [bold]Reference "Good" Quickstarts (Optional)[/bold]')
    console.print('Provide examples of well-written quickstarts for comparison.')
    
    # Show existing references if any
    if existing_refs:
        console.print(f'[dim]Existing references ({len(existing_refs)}):[/dim]')
        for i, ref in enumerate(existing_refs, 1):
            console.print(f'[dim]  {i}. {ref}[/dim]')
        console.print('[dim]\nAdd more references below, or press Enter on empty line to keep existing ones:[/dim]')
    else:
        console.print('Enter reference quickstart links or file paths (one per line).')
    
    console.print('Press Enter on empty line to finish, or type \'back\' to go to previous question:')
    
    reference_links = []
    
    while True:
        try:
            link = click.prompt('  Reference', default='', show_default=False)
            
            if link.lower() == 'back':
                return 'back'
            elif link.lower() == 'cancel':
                return 'cancel'
            elif not link.strip():
                break
            else:
                reference_links.append(link.strip())
        except click.Abort:
            return 'cancel'
    
    # If no new references provided, keep existing ones
    if not reference_links and existing_refs:
        reference_links = existing_refs
    
    # Handle style preference only if we have references
    style_preference = 'none'
    if len(reference_links) > 1:
        style_preference = _get_style_preference(reference_links, session)
        if style_preference == 'back':
            return 'back'
        elif style_preference == 'cancel':
            return 'cancel'
    elif len(reference_links) == 1:
        style_preference = reference_links[0]
    
    return {
        'links': reference_links,
        'style': style_preference
    }


def _display_analysis_prompts_console(prompts: Dict[str, str]):
    """Display analysis prompts in the console with clean, copyable formatting."""
    
    stages = [
        ('doc_analysis', "🔍 Stage 1: Documentation Analysis", 
         "Copy this prompt + your existing documentation to analyze current state."),
        ('improvement_gap', "📊 Stage 2: Gap Analysis", 
         "Copy this prompt + output from stage 1 to identify improvement opportunities."),
        ('improvement_synthesis', "🛠️ Stage 3: Improvement Recommendations", 
         "Copy this prompt + outputs from stages 1 & 2 to get specific improvement suggestions.")
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
        
        if key != 'improvement_synthesis':  # Don't pause after last prompt
            console.print("\n[yellow]⏸️  Paste this prompt into your LLM, then press Enter to continue...[/yellow]")
            click.pause(info="")


def _format_analysis_prompts_for_file(prompts: Dict[str, str], format_type: str) -> str:
    """Format analysis prompts for file output."""
    if format_type == 'markdown':
        content = "# Quickstart Analysis Prompt Generator Output\n\n"
        content += "## Stage 1: Documentation Analysis Prompt\n\n"
        content += "**Instructions:** Copy this prompt + your existing documentation to analyze current state.\n\n"
        content += f"```\n{prompts['doc_analysis']}\n```\n\n"
        content += "---\n\n"
        content += "## Stage 2: Gap Analysis Prompt\n\n"
        content += "**Instructions:** Copy this prompt + output from stage 1 to identify improvement opportunities.\n\n"
        content += f"```\n{prompts['improvement_gap']}\n```\n\n"
        content += "---\n\n"
        content += "## Stage 3: Improvement Recommendations Prompt\n\n"
        content += "**Instructions:** Copy this prompt + outputs from stages 1 & 2 to get specific improvement suggestions.\n\n"
        content += f"```\n{prompts['improvement_synthesis']}\n```\n\n"
    else:  # text format
        content = "QUICKSTART ANALYSIS PROMPT GENERATOR OUTPUT\n"
        content += "=" * 50 + "\n\n"
        content += "STAGE 1: DOCUMENTATION ANALYSIS PROMPT\n"
        content += "Instructions: Copy this prompt + your existing documentation to analyze current state.\n\n"
        content += prompts['doc_analysis'] + "\n\n"
        content += "-" * 50 + "\n\n"
        content += "STAGE 2: GAP ANALYSIS PROMPT\n"
        content += "Instructions: Copy this prompt + output from stage 1 to identify improvement opportunities.\n\n"
        content += prompts['improvement_gap'] + "\n\n"
        content += "-" * 50 + "\n\n"
        content += "STAGE 3: IMPROVEMENT RECOMMENDATIONS PROMPT\n"
        content += "Instructions: Copy this prompt + outputs from stages 1 & 2 to get specific improvement suggestions.\n\n"
        content += prompts['improvement_synthesis'] + "\n\n"
    
    return content


def main():
    """Entry point for the CLI."""
    cli()

if __name__ == "__main__":
    main()
