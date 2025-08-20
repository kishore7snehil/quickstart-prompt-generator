# Examples & Usage Guide

This document provides comprehensive examples of the Quickstart Prompt Generator in action, including real generated outputs and advanced features.

## Complete Example: Auth0 SPA JS for Svelte

This example shows the complete workflow using real generated prompts from the `generated_prompts/` folder.

### Session Setup
```bash
$ quickstart-prompt-generator init

🔧 Which SDK/library are you using?: @auth0/auth0-spa-js
📝 What is the SDK language?: JavaScript  
🔗 SDK repository or documentation link? (optional): https://github.com/auth0/auth0-spa-js

📚 Reference Quickstart Documents
Enter reference quickstart links or file paths (one per line):
  Reference: https://auth0.com/docs/quickstart/spa/vanillajs
  Reference: 

🎯 Which framework/platform is your target?: Svelte

$ quickstart-prompt-generator generate
```

### Generated Prompts

The three-stage prompts generated for this session are available in the `generated_prompts/` folder:

- **Stage 1**: [`generated_prompts/analysis/auth0-spa-js-analysis.md`](../generated_prompts/analysis/auth0-spa-js-analysis.md) - SDK Deep Analysis Prompt
- **Stage 2**: [`generated_prompts/style/auth0-spa-js-style-extraction.md`](../generated_prompts/style/auth0-spa-js-style-extraction.md) - Reference Style Extraction Prompt  
- **Stage 3**: [`generated_prompts/synthesis/auth0-spa-js-svelte-synthesis.md`](../generated_prompts/synthesis/auth0-spa-js-svelte-synthesis.md) - Quickstart Synthesis Prompt

### Real Results

The `generated_prompts/results/` folder contains actual LLM outputs from using these prompts:

- [`auth0-spa-js-analysis-results.md`](../generated_prompts/results/auth0-spa-js-analysis-results.md) - Complete SDK analysis
- [`auth0-spa-js-style-extraction-results.md`](../generated_prompts/results/auth0-spa-js-style-extraction-results.md) - Style guide
- [`auth0-spa-js-svelte-quickstart.md`](../generated_prompts/results/auth0-spa-js-svelte-quickstart.md) - Final Svelte quickstart

## Analysis Mode Examples

The Analysis Mode provides detailed evaluation of existing quickstart documentation using a structured 3-stage analysis process.

### Complete Analysis Example: Auth0 Next.js Quickstart

This example shows how to analyze an existing quickstart document:

```bash
$ quickstart-prompt-generator analyze

📋 Analysis Mode Configuration

🔗 Document URL or file path to analyze: https://auth0.com/docs/quickstart/webapp/nextjs/interactive

🔧 What SDK/library does this document cover?: nextjs-auth0

📝 What is the SDK language?: TypeScript

🎯 Select focus areas for analysis (press Enter for default):
  1. Writing Style & Tone
  2. Content Structure & Flow
  3. Code Example Quality
  4. Developer Guidance & UX
  5. Visual & Formatting Elements
  6. Prerequisites & Environment Setup
  7. Configuration & External Service Setup
  8. Technology Currency & Practices
  9. Error Prevention & Troubleshooting
  10. Completeness & Accuracy
  11. All of the above (default)

Focus areas: [Enter] # Selects all focus areas

📚 Additional reference documents (optional):
Enter reference quickstart links or file paths (one per line):
  Reference:  https://vercel.com/guides/getting-started-with-nextjs-typescript-stripe
```

### Generated Analysis Prompts

The analysis mode creates three specialized prompts:

- **Stage 1**: `nextjs-auth0-stage1-documentation-analysis.md` - Comprehensive evaluation across all focus areas
- **Stage 2**: `nextjs-auth0-stage2-gap-analysis.md` - Identifies missing elements and improvement opportunities  
- **Stage 3**: `nextjs-auth0-stage3-improvement-recommendations.md` - Provides specific, actionable recommendations

### Focus Area Selection Examples

#### Selecting Specific Focus Areas

```bash
🎯 Select focus areas for analysis:
  1. Writing Style & Tone
  2. Content Structure & Flow
  3. Code Example Quality
  4. Developer Guidance & UX
  5. Visual & Formatting Elements
  6. Prerequisites & Environment Setup
  7. Configuration & External Service Setup
  8. Technology Currency & Practices
  9. Error Prevention & Troubleshooting
  10. Completeness & Accuracy
  11. All of the above

Focus areas: 3,4,6 # Focus only on Code Examples, UX, and Prerequisites
```

#### Multiple Reference Documents

```bash
📚 Additional reference documents (optional):
  Reference: https://auth0.com/docs/quickstart/webapp/react
  Reference: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
  Reference: [Enter]

References: 3 document(s) # Original + 2 additional references
```

### Analysis Results Structure

When you run the generated prompts through an LLM, you'll get structured results like:

```
generated_prompts/analysis/results/
├── nextjs-auth0-stage1-analysis-results.md     # Detailed evaluation scores
├── nextjs-auth0-stage2-gap-analysis-results.md # Gap identification
└── nextjs-auth0-stage3-improvement-recommendations-results.md # Action items
```

## Advanced Features & Examples

### Standalone SDK Usage

For generating quickstarts for pure SDK usage (no framework integration):

```bash
$ quickstart-prompt-generator init

🔧 Which SDK/library are you using?: auth0-api-python
📝 What is the SDK language?: Python
🔗 SDK repository or documentation link? (optional): https://github.com/auth0/auth0-api-python

📚 Reference Quickstart Documents
Enter reference quickstart links or file paths (one per line).
Press Enter on empty line to finish:
  Reference: https://vercel.com/docs/functions/runtimes/python
  Reference: https://auth0.com/docs/quickstart/backend/python/interactive
  Reference: 

📝 Documentation Style Preference
You provided 2 reference documents:
  1. https://vercel.com/docs/functions/runtimes/python
  2. https://auth0.com/docs/quickstart/backend/python/interactive

Which documentation style would you like to primarily emulate?
Enter the number (1, 2, etc.) or 'blend' to combine all styles:
Style preference: 2

🎯 Which framework/platform is your target? (or 'standalone' for pure SDK usage): standalone

$ quickstart-prompt-generator generate --format markdown --output stripe-standalone-prompts.md
```

### Multiple Reference Style Selection

When you provide multiple reference documents, you can choose which style to prioritize:

#### Example 1: Selecting a Primary Style

```bash
$ quickstart-prompt-generator init

🔧 Which SDK/library are you using?: openai
📝 What is the SDK language?: Python

📚 Reference Quickstart Documents:
  Reference: https://platform.openai.com/docs/quickstart
  Reference: https://docs.anthropic.com/claude/docs/quickstart
  Reference: https://auth0.com/docs/quickstart/web/react
  Reference: 

📝 Documentation Style Preference
You provided 3 reference documents:
  1. https://platform.openai.com/docs/quickstart
  2. https://docs.anthropic.com/claude/docs/quickstart  
  3. https://auth0.com/docs/quickstart/web/react

Which documentation style would you like to primarily emulate?
Enter the number (1, 2, etc.) or 'blend' to combine all styles:
> 2
```

**Result**: Stage 2 prompt will contain:
```markdown
Please analyze these reference quickstart documents, with **primary focus** on emulating the style of: **https://docs.anthropic.com/claude/docs/quickstart**

All reference documents:
- https://platform.openai.com/docs/quickstart
- https://docs.anthropic.com/claude/docs/quickstart ← **PRIMARY STYLE TO EMULATE**
- https://auth0.com/docs/quickstart/web/react

**Style Instruction**: Focus primarily on matching the writing style, tone, structure, and approach of the marked primary reference.
```

#### Example 2: Blending All Styles

```bash
# Same setup as above, but choosing "blend"
> blend
```

**Result**: Stage 2 prompt will contain:
```markdown
Please analyze these reference quickstart documents and blend the best aspects of each:
- https://platform.openai.com/docs/quickstart
- https://docs.anthropic.com/claude/docs/quickstart
- https://auth0.com/docs/quickstart/web/react

**Style Instruction**: Extract and combine the best elements from all these sources to create a hybrid approach.
```

#### Example 3: Same-Source References

```bash
📚 Reference Quickstart Documents:
  Reference: https://auth0.com/docs/quickstart/backend/java
  Reference: https://auth0.com/docs/quickstart/web/react
  Reference: https://auth0.com/docs/quickstart/spa/vanilla
  Reference: 

📝 Documentation Style Preference
You provided 3 reference documents:
  1. https://auth0.com/docs/quickstart/backend/java
  2. https://auth0.com/docs/quickstart/web/react
  3. https://auth0.com/docs/quickstart/spa/vanilla

> blend
```

**Recommended**: When all references are from the same source, choose `blend` to leverage different approaches within the same documentation ecosystem.

### Style Selection Decision Guide

| Input Choice | Generated Instruction to LLM | Best Use Case |
|--------------|----------------------------|---------------|
| **Number (e.g., "2")** | Focus primarily on the selected reference's style | Match a specific company's documentation style exactly |
| **"blend"** | Combine the best elements from all references | Leverage strengths from multiple styles OR all references from same source |
| **Single reference** | Standard analysis of the one provided reference | One excellent reference to follow |
| **No references** | Generic style analysis prompt | Provide documentation directly in LLM chat |
