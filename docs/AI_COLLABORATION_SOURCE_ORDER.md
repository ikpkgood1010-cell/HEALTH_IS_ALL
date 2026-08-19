# 다른 AI와 협업할 때 읽힐 자료 순서

상태: **CANONICAL / 2026-08-16**

다른 AI에게 프로젝트를 전달할 때 GitHub와 로컬 자료 중 하나만 선택하지 않는다.
버전과 결정은 GitHub를 기준으로 하고, 대용량 원본 에셋과 아직 정리되지 않은 참고 자료만
로컬 폴더에서 추가로 제공한다.

## 읽기 우선순위

1. GitHub 최신 `main` 또는 현재 작업 PR의 코드와 `docs/`
2. `docs/GAME_DIRECTION_V2_CANONICAL.md`
3. `docs/GAME_2D_ART_AND_ANIMATION_PIPELINE.md`
4. `docs/MASTER_PLAN_IMPLEMENTATION_MAP.md`
5. 현재 작업 브랜치의 변경 내용과 테스트 결과
6. 사용자가 명시적으로 제공한 로컬 ZIP·HTML·이미지 원본

GitHub에 없는 로컬 문서는 자동으로 canonical로 취급하지 않는다. 로컬 자료가 GitHub
canonical 문서와 충돌하면 최신 사용자 결정과 GitHub canonical 문서를 우선하고, 해결되지
않은 충돌만 사용자에게 파일명·문구와 함께 보고한다.

## 다른 AI에게 전달할 필수 문구

```text
먼저 GitHub의 최신 main과 docs/GAME_DIRECTION_V2_CANONICAL.md,
docs/GAME_2D_ART_AND_ANIMATION_PIPELINE.md를 읽으세요. 이것이 현재 확정 기준입니다.
로컬 첨부 자료는 근거·원본·참고 자료이며, GitHub canonical과 충돌하면 임의로 선택하지
말고 충돌한 파일명과 내용을 보고하세요. 코드나 문서를 수정하기 전 git status와 현재
브랜치를 확인하고, 기존 사용자 변경을 삭제하거나 되돌리지 마세요.
```

비밀번호, `DATABASE_URL`, API 키, 실제 `.env`는 다른 AI에 첨부하지 않는다.

