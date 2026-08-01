# MASTER_DOCUMENT_INDEX_V2.md

## Purpose
본 문서는 'HEALTH IS ALL' 프로젝트의 모든 구조와 최신 모듈, 사양서, 코드 파일의 경로를 총괄 관리하는 마스터 색인(Master Document Index) v2입니다.

## Scope
* `HEALTH IS ALL` 프로젝트 내의 모든 사양서, 모듈, 코드 파일 구조 관리
* 최신 문서 및 코드의 버전 상태 및 아카이브(00_ARCHIVE) 이관 이력 관리

## SSOT
* **경로**: `HEALTH IS ALL/00_PROJECT_START/MASTER_DOCUMENT_INDEX_V2.md`
* **소유팀**: Project PMO & Architecture Board

## Definitions
* **Master Index**: 프로젝트의 전체 문서 및 소스 코드의 위치, 버전, 상호 관계를 한눈에 파악할 수 있는 단일 진실 공급원 색인.

## Runtime
* **실행 환경**: 문서 관리 및 빌드 오케스트레이션 시스템

## Rules
1. 새 모듈이나 사양서가 생성되거나 버전이 업그레이드되면 본 마스터 색인에 즉시 반영한다.
2. 이전 버전은 반드시 `HEALTH IS ALL/00_ARCHIVE/` 경로로 이관되어야 한다.
3. 모든 신규 작성 문서는 정의된 표준 가이드라인 구조를 준수한다.

## State
* `ACTIVE`: 색인 최신화 완료 상태
* `UPDATING`: 문서 업데이트 진행 상태

## Event
* `ON_DOCUMENT_CREATED`: 신규 파일 생성 시 마스터 색인 자동 업데이트
* `ON_VERSION_UPGRADED`: 버전 업그레이드 및 아카이브 이관 기록

## Example
* `UNIFIED_ENGINE_V9_SPEC.md` 생성 시 V8 버전이 아카이브로 이관되고, 본 마스터 색인의 01_ARCHITECTURE 섹션에 V9이 최신 문서로 등록됨.

## Exception
* 경로 불일치 발생 시: 빌드 타임 시 시스템 에러 경고 발생.

## Related Documents
* `HEALTH IS ALL/00_PROJECT_START/FOLDER_STRUCTURE.mdux`
* `HEALTH IS ALL/00_PROJECT/DOCUMENT_DEPENDENCY_MATRIX.mdux`

## Change History
* **v2.0.0 (2026-07-31)**: V1 대비 2026 최신 V9 엔진 시리즈 및 호감형 AI 대화 시스템 통합 색인 전면 개편.