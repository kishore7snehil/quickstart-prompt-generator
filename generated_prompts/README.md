# Quickstart Prompt Generator Examples

This directory contains example prompts generated using the Quickstart Prompt Generator tool along with template files for storing results from LLMs (Large Language Models).

## Directory Structure

```
generated_prompts/
│
├── analysis/               # Stage 1: SDK Deep Analysis prompts
│   └── auth0-java-analysis.md
│
├── style/                  # Stage 2: Style Extraction prompts
│   └── auth0-java-style-extraction.md
│
├── synthesis/              # Stage 3: Synthesis & Generation prompts
│   └── auth0-java-spring-boot-synthesis.md
│
└── results/                # Template files for storing LLM responses
    ├── auth0-java-analysis-results.md
    ├── auth0-java-style-extraction-results.md
    └── auth0-java-spring-boot-quickstart.md
```

## How to Use This Structure

### 1. Start with Analysis Prompts

1. Navigate to `analysis/` and select the appropriate prompt for your SDK
2. Copy the prompt and paste it into your LLM interface (ChatGPT, Claude, etc.)
3. Save the LLM's response in the corresponding file in the `results/` directory

### 2. Move to Style Extraction

1. Navigate to `style/` and select the appropriate style prompt
2. Copy the prompt and paste it into your LLM, along with reference documentation links
3. Save the LLM's style guide in the corresponding results file

### 3. Complete with Synthesis

1. Navigate to `synthesis/` and select the appropriate synthesis prompt
2. Copy the prompt and paste it into your LLM
3. Paste the results from steps 1 and 2 in the indicated sections of the prompt
4. Save the final quickstart documentation in the corresponding results file

### 4. Adding Your Own Examples

To add new examples for different SDKs or frameworks:

1. Duplicate the example files and rename them for your SDK/framework
2. Modify the SDK information, language, and target framework details
3. Update the reference links to point to relevant documentation
4. Create corresponding result template files in the `results/` directory

## Tips for Best Results

- **Be specific**: Provide detailed SDK information and specific reference documentation links
- **Review outputs**: Check each stage's output before proceeding to the next stage
- **Iterate if needed**: If results aren't satisfactory, refine your prompts and try again
- **Track insights**: Use the notes sections in the result templates to record key insights

## Github Integration

This folder structure is designed to be Github-friendly, allowing you to:

1. Share prompts with teammates or the community
2. Track changes to prompts and results over time
3. Collaborate on improving prompt effectiveness
4. Maintain a library of successful quickstart documentation examples

---

**Note**: This structure is extensible - feel free to add more subdirectories or templates as your needs evolve.
