# Copilot Instructions

## Workspace Rules

1. **Do not modify anything inside the `.github` folder** unless the user specifically asks to update it.
   - This includes skills, workflows, and any configuration files
   - Treat the `.github` folder as read-only by default

2. **Always look for `/skills` first to complete the goal**
   - Check `.github/skills/` directory for available skills before implementing solutions
   - Use existing skills when they match the user's requirements
   - Skills should be invoked rather than reimplemented

## Skill Usage

When a user requests functionality:
- First, search for relevant skills in `.github/skills/`
- Read the skill's documentation (SKILL.md) to understand its capabilities
- Use the skill's scripts/tools rather than creating new implementations
- Only create new solutions if no suitable skill exists
