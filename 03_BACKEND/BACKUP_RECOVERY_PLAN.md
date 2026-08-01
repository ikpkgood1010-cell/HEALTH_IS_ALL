# BACKUP_RECOVERY_PLAN

## Purpose
본 문서는 시스템 장애, 데이터 파손, 인프라 붕괴 상황 시 데이터 유실을 방지하고 빠른 서비스 정상화를 위한 백업 주기, 복구 절차(RPO/RTO) 및 재해 복구(DR) 표준을 정립하는 SSOT이다.

## Scope
백엔드 RDB, Redis, S3 스토리지, AI Prompt/Formula 버전 관리에 적용된다.

## SSOT
복구 목표 시간, 목표 시점 및 장애 유형별 DR 실행 가이드의 단일 진실 출처이다.

## Service Level Objectives (RPO & RTO)
- **RPO (Recovery Point Objective - 최대 허용 데이터 손실 시간)**: $< 5\text{분}$
- **RTO (Recovery Time Objective - 최대 허용 서비스 중단 시간)**: $< 30\text{분}$

## Backup Schedule Matrix

| Target System | Backup Type | Frequency | Storage Location | Retention |
| :--- | :--- | :--- | :--- | :--- |
| **Database (RDB)** | WAL Archiving + Full Snapshot | Continuous / Daily 03:00 | Multi-AZ Cloud Storage | 30 Days |
| **S3 Storage** | Cross-Region Replication | Real-time | Secondary Cloud Region | 30 Days |
| **Redis Cache** | RDB Snapshot | Daily 04:00 | Local Encrypted Storage | 7 Days |
| **Formula / Prompt**| Git Tag & Vault Sync | Event-driven (On Release) | Version Controlled Registry | Permanent |

## Disaster Recovery Execution Flow
1. **Detection**: Health Check 실패 Alert 통지.
2. **Failover Decision**: 주 DB 장애 확인 시 3분 이내 Secondary DB로 Read-Write Switchover 단행.
3. **Formula & Prompt Rollback**: 계산식 또는 프롬프트 이상 시 이전 Git Tag 시점으로 1분 내 즉시 복원.

## Runtime Impact
- 치명적인 데이터센터 장애 발생 시에도 30분 이내에 5분 전 데이터 상태로 완벽 복구된다.

## Related Documents
- `03_BACKEND/OBSERVABILITY_RUNBOOK.md`
- `03_BACKEND/FEATURE_FLAG_POLICY.md`

## Change History
- v1.0.0 (2026-07-31): Backup Recovery Plan established.