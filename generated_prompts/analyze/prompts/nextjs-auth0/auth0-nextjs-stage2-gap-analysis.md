# Stage 2: Gap Analysis Prompt

**Instructions:** Copy this prompt + output from Stage 1 to identify improvement opportunities.

```
# Quickstart Documentation Gap Analysis

Based on the analysis of the existing nextjs-auth0 documentation, I need you to identify gaps compared to industry best practices and high-quality reference documentation.

## Current Documentation Analysis
[Paste the output from the previous documentation analysis here]

## Reference Documentation Examples

Please compare against these high-quality quickstart examples:
- https://vercel.com/guides/getting-started-with-nextjs-typescript-stripe


**Primary Style Reference**: https://vercel.com/guides/getting-started-with-nextjs-typescript-stripe



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
- Create a results file at: `generated_prompts/analyze/results/nextjs-auth0-stage2-gap-analysis-results.md`
- Structure as a comprehensive gap analysis with prioritized recommendations
- Include specific examples and actionable suggestions

**If you are in CHAT MODE without file creation:**
- Provide the complete gap analysis as copy-pastable markdown in your response
- Use proper markdown formatting with clear sections and priority ratings
- Structure it as a complete document ready for saving
```
