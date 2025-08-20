"""Prompt template engine for generating LLM prompts."""

from typing import Dict, List
from jinja2 import Template


class PromptGenerator:
    """Generates structured LLM prompts for SDK quickstart documentation."""
    
    def __init__(self):
        """Initialize the prompt generator with templates."""
        self.templates = {
            # Generation mode templates
            'sdk_analysis': self._get_sdk_analysis_template(),
            'style_extraction': self._get_style_extraction_template(),
            'synthesis': self._get_synthesis_template(),
            
            # Analysis mode templates
            'doc_analysis': self._get_doc_analysis_template(),
            'improvement_gap': self._get_improvement_gap_template(),
            'improvement_synthesis': self._get_improvement_synthesis_template()
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
    
    def generate_doc_analysis_prompt(self, session_data: Dict) -> str:
        """Generate Stage 1: Documentation Analysis prompt."""
        template = Template(self.templates['doc_analysis'])
        return template.render(**session_data)
    
    def generate_improvement_gap_prompt(self, session_data: Dict) -> str:
        """Generate Stage 2: Improvement Gap Analysis prompt."""
        template = Template(self.templates['improvement_gap'])
        return template.render(**session_data)
    
    def generate_improvement_synthesis_prompt(self, session_data: Dict) -> str:
        """Generate Stage 3: Improvement Synthesis prompt."""
        template = Template(self.templates['improvement_synthesis'])
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
{% if target_framework and target_framework.lower() != 'standalone' -%}
- Are there framework-specific considerations for {{ target_framework }}?
- How does this SDK work within {{ target_framework }} applications?
{% else -%}
- What are the core standalone usage patterns for {{ sdk_language }}?
- How do developers typically structure projects using this SDK directly?
{% endif %}

### 6. Error Handling & Best Practices
- What are common error scenarios developers encounter?
- What are the recommended best practices for using this SDK?
- Are there performance or security considerations?

### 7. Dependencies & Requirements
- What are the key dependencies or system requirements?
- Are there version compatibility considerations?
- What minimum {{ sdk_language }} version is supported?

### 8. Prerequisites & Development Environment
- What system-level prerequisites are required (runtime, SDK, package manager, etc.)?
- Are there specific development tools or CLI installations needed?
- What are the exact version requirements for critical dependencies?
- Are there common environment setup issues that block developers?

### 9. Language Ecosystem & Type System Considerations
- How does this SDK integrate with the {{ sdk_language }} type system (if applicable)?
- Are there language-specific patterns, interfaces, or contracts to understand?
- What language-specific configuration or imports are required?
- Are there compilation or runtime compatibility considerations?

### 10. Current vs Deprecated Approaches
- What are the current, recommended installation and setup methods?
- Are there deprecated commands, patterns, or approaches to avoid?
- How does this SDK work with modern {{ sdk_language }} tooling and conventions?
- What {{ target_framework }}-specific integration patterns are current?

### 11. External Service & Configuration Requirements
- Does this SDK require external service setup (APIs, dashboards, accounts)?
- What configuration values need to be obtained and from where?
- What do typical configuration values look like (format and examples)?
- What are the most common configuration errors and how to prevent them?

## Output Format
Please structure your analysis clearly with headers and bullet points. Focus on information that would be valuable for creating developer quickstart documentation. Be comprehensive but practical - emphasize what developers need to know to get started successfully.

## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create a results file at: `generated_prompts/analysis/results/{{ sdk_name|lower|replace(' ', '-')|replace('_', '-') }}-sdk-analysis-results.md`
- Structure the analysis as a comprehensive markdown document with proper headers
- Include a summary section at the top with key insights

**If you are in CHAT MODE without file creation:**
- Provide the complete analysis as copy-pastable markdown in your response
- Use proper markdown formatting with headers, lists, and code blocks
- Structure it as a complete document ready for saving

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
{% if style_preference == 'blend' -%}
Please analyze these reference quickstart documents and blend the best aspects of each:
{% for link in reference_links %}
- {{ link }}
{% endfor %}

**Style Instruction**: Extract and combine the best elements from all these sources to create a hybrid approach that leverages the strengths of each documentation style.
{% elif style_preference != 'none' and style_preference in reference_links -%}
Please analyze these reference quickstart documents, with **primary focus** on emulating the style of: **{{ style_preference }}**

All reference documents:
{% for link in reference_links %}
- {{ link }}{% if link == style_preference %} ← **PRIMARY STYLE TO EMULATE**{% endif %}
{% endfor %}

**Style Instruction**: Focus primarily on matching the writing style, tone, structure, and approach of the marked primary reference. Use other references for additional context but prioritize the primary style.
{% else -%}
Please analyze these reference quickstart documents:
{% for link in reference_links %}
- {{ link }}
{% endfor %}
{% endif %}
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

### 6. Prerequisites & Environment Setup Coverage
- **Prerequisites Approach**: How thoroughly does the documentation cover system requirements and prerequisites?
- **Environment Setup Detail**: What level of detail is provided for development environment configuration?
- **Dependency Management**: How are package managers, build tools, and dependency installations handled?
- **Version Specification**: How are version requirements and compatibility issues communicated?

### 7. Configuration & External Service Setup Patterns
- **Service Configuration**: How does the documentation guide users through external service setup?
- **Credential & API Key Management**: How are configuration values and authentication setup explained?
- **Step-by-Step Guidance**: What level of detail is provided for admin dashboards or external setup?
- **Configuration Examples**: How are example values and configuration formats presented?

### 8. Technology Evolution & Current Practices
- **Command Currency**: How does the documentation ensure commands and approaches are current?
- **Framework Compatibility**: How are framework-specific patterns and file structures addressed?
- **Deprecated vs Current**: How does the documentation handle evolution of tools and practices?
- **Ecosystem Integration**: How well does the documentation integrate with current ecosystem patterns?

### 9. Error Prevention & Troubleshooting Approach
- **Problem Anticipation**: How comprehensively does the documentation address potential issues?
- **Troubleshooting Organization**: How are common problems and solutions structured?
- **Error Context**: How much background is provided to help developers understand issues?
- **Validation & Checkpoints**: How does the documentation help developers verify successful setup?

## Output Format
## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create a results file at: `generated_prompts/generation/style/{{ sdk_name|lower|replace(' ', '-')|replace('_', '-') }}-style-extraction-results.md`
- Structure the style guide as a comprehensive markdown document
- Include examples and specific recommendations

**If you are in CHAT MODE without file creation:**
- Provide a detailed style guide based on your analysis, formatted as:

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
{% if target_framework and target_framework.lower() != 'standalone' -%}
This style analysis will be used to create quickstart documentation for {{ sdk_name }} ({{ sdk_language }}) targeting {{ target_framework }} developers. The goal is to maintain consistency with established patterns while creating effective developer onboarding experiences.
{% else -%}
This style analysis will be used to create standalone quickstart documentation for {{ sdk_name }} ({{ sdk_language }}) for pure SDK usage. The goal is to maintain consistency with established patterns while creating effective developer onboarding experiences for direct SDK integration.
{% endif %}

---
**Next Steps**: I'll combine this style analysis with SDK technical details to generate a quickstart guide that matches the established documentation patterns."""
    
    def _get_synthesis_template(self) -> str:
        """Template for synthesis prompt."""
        return """# Quickstart Documentation Generation Request

{% if target_framework and target_framework.lower() != 'standalone' -%}
I need you to create comprehensive quickstart documentation that combines technical SDK analysis with established documentation style patterns. This will help {{ target_framework }} developers quickly get started with {{ sdk_name }}.

## Context & Goals
- **SDK**: {{ sdk_name }} ({{ sdk_language }})
- **Target Framework**: {{ target_framework }}
- **Goal**: Create developer-friendly quickstart documentation that follows proven patterns
{% else -%}
I need you to create comprehensive quickstart documentation that combines technical SDK analysis with established documentation style patterns. This will help developers quickly get started with {{ sdk_name }} for direct, standalone usage.

## Context & Goals
- **SDK**: {{ sdk_name }} ({{ sdk_language }})
- **Target**: Standalone SDK usage (pure {{ sdk_language }})
- **Goal**: Create developer-friendly quickstart documentation for direct SDK integration
{% endif %}

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
**IMPORTANT: Follow the exact structure and organization patterns identified in the Style Extraction analysis above.**

Use the structure pattern from the reference documentation analysis to organize your quickstart. This may vary significantly depending on the type of application (SPA, webapp, backend API, native mobile, etc.) and the specific patterns used by the reference documentation.

Ensure your quickstart matches:
- **Section flow and hierarchy** from the extracted style patterns
- **Content organization approach** identified in the reference analysis  
- **Heading styles and terminology** used in the reference documentation
- **Step progression and grouping** that matches the established patterns

Do NOT use a generic structure - adapt to the specific patterns found in the reference documentation.

## Output Format
## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create the final quickstart at: `generated_prompts/generation/results/{{ sdk_name|lower|replace(' ', '-')|replace('_', '-') }}-{{ target_framework|lower|replace(' ', '-')|replace('_', '-') }}-quickstart.md`
- Structure as a complete, publication-ready quickstart guide
- Include comprehensive examples and clear instructions

**If you are in CHAT MODE without file creation:**
- Generate the quickstart documentation in Markdown format, ready for publication. Include:
  - Clear section headers
  - Working code examples with syntax highlighting
  - Step-by-step numbered instructions where appropriate
  - Callouts for important information (tips, warnings, notes)
  - Links to relevant additional resources

## Quality Criteria
The final quickstart should:
{% if target_framework and target_framework.lower() != 'standalone' -%}
- ✅ Allow a {{ target_framework }} developer to go from zero to working implementation
{% else -%}
- ✅ Allow a {{ sdk_language }} developer to go from zero to working SDK implementation
{% endif -%}
- ✅ Match the style and approach of the reference documentation
- ✅ Include all necessary setup and configuration steps
- ✅ Provide working, copy-paste code examples
- ✅ Address common developer concerns and potential issues
- ✅ Maintain consistency with {{ sdk_name }} best practices

## Critical Quality Assurance Requirements

Before finalizing the quickstart, ensure it meets these mandatory standards:

### Prerequisites & Environment Setup (MANDATORY)
- ✅ **Complete prerequisites listed** - All system requirements, runtimes, tools, and versions specified
- ✅ **Development environment setup** - Clear instructions for setting up the development environment
- ✅ **Package/dependency management** - Correct installation methods for the target ecosystem
- ✅ **Version compatibility** - Minimum and recommended versions clearly specified

### Language & Framework Compatibility (MANDATORY)
- ✅ **Type system compatibility** - Code examples work with the language's type system (if applicable)
- ✅ **Language conventions followed** - Code follows established patterns and idioms for {{ sdk_language }}
{% if target_framework and target_framework.lower() != 'standalone' -%}
- ✅ **Framework integration verified** - Examples work with current {{ target_framework }} patterns and structure
{% else -%}
- ✅ **Standalone integration verified** - Examples work with standard {{ sdk_language }} project structure
{% endif -%}
- ✅ **Import/dependency statements complete** - All necessary imports, using statements, or includes provided

### Current Practices & Command Accuracy (MANDATORY)
- ✅ **Current commands used** - No deprecated installation, build, or setup commands
- ✅ **Modern tooling integration** - Works with current package managers, build tools, and CLI utilities
{% if target_framework and target_framework.lower() != 'standalone' -%}
- ✅ **Framework structure accuracy** - File paths and project structure match current {{ target_framework }} conventions
{% else -%}
- ✅ **Project structure accuracy** - File paths and project structure match current {{ sdk_language }} conventions
{% endif %}
- ✅ **Ecosystem best practices** - Follows current recommended approaches for the technology stack

### Configuration & External Service Setup (MANDATORY)
- ✅ **External service configuration complete** - Step-by-step setup for any required external services
- ✅ **Configuration value acquisition** - Clear guidance on obtaining API keys, domains, credentials, etc.
- ✅ **Configuration examples provided** - Sample values showing expected format and structure
- ✅ **Common configuration errors prevented** - Proactive guidance on typical setup mistakes

### Error Prevention & Developer Success (HIGH PRIORITY)
- ✅ **Common issues anticipated** - Troubleshooting covers likely problems developers will encounter
- ✅ **Validation checkpoints included** - Clear steps to verify successful setup at each stage
- ✅ **Error context provided** - Explanations help developers understand and resolve issues
- ✅ **Alternative approaches offered** - Backup methods for common failure points

**QUALITY GATE**: The quickstart should be rejected if it fails any MANDATORY requirement above.

---
**Final Goal**: Create quickstart documentation that {{ target_framework }} developers can follow to successfully integrate {{ sdk_name }} in under 30 minutes, following established documentation patterns for optimal developer experience."""
    
    def _get_doc_analysis_template(self) -> str:
        """Template for analyzing existing documentation."""
        return """# Existing Quickstart Documentation Analysis

I need your help analyzing an existing quickstart documentation to identify its strengths, weaknesses, and areas for improvement.

## Documentation to Analyze

{% if existing_doc_content.startswith('URL_TO_EXTRACT:') -%}
**DOCUMENTATION SOURCE URL:** {{ existing_doc_content.replace('URL_TO_EXTRACT: ', '') }}

**IMPORTANT INSTRUCTION:**
If you cannot directly access web content (most LLMs cannot browse the internet), please respond with:

"I cannot directly access web URLs. Please visit {{ existing_doc_content.replace('URL_TO_EXTRACT: ', '') }} and copy the complete documentation content (including all code examples, setup instructions, and text), then paste it here and ask me to analyze it again."

If you CAN access web content, please extract the complete documentation from the URL above (including all code examples, interactive elements, and documentation text), then proceed with the analysis below.
{% else -%}
```
{{ existing_doc_content }}
```
{% endif %}

## SDK Context
- **Name**: {{ sdk_name }}
- **Language**: {{ sdk_language }}
{% if improvement_focus -%}

## Focus Areas
Please pay special attention to these aspects:
{% for focus in improvement_focus -%}
- {{ focus }}
{% endfor %}
{% endif %}

## Evaluation Request

You are an expert developer-advocate and technical writer. Evaluate this quickstart documentation using the structured rubric below, comparing it against widely accepted quickstart best practices.

### Evaluation Rubric
For each criterion below, assign a score from **0** (missing/very poor) to **5** (exemplary) and justify the score with concrete observations from the document:

1. **Writing Style & Tone** – Clarity, use of active/second-person voice, personality and assumed prior knowledge. Judge against industry best practices (concise, instructive, friendly tone).

2. **Content Structure & Flow** – Presence and logical sequence of introduction, prerequisites, setup, installation, implementation, testing and next steps.

3. **Code Example Quality** – Correctness, completeness, use of modern syntax, in-code comments and clear context.

4. **Developer Guidance & UX** – Detail and clarity of installation/setup instructions, troubleshooting guidance, and helpful next steps.

5. **Visual & Formatting Elements** – Use of headings, call-outs, lists and other formatting to aid comprehension.

6. **Prerequisites & Environment Setup** – Coverage of required tools, accounts and environment configuration, including version requirements.

7. **Configuration & External Service Setup** – Completeness and clarity of API key, dashboard and configuration instructions.

8. **Technology Currency & Practices** – Use of current commands, avoidance of deprecated patterns, alignment with modern tooling and framework conventions.

9. **Error Prevention & Troubleshooting** – Anticipation of common issues, organization of troubleshooting steps and inclusion of validation checkpoints.

10. **Completeness & Accuracy** – Whether the quickstart allows a developer to go from zero to a working implementation, including all required steps and accurate integration.

### Output Format
1. Produce a structured list showing each criterion, its 0–5 score and a short justification.
2. Calculate and report the overall average score.
3. Provide a concise summary of the quickstart's key strengths and weaknesses.
4. List at least five specific, prioritized recommendations for improvement based on the lowest-scoring areas.

## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create a results file at: `generated_prompts/analyze/results/{{ sdk_name|lower|replace(' ', '-')|replace('_', '-') }}-stage1-documentation-analysis-results.md`
- Structure as a comprehensive analysis with scores, justifications, and recommendations
- Include executive summary and detailed findings

**If you are in CHAT MODE without file creation:**
- Provide the complete analysis as copy-pastable markdown in your response
- Use proper markdown formatting with clear sections, scores, and recommendations
- Structure it as a complete document ready for saving"""
    
    def _get_improvement_gap_template(self) -> str:
        """Template for gap analysis against best practices."""
        return """# Quickstart Documentation Gap Analysis

Based on the analysis of the existing {{ sdk_name }} documentation, I need you to identify gaps compared to industry best practices and high-quality reference documentation.

## Current Documentation Analysis
[Paste the output from the previous documentation analysis here]

{% if reference_links -%}
## Reference Documentation Examples

Please compare against these high-quality quickstart examples:
{% for link in reference_links -%}
- {{ link }}
{% endfor %}

{% if style_preference != 'none' and style_preference != 'blend' -%}
**Primary Style Reference**: {{ style_preference }}
{% elif style_preference == 'blend' -%}
**Style Approach**: Blend the best elements from all reference sources
{% endif %}
{% endif %}

## Gap Analysis Request

Compare the current documentation against industry best practices and identify:

### 1. Content Gaps
- **Missing Prerequisites**: What assumptions are made about developer knowledge?
- **Setup Gaps**: Are environment setup steps complete?
- **Integration Gaps**: Are framework-specific examples missing?
- **Use Case Coverage**: What common scenarios are not addressed?

### 2. Structural Gaps
- **Getting Started**: Is there a clear "Hello World" example?
- **Progressive Complexity**: Does complexity increase appropriately?
- **Reference Material**: Are there quick-reference sections?
- **Troubleshooting**: Is there a debugging/FAQ section?

### 3. Developer Experience Gaps
- **Copy-Paste Ready**: Are examples immediately runnable?
- **Error Prevention**: Are common pitfalls highlighted?
- **Success Validation**: How do users know it's working?
- **Next Steps**: Are advanced topics clearly linked?

### 4. Modern Standards Gaps
- **Authentication**: Are security best practices covered?
- **Error Handling**: Is robust error handling demonstrated?
- **Testing**: Are testing examples provided?
- **Production Readiness**: Is deployment guidance included?

### 5. Accessibility Gaps
- **Multiple Learning Styles**: Text, code, visual aids?
- **Skill Levels**: Beginner vs. experienced developer paths?
- **Platform Coverage**: Cross-platform considerations?

For each gap identified, please:
- Explain why it matters for developer success
- Rate the priority (High/Medium/Low)  
- Suggest specific content that should be added

Focus especially on gaps that would prevent developers from successfully implementing the SDK in their projects.

## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create a results file at: `generated_prompts/analyze/results/{{ sdk_name|lower|replace(' ', '-')|replace('_', '-') }}-stage2-gap-analysis-results.md`
- Structure as a comprehensive gap analysis with prioritized recommendations
- Include specific examples and actionable suggestions

**If you are in CHAT MODE without file creation:**
- Provide the complete gap analysis as copy-pastable markdown in your response
- Use proper markdown formatting with clear sections and priority ratings
- Structure it as a complete document ready for saving"""
    
    def _get_improvement_synthesis_template(self) -> str:
        """Template for generating specific improvement recommendations."""
        return """# Quickstart Documentation Improvement Recommendations

Based on the documentation analysis and gap analysis, provide specific, actionable recommendations to improve the {{ sdk_name }} quickstart documentation.

## Previous Analysis Results

### Current State Analysis
[Paste the documentation analysis results here]

### Gap Analysis Results  
[Paste the gap analysis results here]

## Improvement Synthesis Request

Generate a comprehensive improvement plan with specific recommendations:

### 1. High-Priority Fixes
Identify the top 3-5 issues that should be addressed first:
- **Issue**: [Specific problem]
- **Impact**: [Why this matters for developers]
- **Solution**: [Detailed fix with examples]
- **Effort**: [Estimated work required]

### 2. Content Improvements
For each section that needs work:

#### [Section Name]
- **Current Problem**: [What's wrong now]
- **Recommended Change**: [Specific improvement]
- **New Content**: [Actual text/code to add or replace]
- **Rationale**: [Why this change helps developers]

### 3. Structural Reorganization
If the documentation needs restructuring:
- **Current Structure**: [How it's organized now]
- **Proposed Structure**: [Better organization]
- **Migration Plan**: [How to reorganize existing content]

### 4. New Sections to Add
For missing content areas:
- **Section Title**: [Proposed heading]
- **Purpose**: [What problem this solves]
- **Content Outline**: [Key points to cover]
- **Code Examples**: [Specific examples needed]

### 5. Code Example Improvements
For better code samples:
- **Language/Framework**: {{ sdk_language }}{% if target_framework %}/{{ target_framework }}{% endif %}
- **Complete Examples**: [Full, runnable code snippets]
- **Error Handling**: [How to handle common failures]
- **Best Practices**: [Recommended implementation patterns]

### 6. Developer Experience Enhancements
- **Quick Wins**: [Easy improvements with high impact]
- **Navigation Aids**: [Table of contents, cross-references]
- **Visual Elements**: [Diagrams, screenshots, flowcharts]
- **Interactive Elements**: [Try-it-yourself sections]

### 7. Implementation Roadmap
Prioritize improvements by impact and effort:

**Phase 1 (Quick Wins - 1-2 weeks)**
- [List immediate fixes]

**Phase 2 (Major Content - 2-4 weeks)**
- [List significant additions]

**Phase 3 (Advanced Features - 1-2 months)**
- [List comprehensive enhancements]

### 8. Success Metrics
How to measure improvement effectiveness:
- **Developer Feedback**: [What to ask users]
- **Usage Analytics**: [What to track]
- **Completion Rates**: [How to measure success]

### 9. Maintenance Plan
- **Regular Reviews**: [How often to update]
- **Feedback Loops**: [How to collect ongoing input]
- **Version Updates**: [How to handle SDK changes]

Provide specific, actionable recommendations that the documentation team can implement immediately. Include actual content suggestions, not just abstract advice.

## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create a results file at: `generated_prompts/analyze/results/{{ sdk_name|lower|replace(' ', '-')|replace('_', '-') }}-stage3-improvement-recommendations-results.md`
- Structure as a comprehensive improvement plan with detailed examples
- Include complete code examples, specific content, and implementation roadmap

**If you are in CHAT MODE without file creation:**
- Provide the complete improvement recommendations as copy-pastable markdown in your response
- Use proper markdown formatting with clear sections and actionable items
- Include all code examples, content suggestions, and implementation details
- Structure it as a complete document ready for saving"""

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
