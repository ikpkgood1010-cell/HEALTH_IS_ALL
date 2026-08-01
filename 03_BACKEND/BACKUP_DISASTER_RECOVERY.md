# BACKUP_DISASTER_RECOVERY.md

## Purpose
데이터베이스 오염 및 인프라 장애 발생 시 신속히 복구하기 위한 백업 및 재해 복구(DR) 명세를 정의한다.

## Rules
1. **RPO / RTO**: RPO < 5분, RTO < 15분.
2. **백업 주기**: Daily Full Snapshot (03:00 KST) + 5분 WAL Archiving.

## Change History
* **v1.0.0 (2026-07-31)**: PATCH-005 최초 작성.