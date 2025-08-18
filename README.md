# Quickstart Prompt Generator

A language-agnostic CLI tool that enables SDK and documentation teams to rapidly generate LLM prompt templates for any programming language or platform (JavaScript, Java, .NET, Python, etc.), without performing codebase introspection.

## 🎯 Purpose

The Quickstart Prompt Generator guides teams through structured prompt creation for:
1. **Deep SDK Analysis** - Understanding SDK capabilities and architecture
2. **Style Extraction** - Learning from reference quickstart documentation
3. **Final Synthesis** - Combining insights to generate tailored quickstart docs

Perfect for SDK teams working across multiple languages who need consistent, high-quality quickstart documentation generated via LLMs like ChatGPT or Claude.

## ✨ Key Features

- **Language-Agnostic**: Works with any SDK/library in any programming language
- **No Code Parsing**: Accepts SDK information as plain input - no introspection required
- **Three-Stage Workflow**: Structured approach ensures comprehensive and consistent results
- **Standalone Mode**: Generate quickstarts for pure SDK usage without framework dependencies
- **Multiple Style References**: Blend documentation styles from different sources or focus on specific companies
- **Smart Session Management**: Continue existing sessions, go back during questionnaire, and handle errors gracefully
- **Interactive CLI**: Step-by-step guidance with session persistence and undo functionality
- **Flexible Output**: Console display, Markdown, or plain text export
- **Extensible Templates**: Modular prompt templates for easy customization

## 🚀 Quick Start

### Installation

```bash
cd quickstart_prompt_generator
pip install -e .
```

### Basic Usage

1. **Initialize a session** with your SDK details:
```bash
quickstart-prompt-generator init
```

2. **Generate all prompts** for your LLM workflow:
```bash
quickstart-prompt-generator generate
```

3. **Follow the three-stage process**:
   - Copy Stage 1 prompt → Paste in LLM → Get SDK analysis
   - Copy Stage 2 prompt + reference docs → Get style guide  
   - Copy Stage 3 prompt + previous outputs → Get final quickstart

## 📋 CLI Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new prompt generation session |
| `generate` | Generate all three LLM prompts |
| `status` | Show current session information |
| `reset` | Clear current session and start over |

### Generate Command Options

```bash
quickstart-prompt-generator generate [OPTIONS]

Options:
  -f, --format [console|markdown|text]  Output format (default: console)
  -o, --output PATH                     Save to file (optional)
  --help                                Show help message
```

## 🔄 Three-Stage Workflow

### Stage 1: SDK Deep Analysis
- **Purpose**: Analyze SDK capabilities, architecture, and developer workflow
- **Input**: SDK name, language, and optional repository link
- **Output**: Comprehensive technical analysis for LLM

### Stage 2: Reference Style Extraction  
- **Purpose**: Extract writing style and structure from reference documentation
- **Input**: Links to existing quickstart documentation (supports multiple references with style blending)
- **Output**: Style guide and formatting patterns with smart style preference handling

### Stage 3: Synthesis & Generation
- **Purpose**: Combine SDK analysis with style patterns to create final quickstart
- **Input**: Results from Stages 1 & 2
- **Output**: Complete, framework-specific quickstart documentation

## 💡 Example Workflows

### Framework Integration Example

```bash
$ quickstart-prompt-generator init

Which SDK/library are you using?
> auth0-spa-js

What is the SDK language?
> JavaScript

SDK repository or documentation link? (optional)
> https://github.com/auth0/auth0-spa-js

Reference quickstart links (one per line, empty to finish):
  Reference: https://auth0.com/docs/quickstart/spa/javascript
  Reference: https://auth0.com/docs/quickstart/spa/react
  Reference: https://auth0.com/docs/quickstart/spa/angular
  Reference: 

📝 Documentation Style Preference
You provided 3 reference documents:
  1. https://auth0.com/docs/quickstart/spa/javascript
  2. https://auth0.com/docs/quickstart/spa/react
  3. https://auth0.com/docs/quickstart/spa/angular

Which documentation style would you like to primarily emulate?
Enter the number (1, 2, etc.) or 'blend' to combine all styles:
Style preference: blend

Which framework/platform is your target? (or 'standalone' for pure SDK usage)
> Svelte

# Generate prompts focused on Svelte integration
$ quickstart-prompt-generator generate --format markdown --output auth0-svelte-prompts.md
```

### Standalone Mode Example

```bash
$ quickstart-prompt-generator init

Which SDK/library are you using?
> auth0-api-python

What is the SDK language?
> Python

SDK repository or documentation link? (optional)
> https://github.com/auth0/auth0-api-python

Reference quickstart links (one per line, empty to finish):
  Reference: https://auth0.com/docs/quickstart/backend/python/interactive
  Reference: https://vercel.com/docs/functions/runtimes/python
  Reference: 

Which framework/platform is your target? (or 'standalone' for pure SDK usage)
> standalone

# Generate prompts focused on direct SDK usage
$ quickstart-prompt-generator generate --format markdown --output auth0-standalone-prompts.md
```

### Multiple Style Reference with Blending

```bash
📝 Documentation Style Preference
You provided 2 reference documents:
  1. https://auth0.com/docs/quickstart/backend/python/interactive
  2. https://vercel.com/docs/functions/runtimes/python

Which documentation style would you like to primarily emulate?
Enter the number (1, 2, etc.) or 'blend' to combine all styles:
Style preference: blend  # Combines best of both Auth0 and Vercel styles
```

### Smart Session Management

```bash
$ quickstart-prompt-generator init

⚠️  Existing session detected!

SDK: auth0-api-python
Language: Python
Target: standalone

What would you like to do?
Choose an option (continue, reset, cancel): continue

# Continue editing your existing session with all previous values preserved
# Use 'back' during questionnaire to fix any mistakes
```

For more detailed examples including standalone mode, style preferences, and advanced workflows, see **[docs/EXAMPLES.md](docs/EXAMPLES.md)**.

## 📁 Project Structure

```
quickstart_prompt_generator/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Main CLI interface
│   └── prompts.py           # Prompt template engine
├── docs/
│   ├── README.md            # This file
│   ├── EXAMPLES.md          # Sample generated prompts
│   └── PROMPT_TEMPLATES.md  # Template documentation
├── tests/
│   └── test_cli.py          # Unit tests
└── setup.py                 # Package configuration
```

## 🔧 Configuration

The tool stores session data in `.qpg_session.json` in your current directory. This allows you to:
- Resume sessions after closing the terminal
- Modify session data and regenerate prompts
- Share session configurations with team members

## 🎨 Customization

### Adding Custom Templates

```python
from src.prompts import PromptGenerator

generator = PromptGenerator()
generator.add_custom_template('my_template', 'Your custom template here')
```

### Extending for New Use Cases

The prompt templates use Jinja2 for flexibility. See `docs/PROMPT_TEMPLATES.md` for detailed template documentation and customization examples.

## 📚 Documentation

- **[Examples](docs/EXAMPLES.md)**: Sample generated prompts and workflows
- **[Template Guide](docs/PROMPT_TEMPLATES.md)**: Template structure and customization
- **[Contributing](#)**: Guidelines for extending the tool

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join the community discussions for usage questions
- **Documentation**: Check the `docs/` directory for detailed guides

---

**Built for SDK teams who want to generate consistent, high-quality quickstart documentation across any programming language or platform using the power of LLMs.**
