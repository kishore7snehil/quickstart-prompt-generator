# Stage 3: Improvement Recommendations Prompt

**Instructions:** Copy this prompt + outputs from stages 1 & 2 to get specific improvement suggestions.

```
# Quickstart Documentation Improvement Recommendations

Based on the documentation analysis and gap analysis, provide specific, actionable recommendations to improve the nextjs-auth0 quickstart documentation.

## Previous Analysis Results

### Current State Analysis
[Paste the documentation analysis results here]

### Gap Analysis Results  
[Paste the gap analysis results here]

## Improvement Synthesis Request

Generate a comprehensive improvement plan with clear, actionable recommendations:

## Improvement Framework

### 1. Critical Issues (Fix Immediately)
For the top 3-5 blocking issues:

#### Issue #[N]: [Specific Problem Title]
- **Current State**: [What exists in documentation now - quote exact text/sections]
- **Problem**: [Why current approach fails developers]
- **Root Cause**: [Underlying reason for the problem]
- **Recommended Action**: 
  - [ ] **REMOVE**: [Specific content to delete]
  - [ ] **MODIFY**: [Existing content to change - show before/after]
  - [ ] **ADD**: [New content to include - provide actual examples]
- **Success Criteria**: [How to verify fix works]
- **Effort Estimate**: [Time/complexity]

### 2. Content Enhancement Plan
For each existing section that needs improvement:

#### Section: "[Exact Heading from Documentation]"
**Location**: [Where this appears in current doc]
**Current Content Assessment**: [Quote key parts that need work]

**Enhancement Strategy**:
- **Keep**: [What's working well - be specific]
- **Fix**: [What's broken - show exact changes needed]
  - Before: `[current problematic content]`
  - After: `[improved version]`
- **Add**: [What's missing - provide complete new content]
- **Remove**: [What should be deleted entirely]

### 3. Missing Content Plan
For completely absent sections:

#### New Section: "[Proposed Heading]"
- **Placement**: [Where in document structure]
- **Purpose**: [Developer problem this solves]
- **Complete Content Draft**: [Full section content ready to use]
- **Integration Notes**: [How it connects to existing content]

### 4. Structural Improvements
**Current Document Flow**: [List current section order]
**Problems with Current Structure**: [Why current organization fails]
**Recommended New Structure**: 
1. [Section 1 - with rationale]
2. [Section 2 - with rationale] 
3. [etc.]

**Migration Instructions**:
- Move [specific content] from [current location] to [new location]
- Combine [these sections] into [new unified section]
- Split [this section] into [these separate sections]

### 5. Code Quality Improvements
**Current Code Issues**: [List all problematic code examples with locations]

For each code problem:
#### Code Issue #[N]: [Description]
- **Current Code**: [Show existing problematic code]
- **Problems**: [What's wrong - missing imports, incomplete, etc.]
- **Fixed Code**: [Complete, working replacement]
- **Context Needed**: [Additional explanation/comments to add]

### 6. Implementation Roadmap

#### Phase 1: Critical Fixes (Week 1)
**Goal**: Remove blockers preventing developer success
- [ ] Fix Issue #1: [specific action]
- [ ] Fix Issue #2: [specific action] 
- [ ] Add missing [specific content]
- **Success Metric**: Developers can complete basic setup

#### Phase 2: Content Enhancement (Weeks 2-3)
**Goal**: Improve existing content quality
- [ ] Enhance "[Section Name]" with [specific improvements]
- [ ] Add "[New Section Name]" content
- [ ] Restructure [specific sections]
- **Success Metric**: Reduced time-to-completion

#### Phase 3: Advanced Features (Month 2)
**Goal**: Production-ready guidance
- [ ] Add advanced topics
- [ ] Include troubleshooting scenarios
- [ ] Create maintenance guidelines
- **Success Metric**: Successful production deployments

### 7. Quality Assurance Checklist
**Before Publishing Improvements**:
- [ ] Every code example tested and working
- [ ] All links verified and functional
- [ ] Screenshots updated to match current UI
- [ ] Content reviewed for accuracy
- [ ] User testing completed with 3+ developers

### 8. Maintenance Strategy
**Monthly Reviews**:
- Test all code examples with latest SDK version
- Update screenshots if UI changed
- Review user feedback and support tickets

**Quarterly Updates**:
- Full content audit against current best practices
- Competitive analysis vs other quickstarts
- User journey optimization based on analytics

**CRITICAL REQUIREMENTS FOR ALL RECOMMENDATIONS**:
1. **Be Specific**: Every recommendation must include exact current content that needs changing
2. **Provide Examples**: Include actual code, text, or content to use
3. **Show Before/After**: Demonstrate exact changes needed
4. **Justify Impact**: Explain why each change improves developer success
5. **Include Ready-to-Use Content**: Provide complete sections that can be copy-pasted

**FORMAT REQUIREMENT**: Structure all recommendations so a technical writer can immediately understand:
- What to delete (quote exact current content)
- What to modify (show before → after)
- What to add (provide complete new content)
- Where to place changes (specify exact locations)

**MARKDOWN FORMATTING REQUIREMENTS**:
1. **Code Blocks**: Always specify language and use proper fencing
   ```markdown
   ```typescript
   // Your code here
   ```
   ```
2. **Headers**: Use consistent spacing (one blank line before, one after)
3. **Lists**: Use consistent bullet style and proper indentation
4. **Links**: Verify all markdown links use proper [text](url) format
5. **Tables**: Include proper header separators and alignment
6. **Bold/Italic**: Use **bold** and *italic* consistently
7. **Line Breaks**: Use proper double-line breaks between sections
8. **Escaping**: Escape special characters in code examples when needed

## Output Instructions

**If you are in AGENTIC MODE with file creation capabilities:**
- Create a results file at: `generated_prompts/analyze/results/nextjs-auth0-stage3-improvement-recommendations-results.md`
- Structure as a comprehensive improvement plan with detailed examples
- Include complete code examples, specific content, and implementation roadmap

**If you are in CHAT MODE without file creation:**
- Provide the complete improvement recommendations as copy-pastable markdown in your response
- Use proper markdown formatting with clear sections and actionable items

**FINAL MARKDOWN VALIDATION**:
Before providing your response, review and fix these common markdown issues:
- [ ] All code blocks have proper language specification
- [ ] No unescaped backticks inside code blocks
- [ ] Consistent header hierarchy (H1 → H2 → H3)
- [ ] Proper spacing around headers and sections
- [ ] All links formatted correctly [text](url)
- [ ] Lists use consistent bullet points and indentation
- [ ] Tables have proper markdown syntax with aligned columns
- [ ] No mixing of `markdown` and ```markdown``` in the same document
- [ ] Special characters properly escaped when needed
- [ ] Clean line breaks between sections (no orphaned lines)
- Include all code examples, content suggestions, and implementation details
- Structure it as a complete document ready for saving
```
