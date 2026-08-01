# CONFIG_REGISTRY

- Version: 1.0
- Status: Active
- Last Updated: 2026-08-01
- Purpose: 핵심 구성값의 SSOT와 코드 위치를 한 파일에서 관리한다.

| Config | Value | Code | Document | Verification |
|---|---|---|---|---|
| `SSOT_EXP_LABEL` | `Exp` | `backend/config.py` | `00_PROJECT/CANONICAL_NAMING.md` | `scripts/check_canonical_constants.py`, `scripts/check_patch005_integrity.py` |
| `SSOT_CHARACTER_NAME` | `건강이` | `backend/config.py`, `backend/models.py` | `00_PROJECT/CANONICAL_CONSTANTS.md`, `00_PROJECT/CANONICAL_NAMING.md` | same |
| `DAILY_EXP_CAP` | `300` | `backend/config.py`, `backend/models.py`, `lib/mock_data_provider.dart` | `00_PROJECT/CANONICAL_CONSTANTS.md`, `03_GAME_SYSTEM/EXP_RULE.md` | same |
| `WEEKLY_EXP_SOFT_CAP` | `2100` | 문서 기준만 존재 | `00_PROJECT/CANONICAL_CONSTANTS.md`, `03_GAME_SYSTEM/EXP_RULE.md` | manual review |
| `ANTI_FARMING_INTERVAL_MINUTES` | `10` | `backend/config.py`, `.env.example` | `00_PROJECT/CANONICAL_CONSTANTS.md`, `03_GAME_SYSTEM/EXP_RULE.md` | `scripts/check_canonical_constants.py`, `scripts/check_patch005_integrity.py` |
| `HEALTH_SCORE_MIN` | `0` | 문서 기준 | `00_PROJECT/CANONICAL_CONSTANTS.md` | manual review |
| `HEALTH_SCORE_MAX` | `100` | 문서 기준 | `00_PROJECT/CANONICAL_CONSTANTS.md` | manual review |
| `SQLALCHEMY_DATABASE_URL` | env or sqlite fallback | `backend/config.py`, `backend/database.py` | `.env.example` | API tests |
| `APP_NAME` | `HEALTH IS ALL` | `backend/config.py` | `.env.example`, `README.md` | API tests |
| `APP_VERSION` | `2.1.0-repair` | `backend/config.py` | `.env.example` | API root response |

## Drift Notes
1. 주간 soft cap 2100은 문서에는 있으나 전용 런타임 상수로 분리되어 있지 않다.
2. Point 경제 관련 중앙 config는 아직 미구축 상태다.
3. Time zone / locale policy는 문서 SSOT만 있고 코드 설정 객체에는 직접 반영되지 않았다.
