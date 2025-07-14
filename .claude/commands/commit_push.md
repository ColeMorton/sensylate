# Commit and Push

**Command Classification**: 🛠️ **Utility Command**
**Pre-execution Required**: Optional (basic operational checks only)
**Outputs To**: Git repository

Generate a meaningful commit title, create the commit, and push to remote.

## MANDATORY: Pre-Execution Coordination

**CRITICAL**: Before performing any git operations, you MUST integrate with the Content Lifecycle Management system to ensure content authority and prevent conflicts.

### Step 1: Pre-Execution Consultation
```bash
# Pre-execution consultation step removed
```

### Step 2: Handle Consultation Results
Based on consultation response:
- **proceed**: Continue with git commit and push operations
- **coordinate_required**: Contact relevant command owners before committing their outputs
- **avoid_duplication**: Check if similar commit was recently made
- **update_existing**: Ensure proper superseding workflow was followed for content updates

### Step 3: Workspace Validation
```bash
# Workspace validation step removed
```

**Only proceed with git operations if consultation and validation are successful.**

## Steps

1. **Stage All Changes**: Add all changes to staging area using `git add -A`
2. **Analyze Changes**: Review git status and diff to understand what has changed
3. **Generate Title**: Create a concise, descriptive commit message that explains the purpose of the changes
4. **Commit**: Create the commit with the generated message
5. **Push**: Push the commit to the remote repository

## Usage

This command will:
- Automatically stage ALL changed files using `git add -A` at the beginning
- Generate an appropriate commit message based on the changes
- Create the commit with Claude Code attribution
- Push the changes to the remote repository

## MANDATORY: Post-Execution Lifecycle Management

After completing git commit and push operations, you MUST complete these lifecycle management steps:

### Step 1: Content Authority Validation
Verify that committed content follows authority patterns:
- Check that authority files are in correct `knowledge/` locations
- Validate that superseded content was properly archived
- Confirm topic registry updates are included in commit

### Step 2: Cross-Command Notification
If committing outputs from other commands, notify relevant command owners:
- architect: Implementation plans committed
- code-owner: Technical assessments committed
- product-owner: Strategic decisions committed
- business-analyst: Requirements analyses committed

### Step 3: Registry Synchronization
Ensure topic registry reflects current state after commit:
```bash
# Knowledge dashboard validation step removed
```

## Notes

- Stages ALL files in the repository using `git add -A` command
- This includes new files, modified files, and deleted files
- Includes proper attribution in commit message
- Handles pre-commit hooks if they modify files
- Be cautious as this will stage everything, including potentially sensitive files
- **Authority Integration**: Ensure all committed content follows lifecycle management patterns
