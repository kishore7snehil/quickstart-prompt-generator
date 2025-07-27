"""Prompt template engine for generating LLM prompts."""

from typing import Dict, List
from jinja2 import Template


class PromptGenerator:
    """Generates structured LLM prompts for SDK quickstart documentation."""
    
    def __init__(self):
        """Initialize the prompt generator with templates."""
        self.templates = {
            'sdk_analysis': self._get_sdk_analysis_template(),
            'style_extraction': self._get_style_extraction_template(),
            'synthesis': self._get_synthesis_template()
        }
    
    def generate_sdk_analysis_prompt(self, session_data: Dict) -> str:
        """Generate Stage 1: SDK Deep Analysis prompt."""
        template = Template(self.templates['sdk_analysis'])
        return template.render(**session_data)
    
    def generate_style_extraction_prompt(self, session_data: Dict) -> str:
        """Generate Stage 2: Reference Style Extraction prompt."""
        template = Template(self.templates['style_extraction'])
        return template.render(**session_data)
    
    def generate_synthesis_prompt(self, session_data: Dict) -> str:
        """Generate Stage 3: Quickstart Synthesis prompt."""
        template = Template(self.templates['synthesis'])
        return template.render(**session_data)
    
    def _get_sdk_analysis_template(self) -> str:
        """Template for SDK deep analysis prompt."""
        return """# SDK Deep Analysis Request

I'm working on creating quickstart documentation for developers and need your help analyzing an SDK/library to understand its core capabilities, structure, and developer workflow.

## SDK Information
- **Name**: {{ sdk_name }}
- **Language**: {{ sdk_language }}
{% if sdk_repository -%}
- **Repository/Documentation**: {{ sdk_repository }}
{% endif %}

## Analysis Request

Please provide a comprehensive analysis of this SDK covering the following areas:

### 1. Core Purpose & Value Proposition
- What is the primary purpose of this SDK?
- What specific problems does it solve for developers?
- What are the key value propositions for developers using this SDK?

### 2. Architecture & Core Components
- What are the main modules, classes, or components?
- How do these components interact with each other?
- What is the typical developer workflow when using this SDK?

### 3. Key Features & Capabilities
- List the most important features developers use
- What are the main use cases this SDK supports?
- Are there any advanced or specialized features worth highlighting?

### 4. Authentication & Configuration
- How do developers authenticate or configure the SDK?
- What credentials, API keys, or setup steps are typically required?
- Are there environment-specific considerations?

### 5. Common Integration Patterns
- How does this SDK typically integrate into applications?
- What are the most common initialization and setup patterns?
- Are there framework-specific considerations for {{ sdk_language }}?

### 6. Error Handling & Best Practices
- What are common error scenarios developers encounter?
- What are the recommended best practices for using this SDK?
- Are there performance or security considerations?

### 7. Dependencies & Requirements
- What are the key dependencies or system requirements?
- Are there version compatibility considerations?
- What minimum {{ sdk_language }} version is supported?

## Output Format
Please structure your analysis clearly with headers and bullet points. Focus on information that would be valuable for creating developer quickstart documentation. Be comprehensive but practical - emphasize what developers need to know to get started successfully.

---
**Next Steps**: After you provide this analysis, I'll use it along with reference documentation styles to generate a targeted quickstart guide for {{ target_framework }}."""
    
    def _get_style_extraction_template(self) -> str:
        """Template for reference style extraction prompt."""
        return """# Reference Documentation Style Analysis

I need to analyze existing quickstart documentation to extract the writing style, structure, and approach that works well for developers. This will help me maintain consistency when creating new quickstart documentation.

## Task Overview
Please analyze the following reference quickstart documentation and extract:
1. **Writing Style & Tone**
2. **Content Structure & Flow** 
3. **Code Example Patterns**
4. **Developer Guidance Approach**

## Reference Documentation
{% if reference_links -%}
Please analyze these reference quickstart documents:
{% for link in reference_links %}
- {{ link }}
{% endfor %}
{% else -%}
*No reference links provided - please analyze any quickstart documentation I provide below this prompt*
{% endif %}

## Analysis Framework

### 1. Writing Style & Tone Analysis
- **Voice & Perspective**: Is it written in first person, second person, or instructional tone?
- **Technical Level**: How technical vs. beginner-friendly is the language?
- **Personality**: Is the tone formal, casual, encouraging, or matter-of-fact?
- **Assumptions**: What level of prior knowledge does it assume from developers?

### 2. Content Structure & Organization
- **Opening Approach**: How does the documentation begin? (overview, prerequisites, direct setup?)
- **Section Flow**: What is the typical progression of topics?
- **Information Hierarchy**: How is information prioritized and organized?
- **Length & Depth**: How comprehensive vs. concise is the content?

### 3. Code Example Patterns
- **Code Style**: How are code examples formatted and presented?
- **Example Complexity**: Are examples minimal/focused or comprehensive/realistic?
- **Code Comments**: How much explanation is provided within code?
- **Multiple Languages**: If applicable, how are multi-language examples handled?

### 4. Developer Guidance & UX
- **Setup Instructions**: How detailed are installation and setup steps?
- **Troubleshooting**: How does it handle potential issues or errors?
- **Next Steps**: How does it guide developers beyond the basic example?
- **Resource Linking**: How does it reference additional documentation or resources?

### 5. Visual & Formatting Elements
- **Headers & Sections**: What heading hierarchy and section structure is used?
- **Callouts & Highlights**: Are there special formatting elements (tips, warnings, notes)?
- **Lists & Bullets**: How is information broken down into digestible pieces?

## Output Format
Please provide a detailed style guide based on your analysis, formatted as:

```markdown
# Style Guide Extract

## Writing Style
[Key characteristics of the writing approach]

## Structure Pattern
[Typical content flow and organization]

## Code Example Style
[How code is presented and explained]

## Developer Experience Focus
[How the documentation guides and supports developers]

## Formatting Conventions
[Visual and structural elements used]
```

## Context for Application
This style analysis will be used to create quickstart documentation for {{ sdk_name }} ({{ sdk_language }}) targeting {{ target_framework }} developers. The goal is to maintain consistency with established patterns while creating effective developer onboarding experiences.

---
**Next Steps**: I'll combine this style analysis with SDK technical details to generate a quickstart guide that matches the established documentation patterns."""
    
    def _get_synthesis_template(self) -> str:
        """Template for synthesis prompt."""
        return """# Quickstart Documentation Generation Request

I need you to create comprehensive quickstart documentation that combines technical SDK analysis with established documentation style patterns. This will help {{ target_framework }} developers quickly get started with {{ sdk_name }}.

## Context & Goals
- **SDK**: {{ sdk_name }} ({{ sdk_language }})
- **Target Framework**: {{ target_framework }}
- **Goal**: Create developer-friendly quickstart documentation that follows proven patterns

## Inputs to Synthesize

### 1. SDK Technical Analysis
*[Paste the complete output from Stage 1: SDK Deep Analysis here]*

### 2. Reference Style Guide
*[Paste the complete style guide from Stage 2: Reference Style Extraction here]*

## Generation Requirements

### Content Requirements
1. **Follow the extracted style patterns** - match the tone, structure, and approach from the reference analysis
2. **Framework-Specific Focus** - tailor examples and instructions specifically for {{ target_framework }}
3. **Complete Workflow** - cover setup through first successful implementation
4. **Practical Examples** - provide working code that developers can copy and run
5. **Clear Prerequisites** - specify what developers need before starting

### Technical Requirements
1. **Accurate Integration** - ensure all code examples work with {{ target_framework }}
2. **Best Practices** - incorporate SDK best practices and security considerations
3. **Error Prevention** - address common pitfalls and setup issues
4. **Scalable Foundation** - show patterns that work for real applications, not just demos

### Documentation Structure
Create a complete quickstart guide with:

1. **Introduction** - brief overview of what developers will accomplish
2. **Prerequisites** - system requirements, accounts needed, prior knowledge
3. **Installation** - step-by-step setup for {{ target_framework }} environment
4. **Configuration** - authentication, environment setup, initial configuration
5. **First Implementation** - working example with complete code
6. **Key Concepts** - essential SDK concepts developers need to understand
7. **Next Steps** - resources for expanding beyond the quickstart
8. **Troubleshooting** - common issues and solutions

## Output Format
Generate the quickstart documentation in Markdown format, ready for publication. Include:
- Clear section headers
- Working code examples with syntax highlighting
- Step-by-step numbered instructions where appropriate
- Callouts for important information (tips, warnings, notes)
- Links to relevant additional resources

## Quality Criteria
The final quickstart should:
- ✅ Allow a {{ target_framework }} developer to go from zero to working implementation
- ✅ Match the style and approach of the reference documentation
- ✅ Include all necessary setup and configuration steps
- ✅ Provide working, copy-paste code examples
- ✅ Address common developer concerns and potential issues
- ✅ Maintain consistency with {{ sdk_name }} best practices

---
**Final Goal**: Create quickstart documentation that {{ target_framework }} developers can follow to successfully integrate {{ sdk_name }} in under 30 minutes, following established documentation patterns for optimal developer experience."""

    def get_template_info(self) -> Dict[str, str]:
        """Get information about available templates."""
        return {
            'sdk_analysis': 'Analyzes SDK capabilities, architecture, and developer workflow',
            'style_extraction': 'Extracts writing style and structure from reference documentation',
            'synthesis': 'Combines SDK analysis with style patterns to generate final quickstart'
        }
    
    def add_custom_template(self, name: str, template: str):
        """Add a custom template for extensibility."""
        self.templates[name] = template
    
    def update_template(self, name: str, template: str):
        """Update an existing template."""
        if name in self.templates:
            self.templates[name] = template
        else:
            raise KeyError(f"Template '{name}' not found")
    
    def list_templates(self) -> List[str]:
        """List all available template names."""
        return list(self.templates.keys())
