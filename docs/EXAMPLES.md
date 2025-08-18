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

## Advanced Features & Examples

### Standalone SDK Usage

For generating quickstarts for pure SDK usage (no framework integration):

```bash
$ quickstart-prompt-generator init

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

## 💡 Pro Tips

### Same-Source References
When providing multiple references from the same source (e.g., all Auth0 docs), always choose **"blend"**:
- Extract consistent brand voice and style patterns
- Learn from different approaches within the same ecosystem  
- Combine structural variations (backend vs web vs SPA patterns)
- Maintain consistent terminology and tone

### Team Workflow
```bash
# Team lead creates base session
$ quickstart-prompt-generator init
$ quickstart-prompt-generator status > team-session.txt

# Team members can restore session data by copying .qpg_session.json
$ quickstart-prompt-generator generate
```

### Multi-Framework Comparison
```bash
# Generate for React
$ quickstart-prompt-generator init
# ... set up for React/Next.js
$ quickstart-prompt-generator generate -f markdown -o react-prompts.md

# Reset and generate for Vue
$ quickstart-prompt-generator reset
$ quickstart-prompt-generator init  
# ... set up for Vue/Nuxt
$ quickstart-prompt-generator generate -f markdown -o vue-prompts.md
```

## Real-World Impact

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
