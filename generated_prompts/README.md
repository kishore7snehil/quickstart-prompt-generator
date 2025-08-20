# Quickstart Prompt Generator Examples

This directory contains example prompts and results demonstrating both **Generation Mode** and **Analysis Mode** workflows.

## Directory Structure

```
generated_prompts/
│
├── generation/             # New Quickstart Generation Mode
│   ├── analysis/          # Stage 1: SDK Deep Analysis prompts
│   ├── style/             # Stage 2: Style Extraction prompts
│   ├── synthesis/         # Stage 3: Synthesis & Generation prompts
│   └── results/           # Generated quickstart documentation
│
└── analysis/              # Existing Quickstart Analysis Mode
    ├── prompts/           # Analysis prompt examples
    └── results/           # Analysis reports and recommendations
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



**Note**: This structure is extensible - feel free to add more subdirectories or templates as your needs evolve.
