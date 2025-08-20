# Stage 1: Documentation Analysis Prompt

**Instructions:** Copy this prompt to your LLM to analyze the existing Auth0 PHP quickstart documentation.

```
# Existing Quickstart Documentation Analysis

I need your help analyzing an existing quickstart documentation to identify its strengths, weaknesses, and areas for improvement.

## Documentation to Analyze

**IMPORTANT: First, please visit and extract the complete content from this URL (including all code examples, interactive elements, and documentation text):**

https://auth0.com/docs/quickstart/webapp/nextjs/interactive

After extracting the content, analyze the documentation as requested below.


## SDK Context
- **Name**: nextjs-auth0
- **Language**: Typescript
## Focus Areas
Please pay special attention to these aspects:
- Writing Style & Tone
- Content Structure & Flow
- Code Example Quality
- Developer Guidance & UX
- Visual & Formatting Elements
- Prerequisites & Environment Setup
- Configuration & External Service Setup
- Technology Currency & Practices
- Error Prevention & Troubleshooting
- Completeness & Accuracy



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
```
