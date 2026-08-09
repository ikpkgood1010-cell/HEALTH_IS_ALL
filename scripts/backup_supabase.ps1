param([Parameter(Mandatory=$true)][string]$OutputPath)
if (-not $env:DATABASE_URL) { Write-Error 'DATABASE_URL is required.'; exit 1 }
if (-not (Get-Command pg_dump -ErrorAction SilentlyContinue)) { Write-Host 'pg_dump is not installed. Install PostgreSQL client tools and retry.'; exit 1 }
pg_dump --format=custom --file $OutputPath $env:DATABASE_URL
