param([Parameter(Mandatory=$true)][string]$OutputDirectory)
if (-not $env:DATABASE_URL) { Write-Error 'DATABASE_URL is required.'; exit 1 }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
& "$PSScriptRoot\backup_supabase.ps1" -OutputPath (Join-Path $OutputDirectory 'backup.dump'); if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$PSScriptRoot\schema_preflight.py" --output (Join-Path $OutputDirectory 'schema.json'); if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$status = (Get-Content (Join-Path $OutputDirectory 'schema.json') -Raw | ConvertFrom-Json).status
if ($status -ne 'MATCH') { Write-Error "Schema preflight status: $status"; exit 1 }
Write-Host "Readiness complete: $OutputDirectory"
