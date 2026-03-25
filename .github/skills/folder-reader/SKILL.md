---
name: folder-reader
description: Fetch all files from folder
---

# When to use
Use this skill when the user asks for:
- list of files in folder
- scan folder in an specific path
- get all files in folder
- get all files in folder and subfolders
- get specific file in folder
- get specific file in folder and subfolders

# Steps
1. Run the appropriate script:
   - PowerShell: `powershell .\scripts\get_files.ps1 -path <folder_path>`
