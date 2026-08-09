param([Parameter(Mandatory=$true)][string]$OutputDirectory)
if (-not $env:DATABASE_URL) { Write-Error 'DATABASE_URL is required.'; exit 1 }
if (Test-Path $OutputDirectory) { Write-Error 'OutputDirectory must not already exist.'; exit 1 }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
& "$PSScriptRoot\backup_supabase.ps1" -OutputPath (Join-Path $OutputDirectory 'backup.dump'); if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $venvPython = Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe'
    if (Test-Path $venvPython) { $python = Get-Item $venvPython }
}
if (-not $python) { Write-Error 'Python is not available. Create the project .venv and retry.'; exit 1 }
& $python.Source "$PSScriptRoot\schema_preflight.py" --output (Join-Path $OutputDirectory 'schema.json'); if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$status = (Get-Content (Join-Path $OutputDirectory 'schema.json') -Raw | ConvertFrom-Json).status
if ($status -ne 'MATCH') { Write-Error "Schema preflight status: $status"; exit 1 }
Write-Host "Readiness complete: $OutputDirectory"
