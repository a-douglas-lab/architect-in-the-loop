# Prepare a clone or worktree: fetch the pinned subject system and check prerequisites.
# Safe to run repeatedly. Run from anywhere inside the repository.
$ErrorActionPreference = 'Stop'

$root = (git rev-parse --show-toplevel).Trim()
Set-Location $root

Write-Host '== Subject system (eShop fork, pinned by submodule)'
git submodule update --init --recursive
if ($LASTEXITCODE -ne 0) { throw 'git submodule update failed' }
Write-Host "subject/eshop at $(git -C subject/eshop rev-parse --short HEAD)"

Write-Host '== Private evaluation material must not be present'
$found = Get-ChildItem -Path $root -Recurse -Force -ErrorAction SilentlyContinue -Filter '*private-eval*' |
    Where-Object { $_.FullName -notlike (Join-Path $root 'subject*') }
if ($found) {
    Write-Error "Found private evaluation material in this working tree. Remove it: $($found.FullName -join ', ')"
    exit 1
}
Write-Host 'none found'

Write-Host '== Prerequisites'
$missing = $false
function Test-Tool($name, $versionArgs, $hint) {
    if (Get-Command $name -ErrorAction SilentlyContinue) {
        $v = (& $name $versionArgs 2>&1 | Select-Object -First 1)
        Write-Host "ok       $name ($v)"
        return $true
    }
    Write-Host "MISSING  ${name}: $hint"
    return $false
}
if (-not (Test-Tool 'dotnet' '--version' 'install the SDK named in subject/eshop/global.json')) { $missing = $true }
if (-not (Test-Tool 'docker' '--version' 'Aspire needs a container runtime (Docker or Podman) to run eShop')) { $missing = $true }
if (-not (Test-Tool 'node' '--version' "needed for the capability's React frontend")) { $missing = $true }

if (Get-Command dotnet -ErrorAction SilentlyContinue) {
    $required = (Get-Content subject/eshop/global.json -Raw | ConvertFrom-Json).sdk.version
    $band = $required.Substring(0, $required.Length - 2)   # e.g. 10.0.302 -> 10.0.3 (feature band)
    if (dotnet --list-sdks | Where-Object { $_ -like "$band*" }) {
        Write-Host "ok       .NET SDK feature band for $required"
    } else {
        Write-Host "MISSING  .NET SDK $required (from subject/eshop/global.json)"
        $missing = $true
    }
}

if ($missing) {
    Write-Host 'Bootstrap finished with missing prerequisites (see above).'
    exit 2
}
Write-Host 'Bootstrap complete.'
