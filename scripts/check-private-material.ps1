# Fail if private evaluation material is in a working tree (CLAUDE.md hard rule 1, ADR-011@v1 C7).
# Matches names anywhere in the tree, subject/ included, and remote URLs in git files.
# Reads only names and git metadata inside the tree. Usage: check-private-material.ps1 [-Root <path>]
param([string]$Root = (git rev-parse --show-toplevel).Trim())
$ErrorActionPreference = 'Stop'

$pattern = 'private-eval|architect-in-the-loop-evaluator'   # -match ignores case
$items = Get-ChildItem -LiteralPath $Root -Recurse -Force -ErrorAction SilentlyContinue

# Any file or folder whose name matches.
$found = @($items | Where-Object { $_.Name -match $pattern } | ForEach-Object FullName)

# A clone or submodule under another name still records its remote URL.
$gitFiles = $items | Where-Object {
    -not $_.PSIsContainer -and (
        $_.Name -eq '.gitmodules' -or $_.Name -eq '.git' -or
        ($_.Name -eq 'config' -and $_.FullName -match '[\\/]\.git([\\/]modules[\\/].+)?[\\/]config$'))
}
$found += @($gitFiles | Where-Object { Select-String -LiteralPath $_.FullName -Pattern $pattern -Quiet } | ForEach-Object FullName)

if ($found.Count -gt 0) {
    [Console]::Error.WriteLine("ERROR: found private evaluation material in this working tree. Remove it:")
    $found | ForEach-Object { [Console]::Error.WriteLine($_) }
    exit 1
}
Write-Host 'none found'
