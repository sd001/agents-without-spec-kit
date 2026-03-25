param (
    [string]$path = "."
)

Write-Output "using skill to read files/folder details from : ${path}"

Get-ChildItem -Recurse $path | Select-Object FullName