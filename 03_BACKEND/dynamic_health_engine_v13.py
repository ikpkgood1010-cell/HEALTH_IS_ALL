"""
HEALTH IS ALL - Dynamic Health & Game Dual-Balance Engine V13
File Path: HEALTH IS ALL/03_BACKEND/dynamic_health_engine_v13.py
Description: 다변수 동적 보상 연산 및 2단계 Fallback 안전 강하 시스템
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DynamicHealthEngineV13")

class CalculationMode(Enum):
    DYNAMIC_MULTI = "DYNAMIC_MULTI"
    FALLBACK_SIMPLE = "FALLBACK_SIMPLE"

@dataclass
class HealthInputData:
    steps: int
    burned_kcal: float
    avg_hr: float
    max_hr: float
    circadian_factor: Optional[float] = 1.0
    nutritive_synergy: Optional[float] = 1.0

@dataclass
class CalculationResult:
    calculation_mode: CalculationMode
    exp_gained: int
    spirit_affinity_delta: int
    snack_reward_count: int
    health_tip: Dict[str, Any]

class DynamicHealthEngineV13:
    BASE_EXP_PER_KCAL = 1.0  # 기본 칼로리 당 EXP 환산비
    
    # 1~3줄 꿀팁 데이터베이스 큐 (실시 예시)
    TIP_DATABASE = [
        "단백질 섭취 후 30분 내 가벼운 산책은 근육 합성률을 높여줘요! 정령도 함께 기운을 얻었습니다.",
        "식사 후 15분 산책은 혈당 피크를 예방하는 가장 효과적인 방법입니다.",
        "충분한 수분 섭취는 대사율을 올려 정령의 친밀도 상승을 돕습니다!"
    ]

    def calculate_rewards(self, user_id: str, health_data: HealthInputData) -> CalculationResult:
        """
        다변수 연산 시도 후, 오류/파라미터 누락 발생 시 2단계 Fallback으로 즉시 강하
        """
        try:
            # 필수 파라미터 검증 및 연산 가능 여부 확인
            if (health_data.max_hr is None or health_data.max_hr <= 0 or 
                health_data.circadian_factor is None or health_data.nutritive_synergy is None):
                raise ValueError("필수 파라미터 누락 또는 0으로 나누기 위험 감지")

            # 1단계: 다변수 동적 공식 연산
            hr_ratio = health_data.avg_hr / health_data.max_hr
            base_exp = health_data.burned_kcal * self.BASE_EXP_PER_KCAL
            
            # EXP_final = EXP_base * (1 + avg_hr / max_hr) * Factor_circadian * Synergy_nutritive
            final_exp = int(round(base_exp * (1 + hr_ratio) * health_data.circadian_factor * health_data.nutritive_synergy))
            
            affinity_delta = max(1, int(final_exp * 0.02))
            snack_count = 2 if final_exp >= 500 else 1
            
            logger.info(f"[{user_id}] DYNAMIC_MULTI 연산 성공: {final_exp} EXP")
            
            return CalculationResult(
                calculation_mode=CalculationMode.DYNAMIC_MULTI,
                exp_gained=final_exp,
                spirit_affinity_delta=affinity_delta,
                snack_reward_count=snack_count,
                health_tip={
                    "lines_count": 1,
                    "message": self.TIP_DATABASE[0]
                }
            )

        except Exception as e:
            # 2단계: Fallback 간결 공식으로 즉시 강하
            logger.warning(f"[{user_id}] 연산 예외 발생 ({e}). FALLBACK_SIMPLE 모드로 강하합니다.")
            
            fallback_exp = int(health_data.burned_kcal * self.BASE_EXP_PER_KCAL)
            fallback_affinity = max(1, int(fallback_exp * 0.01))
            
            return CalculationResult(
                calculation_mode=CalculationMode.FALLBACK_SIMPLE,
                exp_gained=fallback_exp,
                spirit_affinity_delta=fallback_affinity,
                snack_reward_count=1,
                health_tip={
                    "lines_count": 1,
                    "message": "꾸준한 활동으로 정령과 함께 건강해지고 있어요!"
                }
            )