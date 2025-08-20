# Stage 1: Documentation Analysis Prompt

**Instructions:** Copy this prompt to your LLM to analyze the existing Auth0 PHP quickstart documentation.

```
# Existing Quickstart Documentation Analysis

I need your help analyzing an existing quickstart documentation to identify its strengths, weaknesses, and areas for improvement.

## Documentation to Analyze

**DOCUMENTATION SOURCE URL:** https://auth0.com/docs/quickstart/webapp/nextjs/interactive

**IMPORTANT INSTRUCTION:**
If you cannot directly access web content (most LLMs cannot browse the internet), please respond with:

"I cannot directly access web URLs. Please visit https://auth0.com/docs/quickstart/webapp/nextjs/interactive and copy the complete documentation content (including all code examples, setup instructions, and text), then paste it here and ask me to analyze it again."

If you CAN access web content, please:
1. **Extract the complete documentation content** including:
   - All section headings (H1, H2, H3, etc.) with exact text
   - All paragraph content and instructional text
   - Every code example, snippet, and command
   - All configuration examples and file contents
   - Any callouts, warnings, notes, or special formatting
   - All links and references mentioned
   - Any visual descriptions or image alt text

2. **Structure the extracted content** in markdown format preserving:
   - Original heading hierarchy
   - Code block language specifications
   - All inline code and variables
   - Original formatting and emphasis

3. **Handle Dynamic Content**: If you encounter code examples that are:
   - Referenced by file names but content not visible
   - Loaded dynamically via JavaScript
   - Behind interactive tabs or collapsible sections
   - In code editors or sandboxes that don't show source
   
   **Explicitly note these in your analysis** and create structured placeholders:
   
   ```
   ⚠️ DYNAMIC CONTENT DETECTED
   
   Some code examples could not be extracted due to dynamic loading.
   
   ACTION REQUIRED: Please visit the original documentation and fill in the missing code below:
   ```
   
   Then create a dedicated section with placeholders for each missing code example:
   
   ```
   ## Missing Code Content (Please Fill In)
   
   ### [Filename/Section Name 1]
   **Location in documentation**: [Describe where to find this]
   **Purpose**: [What this code does]
   
   ```[language]
   // TODO: Add complete code content from documentation
   // Instructions: Copy the full code example from [specific location]
   ```
   
   ### [Filename/Section Name 2]
   **Location in documentation**: [Describe where to find this]
   **Purpose**: [What this code does]
   
   ```[language]
   // TODO: Add complete code content from documentation
   // Instructions: Copy the full code example from [specific location]
   ```
   
   [Continue for each missing code example]
   ```

4. **Then proceed with the analysis below**


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

You are an expert developer-advocate and technical writer. 

**FIRST: Document Content Analysis**
Before scoring, provide a complete content inventory:

### Content Inventory
List every section found in the documentation:
1. **Section Headings**: [List all H1, H2, H3 headings exactly as they appear]
2. **Code Examples**: [Count and list all code blocks with their purposes]
3. **Configuration Elements**: [List all config files, environment variables, settings mentioned]
4. **External Dependencies**: [List all external services, tools, accounts required]
5. **Step-by-step Instructions**: [Count numbered/ordered steps provided]

**SECOND: Detailed Evaluation**
Now evaluate this quickstart documentation using the structured rubric below, comparing it against widely accepted quickstart best practices.

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

**Part 1: Content Inventory** (as specified above)

**Part 2: Scoring Analysis**
1. Produce a structured list showing each criterion, its 0–5 score and a short justification with specific examples from the content.
2. Calculate and report the overall average score.

**Part 3: Gap Analysis**
3. **Missing Elements**: What essential quickstart components are completely absent?
4. **Incomplete Sections**: What sections exist but lack sufficient detail?
5. **Content Quality Issues**: What existing content has problems?

**Part 4: Strategic Recommendations**
6. List five specific, prioritized recommendations for improvement based on the lowest-scoring areas, each with:
   - **Current State**: What exists now
   - **Problem**: Why it's insufficient
   - **Recommendation**: Specific action to take
   - **Impact**: Why this improvement matters

## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create a results file at: `generated_prompts/analyze/results/nextjs-auth0-stage1-documentation-analysis-results.md`
- Structure as a comprehensive analysis with scores, justifications, and recommendations
- Include executive summary and detailed findings

**If you are in CHAT MODE without file creation:**
- Provide the complete analysis as copy-pastable markdown in your response
- Use proper markdown formatting with clear sections, scores, and recommendations
- Structure it as a complete document ready for saving
```
