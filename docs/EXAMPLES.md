# Examples & Sample Generated Prompts

This document provides examples of the Quickstart Prompt Generator in action, showing the complete workflow and sample outputs for different SDK scenarios.

## Example 1: Auth0 Java SDK for Spring Boot

### Session Setup
```bash
$ quickstart-prompt-generator init

🚀 Welcome
┌─ Quickstart Prompt Generator ─────────────────────────────┐
│ Initialize your SDK quickstart prompt generation session │
└───────────────────────────────────────────────────────────┘

🔧 Which SDK/library are you using?: auth0-java
📝 What is the SDK language?: Java
🔗 SDK repository or documentation link? (optional): https://github.com/auth0/auth0-java

📚 Reference Quickstart Documents
Enter reference quickstart links or file paths (one per line).
Press Enter on empty line to finish:
  Reference: https://auth0.com/docs/quickstart/backend/java
  Reference: 

🎯 Which framework/platform is your target?: Spring Boot
```

### Generated Prompts

#### Stage 1: SDK Deep Analysis Prompt

```markdown
# SDK Deep Analysis Request

I'm working on creating quickstart documentation for developers and need your help analyzing an SDK/library to understand its core capabilities, structure, and developer workflow.

## SDK Information
- **Name**: auth0-java
- **Language**: Java
- **Repository/Documentation**: https://github.com/auth0/auth0-java

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

[... continues with detailed analysis framework ...]
```

#### Stage 2: Reference Style Extraction Prompt

```markdown
# Reference Documentation Style Analysis

I need to analyze existing quickstart documentation to extract the writing style, structure, and approach that works well for developers.

## Reference Documentation
Please analyze these reference quickstart documents:
- https://auth0.com/docs/quickstart/backend/java

## Analysis Framework

### 1. Writing Style & Tone Analysis
- **Voice & Perspective**: Is it written in first person, second person, or instructional tone?
- **Technical Level**: How technical vs. beginner-friendly is the language?

[... continues with comprehensive style analysis framework ...]
```

#### Stage 3: Synthesis Prompt

```markdown
# Quickstart Documentation Generation Request

I need you to create comprehensive quickstart documentation that combines technical SDK analysis with established documentation style patterns. This will help Spring Boot developers quickly get started with auth0-java.

## Context & Goals
- **SDK**: auth0-java (Java)
- **Target Framework**: Spring Boot
- **Goal**: Create developer-friendly quickstart documentation that follows proven patterns

[... continues with synthesis requirements ...]
```

## Example 2: React SDK for Next.js

### Session Setup
```bash
$ quickstart-prompt-generator init

🔧 Which SDK/library are you using?: @auth0/nextjs-auth0
📝 What is the SDK language?: JavaScript
🔗 SDK repository or documentation link? (optional): https://github.com/auth0/nextjs-auth0

📚 Reference Quickstart Documents
  Reference: https://auth0.com/docs/quickstart/webapp/nextjs
  Reference: https://nextjs.org/docs/getting-started
  Reference: 

🎯 Which framework/platform is your target?: Next.js 14
```

### Key Differences in Generated Prompts

The generated prompts automatically adapt to the different context:

- **Language-specific considerations**: JavaScript/TypeScript patterns vs Java patterns
- **Framework focus**: Next.js routing and API routes vs Spring Boot controllers
- **Ecosystem integration**: npm packages vs Maven dependencies
- **Development workflow**: Hot reloading vs build cycles

## Example 3: Python SDK for Django

### Session Commands
```bash
# Initialize session
quickstart-prompt-generator init

# Generate prompts to console
quickstart-prompt-generator generate

# Generate prompts to Markdown file
quickstart-prompt-generator generate --format markdown --output django-auth-prompts.md

# Check current session
quickstart-prompt-generator status

# Reset and start over
quickstart-prompt-generator reset
```

### Sample Output File Structure

When using `--format markdown --output`, you get:

```markdown
# Quickstart Prompt Generator Output

## Stage 1: SDK Deep Analysis Prompt

**Instructions:** Copy this prompt to your LLM to analyze the SDK capabilities and structure.

```
[Generated SDK analysis prompt]
```

---

## Stage 2: Reference Style Extraction Prompt

**Instructions:** Copy this prompt + your reference documents to extract writing style and structure.

```
[Generated style extraction prompt]
```

---

## Stage 3: Quickstart Synthesis Prompt

**Instructions:** Copy this prompt + outputs from stages 1 & 2 to generate your final quickstart.

```
[Generated synthesis prompt]
```
```

## Workflow Tips

### Best Practices

1. **Reference Selection**: Choose 2-3 high-quality reference quickstarts that match your target audience and complexity level
2. **Framework Specificity**: Be specific about framework versions (e.g., "Spring Boot 3.x" vs just "Spring Boot")
3. **Iterative Refinement**: Use the session persistence to refine SDK details and regenerate prompts
4. **LLM Follow-up**: Don't hesitate to ask follow-up questions to your LLM based on the generated outputs

### Common Session Patterns

#### Multi-Framework Comparison
```bash
# Generate for React
quickstart-prompt-generator init
# ... set up for React/Next.js
quickstart-prompt-generator generate -f markdown -o react-prompts.md

# Reset and generate for Vue
quickstart-prompt-generator reset
quickstart-prompt-generator init  
# ... set up for Vue/Nuxt
quickstart-prompt-generator generate -f markdown -o vue-prompts.md
```

#### Team Workflow
```bash
# Team lead creates base session
quickstart-prompt-generator init
# ... configure SDK details
quickstart-prompt-generator status > team-session.txt

# Team members can restore session data
# (Copy .qpg_session.json to share session state)
quickstart-prompt-generator generate
```

## Real-World Results

### Before: Manual Documentation Process
- ⏱️ **Time**: 4-6 hours per quickstart
- 🔄 **Consistency**: Varied across team members
- 📚 **Research**: Manual SDK exploration and style analysis
- ✍️ **Writing**: From scratch for each framework

### After: LLM-Assisted with Generated Prompts
- ⏱️ **Time**: 30-60 minutes per quickstart
- 🔄 **Consistency**: Structured prompts ensure uniform approach
- 📚 **Research**: Guided analysis with comprehensive prompts
- ✍️ **Writing**: LLM generates draft, human refines and validates

### Quality Improvements
- **Completeness**: Structured prompts ensure no critical steps are missed
- **Framework Fit**: Targeted synthesis creates framework-specific examples
- **Developer Experience**: Style extraction maintains proven UX patterns
- **Maintenance**: Easy to update templates as documentation standards evolve

## Troubleshooting Common Issues

### Issue: "Missing required information" error
```bash
❌ Missing required information: target_framework
Run quickstart-prompt-generator init first to set up your session.
```
**Solution**: Run `quickstart-prompt-generator init` to set up all required fields.

### Issue: Empty or generic prompts
**Cause**: Insufficient session data or too generic inputs
**Solution**: Provide specific SDK names, version numbers, and detailed framework targets

### Issue: Prompts don't match target audience
**Cause**: Reference documentation doesn't match intended complexity level
**Solution**: Choose reference docs that match your target developer experience level

---

*These examples demonstrate the flexibility and power of structured prompt generation across different programming languages, frameworks, and use cases.*
