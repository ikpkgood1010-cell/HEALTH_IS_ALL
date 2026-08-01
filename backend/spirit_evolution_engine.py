"""
HEALTH IS ALL - AI Spirit Evolution & Elemental Score Engine
Filename: spirit_evolution_engine.py
Path: HEALTH IS ALL/backend/spirit_evolution_engine.py
Purpose: 영양소/운동/수면 데이터 기반 정령 4대 속성 점수 및 진화 단계 산출 엔진
"""

import math
import random
from typing import Dict, Any

class SpiritEvolutionEngine:
    """
    정령 속성 점수 계산 및 진화 상태 판정 엔진
    """

    EVOLUTION_STAGES = ["EGG", "BABY", "JUNIOR", "SENIOR", "MASTER"]

    @staticmethod
    def calculate_elemental_evolution(
        protein_g: float,
        carbs_g: float,
        fat_g: float,
        veggie_fiber_g: float,
        strength_workout_min: float,
        cardio_workout_min: float,
        recovery_score: float,
        current_affinity_lvl: int = 1,
        consecutive_balanced_days: int = 1
    ) -> Dict[str, Any]:
        """
        다변수 영양 및 운동 수치를 기반으로 4대 속성 점수와 최종 진화 상태 계산
        """
        # 1. 입력 데이터 유효성 검증
        if protein_g < 0 or carbs_g < 0 or fat_g < 0:
            return SpiritEvolutionEngine._build_fallback_evolution()

        # 2. 미세 난수 지터 ($0.96 \sim 1.04$) 생성
        jitter = random.uniform(0.96, 1.04)
        affinity_multiplier = 1.0 + (current_affinity_lvl * 0.02)

        # 3. 속성별 점수 산출
        # 불(Fire): 단백질 섭취 + 근력 운동
        fire_score = ((protein_g * 2.2) + (strength_workout_min * 3.8)) * affinity_multiplier * jitter

        # 물(Water): 유산소 운동 + 수분/카보 대사
        water_score = ((cardio_workout_min * 4.2) + (carbs_g * 0.8)) * affinity_multiplier * jitter

        # 풀(Earth/Nature): 식이섬유/야채 섭취 + 수면 회복 점수
        earth_score = ((veggie_fiber_g * 5.5) + (recovery_score * 1.5)) * affinity_multiplier * jitter

        # 빛(Light): 탄단지 밸런스 + 연속 균형 달성일
        total_macro_kcal = (protein_g * 4) + (carbs_g * 4) + (fat_g * 9)
        balance_index = 1.0
        if total_macro_kcal > 0:
            p_ratio = (protein_g * 4) / total_macro_kcal
            c_ratio = (carbs_g * 4) / total_macro_kcal
            f_ratio = (fat_g * 9) / total_macro_kcal
            # 이상적 비율(P:3, C:5, F:2)과의 이격도 계산
            dev = abs(p_ratio - 0.3) + abs(c_ratio - 0.5) + abs(f_ratio - 0.2)
            balance_index = max(0.2, 1.5 - dev)

        light_score = (balance_index * 80.0) + (consecutive_balanced_days * 12.0) * jitter

        # 4. 주 속성(Dominant Element) 및 오버히트 판정
        scores = {
            "FIRE": fire_score,
            "WATER": water_score,
            "EARTH": earth_score,
            "LIGHT": light_score
        }
        dominant_element = max(scores, key=scores.get)

        # 단백질/불 속성 쏠림 시 오버히트 경고 (건강 안심 장치)
        is_overheated = False
        if fire_score > (water_score + earth_score + light_score) * 1.2 and fire_score > 300:
            is_overheated = True

        # 5. 진화 단계 도출 (총 경험치 기반)
        total_exp = fire_score + water_score + earth_score + light_score
        stage_index = min(4, int(total_exp // 250))
        evolution_stage = SpiritEvolutionEngine.EVOLUTION_STAGES[stage_index]

        # 6. 유저 호감형 반응 인터페이스 대화 문구 생성
        dialogue = SpiritEvolutionEngine._generate_friendly_dialogue(
            dominant_element, evolution_stage, is_overheated
        )

        return {
            "fire_score": round(fire_score, 1),
            "water_score": round(water_score, 1),
            "earth_score": round(earth_score, 1),
            "light_score": round(light_score, 1),
            "dominant_element": dominant_element,
            "evolution_stage": evolution_stage,
            "total_spirit_exp": round(total_exp, 1),
            "is_overheated": is_overheated,
            "friendly_dialogue": dialogue,
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_evolution() -> Dict[str, Any]:
        return {
            "fire_score": 50.0,
            "water_score": 50.0,
            "earth_score": 50.0,
            "light_score": 100.0,
            "dominant_element": "LIGHT",
            "evolution_stage": "BABY",
            "total_spirit_exp": 250.0,
            "is_overheated": False,
            "friendly_dialogue": "정령이 차분히 기운을 모으고 있어요. 오늘도 따뜻하게 시작해봐요! 🌿",
            "is_fallback": True
        }

    @staticmethod
    def _generate_friendly_dialogue(element: str, stage: str, overheated: bool) -> str:
        if overheated:
            return "🔥 정령의 불꽃이 조금 뜨거워졌어요! 차가운 물 한 잔과 가벼운 산책으로 기운을 달래주세요."
        
        dialogues = {
            "FIRE": "💪 든든한 단백질 에너지 덕분에 정령의 불꽃이 힘차게 피어나고 있어요!",
            "WATER": "💧 유산소 운동의 시원한 바람을 타고 정령이 촉촉하게 성장 중입니다!",
            "EARTH": "🌿 싱그러운 채소와 편안한 휴식이 정령에게 따스한 숲을 선물했어요.",
            "LIGHT": "✨ 완벽한 영양 균형에 정령이 눈부신 빛의 아우라를 감싸 안았습니다!"
        }
        return dialogues.get(element, "🌱 정령이 당신의 하루를 응원하며 무럭무럭 자라고 있어요!")

if __name__ == "__main__":
    engine = SpiritEvolutionEngine()
    res = engine.calculate_elemental_evolution(
        protein_g=95.0, carbs_g=160.0, fat_g=45.0, veggie_fiber_g=25.0,
        strength_workout_min=30.0, cardio_workout_min=20.0, recovery_score=82.0
    )
    print(f"[Spirit Evolution Engine Output] {res}")