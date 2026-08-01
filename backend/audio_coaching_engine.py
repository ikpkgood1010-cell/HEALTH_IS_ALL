"""
HEALTH IS ALL - AI Audio Coaching Engine
Filename: audio_coaching_engine.py
Path: HEALTH IS ALL/backend/audio_coaching_engine.py
Purpose: 실시간 심박수, 페이스, 정령 속성에 기반한 따뜻한 음성 코칭 멘트 동적 생성 백엔드 엔진
"""

import random
from typing import Dict, Any

class AudioCoachingEngine:
    """
    실시간 바이오 데이터 기반 맞춤형 오디오 코칭 멘트 생성기
    """

    @staticmethod
    def generate_coaching_script(
        current_hr: int,
        target_hr_min: int,
        target_hr_max: int,
        spirit_element: str = "LIGHT",
        spirit_affinity_lvl: int = 1,
        workout_duration_min: int = 15
    ) -> Dict[str, Any]:
        """
        심박수 구간별 정령 속성 및 친밀도를 반영한 호감형 음성 가이드 산출
        """
        if current_hr <= 0:
            return AudioCoachingEngine._build_fallback_coaching()

        jitter = random.uniform(0.97, 1.03)
        hr_ratio = current_hr / max(1, target_hr_max)

        # 1. 심박수 안전 상태 판정
        if current_hr > target_hr_max * 1.05:
            coaching_type = "OVERLOAD_WARNING"
            script = (
                f"유저님, 지금 심박수가 {current_hr}회로 가빠졌어요! "
                f"정령이 옆에서 함께 걷고 있으니, 1분간 속도를 줄이고 크게 호흡해볼까요? 🌿"
            )
            should_slow_down = True
        elif target_hr_min <= current_hr <= target_hr_max:
            coaching_type = "OPTIMAL_ZONE"
            element_dialogue = AudioCoachingEngine._get_element_praise(spirit_element)
            script = (
                f"완벽한 페이스예요! 현재 심박수 {current_hr}회로 최적 유산소 구간에 있습니다. "
                f"{element_dialogue} {workout_duration_min}분째 훌륭히 달리고 계셔요! ✨"
            )
            should_slow_down = False
        else:
            coaching_type = "WARM_UP"
            script = (
                f"좋은 출발입니다! 심박수 {current_hr}회로 차분히 몸을 풀고 계시네요. "
                f"정령과 함께 가볍게 보폭을 넓혀볼까요? 🏃‍♂️"
            )
            should_slow_down = False

        # 2. 정령 음성 템포 조절값 수식
        voice_tempo = round((1.0 + (hr_ratio - 1.0) * 0.15) * jitter, 2)
        voice_tempo = max(0.85, min(1.25, voice_tempo))

        return {
            "coaching_type": coaching_type,
            "voice_script": script,
            "voice_tempo": voice_tempo,
            "should_slow_down": should_slow_down,
            "current_hr": current_hr,
            "spirit_element": spirit_element,
            "is_fallback": False
        }

    @staticmethod
    def _get_element_praise(element: str) -> str:
        praises = {
            "FIRE": "불 정령이 활기찬 불꽃으로 유저님의 에너지를 밝혀주고 있어요!",
            "WATER": "물 정령이 시원한 바람을 일으켜 땀을 쾌적하게 씻어줍니다!",
            "EARTH": "풀 정령이 숲속의 싱그러운 아침 공기를 전하고 있어요!",
            "LIGHT": "빛 정령이 눈부신 아우라로 유저님의 발걸음을 응원합니다!"
        }
        return praises.get(element, "정령이 유저님의 건강한 걸음을 진심으로 기뻐하고 있어요!")

    @staticmethod
    def _build_fallback_coaching() -> Dict[str, Any]:
        return {
            "coaching_type": "SAFE_GUIDE",
            "voice_script": "호흡을 편안하게 유지하며 유저님만의 편안한 속도로 걸어보세요. 정령이 늘 함께합니다 🌿",
            "voice_tempo": 1.0,
            "should_slow_down": False,
            "current_hr": 90,
            "spirit_element": "LIGHT",
            "is_fallback": True
        }

if __name__ == "__main__":
    engine = AudioCoachingEngine()
    res = engine.generate_coaching_script(
        current_hr=142, target_hr_min=120, target_hr_max=150,
        spirit_element="FIRE", spirit_affinity_lvl=3, workout_duration_min=20
    )
    print(f"[Audio Coaching Engine Output] {res}")