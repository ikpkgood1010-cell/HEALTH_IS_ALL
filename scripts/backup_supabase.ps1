param([Parameter(Mandatory=$true)][string]$OutputPath)
if (-not $env:DATABASE_URL) { Write-Error 'DATABASE_URL is required.'; exit 1 }
$pgDump = Get-Command pg_dump -ErrorAction SilentlyContinue
if (-not $pgDump -and $env:ProgramFiles) {
    $pgDump = Get-ChildItem -Path (Join-Path $env:ProgramFiles 'PostgreSQL') -Filter pg_dump.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
}
if (-not $pgDump) { Write-Host 'pg_dump is not installed. Install PostgreSQL client tools and retry.'; exit 1 }
& $pgDump.Source --format=custom --file $OutputPath $env:DATABASE_URL
