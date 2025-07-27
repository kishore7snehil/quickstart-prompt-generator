# Prompt Templates Documentation

This document explains the structure, design philosophy, and customization options for the Quickstart Prompt Generator's template system.

## Template Architecture

The prompt generation system uses **Jinja2 templates** to create structured, consistent LLM prompts. Each template is designed to be:

- **Language-agnostic**: Works across any programming language or platform
- **Context-aware**: Uses session data to create targeted prompts
- **Extensible**: Easy to modify or extend for specific team needs
- **Consistent**: Maintains uniform structure across all generated prompts

## Template Variables

All templates have access to the following session variables:

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `sdk_name` | string | Name of the SDK/library | `"auth0-java"` |
| `sdk_language` | string | Programming language | `"Java"` |
| `sdk_repository` | string | Repository or docs URL (optional) | `"https://github.com/auth0/auth0-java"` |
| `reference_links` | list | List of reference documentation URLs | `["https://auth0.com/docs/quickstart/backend/java"]` |
| `target_framework` | string | Target framework or platform | `"Spring Boot"` |

## Three-Stage Template Design

### Stage 1: SDK Deep Analysis Template

**Purpose**: Generate comprehensive technical analysis of the SDK

**Template Structure**:
```jinja2
# SDK Deep Analysis Request

I'm working on creating quickstart documentation for developers and need your help analyzing an SDK/library...

## SDK Information
- **Name**: {{ sdk_name }}
- **Language**: {{ sdk_language }}
{% if sdk_repository -%}
- **Repository/Documentation**: {{ sdk_repository }}
{% endif %}

## Analysis Request
[Structured analysis framework with 7 key areas]
```

**Design Philosophy**:
- **Comprehensive Coverage**: Ensures LLM analyzes all critical SDK aspects
- **Developer-Focused**: Emphasizes practical integration and workflow patterns
- **Context-Aware**: References target framework for relevant analysis
- **Structured Output**: Requests specific format for consistent results

**Key Sections**:
1. Core Purpose & Value Proposition
2. Architecture & Core Components
3. Key Features & Capabilities
4. Authentication & Configuration
5. Common Integration Patterns
6. Error Handling & Best Practices
7. Dependencies & Requirements

### Stage 2: Reference Style Extraction Template

**Purpose**: Analyze existing documentation to extract style and structure patterns

**Template Structure**:
```jinja2
# Reference Documentation Style Analysis

I need to analyze existing quickstart documentation to extract the writing style...

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
[5 detailed analysis categories]
```

**Design Philosophy**:
- **Style Consistency**: Ensures new docs match established patterns
- **UX Preservation**: Maintains proven developer experience approaches
- **Flexible Input**: Handles both provided links and manual document pasting
- **Multi-Dimensional Analysis**: Covers writing, structure, code, and UX aspects

**Analysis Categories**:
1. Writing Style & Tone Analysis
2. Content Structure & Organization  
3. Code Example Patterns
4. Developer Guidance & UX
5. Visual & Formatting Elements

### Stage 3: Synthesis Template

**Purpose**: Combine SDK analysis with style patterns to generate final quickstart

**Template Structure**:
```jinja2
# Quickstart Documentation Generation Request

I need you to create comprehensive quickstart documentation that combines technical SDK analysis...

## Context & Goals
- **SDK**: {{ sdk_name }} ({{ sdk_language }})
- **Target Framework**: {{ target_framework }}
- **Goal**: Create developer-friendly quickstart documentation that follows proven patterns

## Inputs to Synthesize
[Placeholders for Stage 1 & 2 outputs]

## Generation Requirements
[Detailed requirements for content, technical accuracy, and structure]
```

**Design Philosophy**:
- **Synthesis Focus**: Combines technical and stylistic insights
- **Framework-Specific**: Tailors output for specific development context
- **Quality Assurance**: Includes clear success criteria
- **Production-Ready**: Generates immediately usable documentation

## Customization Guide

### Adding New Templates

```python
from src.prompts import PromptGenerator

generator = PromptGenerator()

# Add a custom template
custom_template = """
# Custom Analysis Request

Analyze {{ sdk_name }} for {{ target_framework }} focusing on:
- Performance considerations
- Security best practices
- Advanced integration patterns

## Your analysis here...
"""

generator.add_custom_template('performance_analysis', custom_template)
```

### Modifying Existing Templates

```python
# Get current template
current_template = generator.templates['sdk_analysis']

# Modify and update
modified_template = current_template.replace(
    "## Analysis Request", 
    "## Deep Technical Analysis Request"
)

generator.update_template('sdk_analysis', modified_template)
```

### Template Extension Patterns

#### Adding New Variables

1. **Update CLI data collection** in `cli.py`:
```python
# In init command
new_field = click.prompt("New field description")
session.update_data(new_field=new_field)
```

2. **Use in templates**:
```jinja2
{% if new_field -%}
- **New Field**: {{ new_field }}
{% endif %}
```

#### Framework-Specific Templates

Create specialized templates for specific frameworks:

```python
def get_react_specific_template(self):
    return """
# React SDK Analysis Request

Analyze {{ sdk_name }} specifically for React applications, focusing on:
- Hook integration patterns
- Component lifecycle considerations
- State management integration
- SSR/CSR compatibility

## React-Specific Analysis
[Framework-specific analysis sections]
"""
```

#### Multi-Language Support

Add conditional sections based on SDK language:

```jinja2
{% if sdk_language == "JavaScript" -%}
## JavaScript-Specific Considerations
- ES6+ compatibility
- TypeScript support
- Node.js vs Browser usage
{% elif sdk_language == "Python" -%}
## Python-Specific Considerations  
- Python version compatibility
- Virtual environment setup
- Async/await support
{% endif %}
```

## Template Best Practices

### Writing Effective Prompts

1. **Be Specific**: Use precise language that guides LLM toward desired outputs
2. **Provide Context**: Include enough background for accurate analysis
3. **Structure Requests**: Use headers, bullets, and formatting for clarity
4. **Set Expectations**: Clearly state desired output format and quality criteria

### Maintaining Consistency

1. **Standard Variables**: Use consistent variable names across templates
2. **Common Patterns**: Maintain similar section structures where appropriate
3. **Error Handling**: Include fallback text for optional fields
4. **Documentation**: Comment complex template logic

### Performance Optimization

1. **Template Caching**: Templates are loaded once at initialization
2. **Minimal Logic**: Keep template logic simple for fast rendering
3. **Variable Validation**: Validate inputs before template rendering

## Advanced Customization

### Conditional Content

```jinja2
{% if reference_links|length > 1 -%}
Please analyze these {{ reference_links|length }} reference documents and identify common patterns:
{% else -%}
Please analyze this reference document:
{% endif %}
```

### Loops and Iteration

```jinja2
{% for link in reference_links %}
{{ loop.index }}. {{ link }}
{% if not loop.last %} 

{% endif %}
{% endfor %}
```

### Custom Filters

```python
from jinja2 import Environment

def format_sdk_name(name):
    """Custom filter to format SDK names."""
    return name.replace('-', ' ').title()

# Add to template environment
env = Environment()
env.filters['format_sdk'] = format_sdk_name
```

### Template Inheritance

For complex customizations, use Jinja2 template inheritance:

```jinja2
{# base_analysis.j2 #}
# {{ analysis_type }} Request

## SDK Information
- **Name**: {{ sdk_name }}
- **Language**: {{ sdk_language }}

{% block analysis_sections %}
{# Override in child templates #}
{% endblock %}

{# child_template.j2 #}
{% extends "base_analysis.j2" %}

{% block analysis_sections %}
## Custom Analysis Areas
[Specific analysis requirements]
{% endblock %}
```

## Testing Templates

### Manual Testing

```python
from src.prompts import PromptGenerator

generator = PromptGenerator()
test_data = {
    'sdk_name': 'test-sdk',
    'sdk_language': 'Python',
    'target_framework': 'Django',
    'reference_links': ['https://example.com/docs']
}

# Test template rendering
result = generator.generate_sdk_analysis_prompt(test_data)
print(result)
```

### Automated Template Testing

```python
def test_template_variables():
    """Test that all templates handle missing variables gracefully."""
    generator = PromptGenerator()
    
    # Test with minimal data
    minimal_data = {'sdk_name': 'test', 'sdk_language': 'Python', 'target_framework': 'Django'}
    
    for template_name in generator.list_templates():
        method_name = f'generate_{template_name}_prompt'
        method = getattr(generator, method_name)
        result = method(minimal_data)
        assert len(result) > 0
        assert 'test' in result
```

## Troubleshooting

### Common Template Issues

1. **Variable Not Found**: Ensure variable exists in session data
2. **Conditional Logic**: Check Jinja2 syntax for conditionals
3. **Loop Issues**: Verify list variables aren't empty
4. **Formatting Problems**: Check for proper whitespace control (`-` usage)

### Debugging Templates

```python
# Enable Jinja2 debug mode
from jinja2 import Environment, DebugUndefined

env = Environment(undefined=DebugUndefined)
template = env.from_string(template_string)
result = template.render(**data)
```

---

*This template system is designed to be both powerful and accessible, enabling teams to create consistent, high-quality LLM prompts while maintaining flexibility for specific use cases and organizational needs.*
