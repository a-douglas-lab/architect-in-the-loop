# Cases G1 to G10 in expected.md, for scripts/check-private-material.ps1.
# Each case builds a throwaway tree under a fresh temporary folder. Usage: test-private-material.ps1 [-Old]
# -Old runs the guard as it was in scripts/bootstrap.ps1 at 2732f29, lines 14 to 15, to show the gap.
param([switch]$Old)

$guard = Join-Path $PSScriptRoot '..\..\scripts\check-private-material.ps1'
$url = 'https://github.com/a-douglas-lab/Architect-in-the-loop-evaluator.git'

function Test-OldGuard($root) {
    $found = Get-ChildItem -Path $root -Recurse -Force -ErrorAction SilentlyContinue -Filter '*private-eval*' |
        Where-Object { $_.FullName -notlike (Join-Path $root 'subject*') }
    if ($found) { 1 } else { 0 }
}

function New-Tree($case, $r) {
    New-Item -ItemType Directory -Force "$r\docs", "$r\subject\eshop\src" | Out-Null
    switch ($case) {
        'G2' { New-Item -ItemType Directory "$r\Architect-in-the-loop-evaluator" | Out-Null }
        'G3' { New-Item -ItemType Directory -Force "$r\docs\x\architect-in-the-loop-EVALUATOR" | Out-Null }
        'G4' { New-Item -ItemType Directory "$r\subject\Architect-in-the-loop-evaluator" | Out-Null }
        'G5' { New-Item -ItemType Directory "$r\subject\private-eval" | Out-Null }
        'G6' { New-Item -ItemType Directory "$r\private-eval" | Out-Null }
        'G7' { New-Item -ItemType File "$r\Architect-in-the-loop-evaluator.zip" | Out-Null }
        'G8' { New-Item -ItemType Directory -Force "$r\scratch\.git" | Out-Null
               Set-Content -Encoding ascii "$r\scratch\.git\config" "[remote `"origin`"]`n`turl = $url" }
        'G9' { Set-Content -Encoding ascii "$r\.gitmodules" "[submodule `"x`"]`n`tpath = x`n`turl = $url" }
        'G10' { New-Item -ItemType Directory -Force "$r\evaluator", "$r\Architect-in-the-loop", "$r\grader-evaluation", "$r\other\.git" | Out-Null
                Set-Content -Encoding ascii "$r\other\.git\config" "[remote `"origin`"]`n`turl = https://github.com/dotnet/eShop.git" }
    }
}

$want = @{ G1 = 0; G2 = 1; G3 = 1; G4 = 1; G5 = 1; G6 = 1; G7 = 1; G8 = 1; G9 = 1; G10 = 0 }
$fails = 0
foreach ($c in 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10') {
    $root = Join-Path ([IO.Path]::GetTempPath()) ([IO.Path]::GetRandomFileName())
    New-Tree $c $root
    if ($Old) {
        Write-Host "$c old guard: exit $(Test-OldGuard $root)"
    } else {
        powershell -NoProfile -ExecutionPolicy Bypass -File $guard -Root $root *> $null
        $got = $LASTEXITCODE
        $r = if ($got -eq $want[$c]) { 'pass' } else { $fails++; 'FAIL' }
        Write-Host "$c exit $got, expected $($want[$c]): $r"
    }
    Remove-Item -Recurse -Force $root
}
if (-not $Old) { Write-Host "failures: $fails" }
exit $fails
