# Migration Readiness Batch Runbook

# Migration Readiness Batch Runbook

## 목적

이 작업은 DB를 바꾸지 않는다. 한 번의 PowerShell 명령으로 로컬 백업과 읽기 전용 schema 비교 보고서를 만든다.

## 실행 전

1. PostgreSQL client tools가 설치되어 있고 `pg_dump --version`이 동작하는지 확인한다.
2. Supabase Session Pooler 주소를 `DATABASE_URL`로 현재 PowerShell 창에만 설정한다. 주소는 파일·채팅·Git에 저장하지 않는다.
3. 비어 있는 새 출력 폴더 경로를 정한다. 기존 폴더를 지정하면 스크립트는 중단한다.

## 단일 실행

```powershell
$env:DATABASE_URL = 'Supabase connection string entered locally only'
./scripts/run_migration_readiness.ps1 -OutputDirectory 'C:\migration-readiness\20260809'
```

성공하면 출력 폴더에 `backup.dump`와 `schema.json`이 생성된다. 스크립트는 `MATCH`일 때만 성공한다. `DRIFT` 또는 `UNKNOWN`이면 migration을 실행하지 않고 중단한다.

## 실행 후

- `backup.dump`는 안전한 로컬 또는 암호화된 저장소에 보관한다.
- `schema.json`의 `status`와 `differences`만 검토한다. DB 비밀번호·주소는 공유하지 않는다.
- `MATCH`여도 실제 migration 적용은 별도 명시 승인 후에만 진행한다.
