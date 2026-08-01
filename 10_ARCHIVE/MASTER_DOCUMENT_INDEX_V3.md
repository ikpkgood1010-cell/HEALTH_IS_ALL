[코드 다운로드: MASTER_DOCUMENT_INDEX_V3.md]
[코드 복사]
<!-- 여기부터 복사 -->
# MASTER DOCUMENT INDEX V3

## Purpose
본 문서는 HEALTH IS ALL 프로젝트 내의 모든 사양서, 엔진 코드, 디자인, 데이터베이스 스키마 문서의 최신 색인과 의존 관계를 중앙에서 관리하는 단일 색인(Master Index) 역할을 수행한다.

## Scope
HEALTH IS ALL 시스템 전체(00_PROJECT부터 10_ARCHIVE까지)의 모든 문서 및 소스코드의 명칭, 저장 경로, 최신 버전을 포함한다.

## SSOT
`HEALTH IS ALL/00_PROJECT/MASTER_DOCUMENT_INDEX_V3.md`

## Definitions
- **Master Index**: 프로젝트 전반의 문서 버전 및 저장 위치를 총괄 정의하는 표준 문서.
- **SSOT**: Single Source of Truth, 해당 시스템 및 규격의 단일 진실 출처.

## Runtime
시스템 빌드, 문서 자동화 검증 시 및 CI/CD 워크플로우 실행 시 상시 참조된다.

## Rules
1. 모든 파일 생성 및 업그레이드 시 본 색인 문서에 즉시 반영해야 한다.
2. 이전 버전 문서는 생성 즉시 `10_ARCHIVE/` 폴더로 이동하여 보관한다.
3. 문서 저장 경로는 절대 경로 형식의 프로젝트 상대 경로를 준수한다.

## State
- Current Active Version: V3.0
- Total Managed Files: 120+ Documents & Engine Source Files

## Event
- `ON_DOCUMENT_UPGRADE`: 대상 문서의 버전이 업그레이드될 때 본 문서를 자동 update한다.

## Example
`UNIFIED_ENGINE_V10_SPEC.md` 업그레이드 시 본 문서의 01_ARCHITECTURE 섹션 최신화.

## Exception
인덱스 누락 발생 시 빌드 스크립트에서 CI/CD 경고를 발생시키고 자동 복구를 시도한다.

## Related Documents
- `HEALTH IS ALL/00_PROJECT_START/DOCUMENT_DEPENDENCY_MAP.md`
- `HEALTH IS ALL/01_ARCHITECTURE/ARCHITECTURE_INDEX.md`

## Change History
- 2026-07-31 (V3.0): V10 엔진, V8 스키마, V2 꿀팁 피더 추가에 따른 마스터 인덱스 개정.
<!-- 여기까지 복사 -->