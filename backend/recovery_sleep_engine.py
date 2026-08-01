"""
HEALTH IS ALL - Precision Sleep & Recovery Engine
Filename: recovery_sleep_engine.py
Path: HEALTH IS ALL/backend/recovery_sleep_engine.py
Purpose: 수면 효율, 깊은 수면 비율, HRV 데이터를 결합하여 회복 지수(RS)를 정밀 산출하는 백엔드 엔진
"""

import random
from typing import Dict, Any

class RecoverySleepEngine:
    """
    수면 데이터 분석 및 일일 회복 지수($RS$) 계산 엔진
    """

    @staticmethod
    def calculate_recovery_index(
        total_sleep_min: float,
        deep_sleep_min: float,
        rem_sleep_min: float,
        hrv_ms: float,
        bed_time_efficiency: float
    ) -> Dict[str, Any]:
        """
        다변수 수면 수치를 세분화 공식에 대입하여 0~100 범위의 회복 지수 도출
        """
        # 1. 예외 및 유효성 검사
        if total_sleep_min <= 0 or bed_time_efficiency <= 0:
            return RecoverySleepEngine._build_fallback_recovery()

        jitter = random.uniform(0.96, 1.04)

        # 2. 세분화 요소별 점수 산출
        # (1) 수면 시간 및 효율 점수 (40%)
        time_score = min(100.0, (total_sleep_min / 480.0) * 100.0)
        eff_score = (bed_time_efficiency * 0.6) + (time_score * 0.4)

        # (2) 깊은 수면 + 렘수면 비율 점수 (35%)
        deep_ratio = deep_sleep_min / max(1.0, total_sleep_min)
        rem_ratio = rem_sleep_min / max(1.0, total_sleep_min)
        quality_score = min(100.0, (deep_ratio * 250.0) + (rem_ratio * 150.0))

        # (3) HRV (심박 변이도) 안정성 점수 (25%)
        hrv_score = min(100.0, (hrv_ms / 80.0) * 100.0)

        # 3. 종합 회복 지수 ($RS$) 수식
        raw_rs = (eff_score * 0.40) + (quality_score * 0.35) + (hrv_score * 0.25)
        final_rs = round(max(10.0, min(100.0, raw_rs * jitter)), 1)

        # 4. 정령 반응 및 상태 결정
        if final_rs >= 80.0:
            status_title = "최상의 생체 에너지 ✨"
            spirit_message = "깊은 수면 덕분에 정령과 유저님 모두 100% 충전되었어요! 멋진 하루를 시작해볼까요?"
            slumber_mode = False
        elif final_rs >= 50.0:
            status_title = "안정적인 회복 상태 🌿"
            spirit_message = "무난하고 편안한 밤을 보내셨네요. 오늘 하루도 차분히 건강 습관을 이어가요."
            slumber_mode = False
        else:
            status_title = "휴식이 필요한 상태 🌙"
            spirit_message = "몸이 조금 피곤할 수 있어요. 정령이 무리한 운동 대신 가벼운 산책과 휴식을 추천합니다."
            slumber_mode = True

        return {
            "recovery_score": final_rs,
            "status_title": status_title,
            "spirit_message": spirit_message,
            "slumber_mode_active": slumber_mode,
            "sleep_efficiency_pct": round(bed_time_efficiency, 1),
            "deep_sleep_ratio_pct": round(deep_ratio * 100, 1),
            "hrv_ms": round(hrv_ms, 1),
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_recovery() -> Dict[str, Any]:
        return {
            "recovery_score": 70.0,
            "status_title": "편안한 회복 모드 🌿",
            "spirit_message": "수면 기록을 차분히 기다리고 있어요. 오늘도 정령이 유저님의 편안한 하루를 응원합니다!",
            "slumber_mode_active": False,
            "sleep_efficiency_pct": 85.0,
            "deep_sleep_ratio_pct": 20.0,
            "hrv_ms": 55.0,
            "is_fallback": True
        }

if __name__ == "__main__":
    engine = RecoverySleepEngine()
    res = engine.calculate_recovery_index(
        total_sleep_min=450.0, deep_sleep_min=105.0, rem_sleep_min=90.0,
        hrv_ms=62.0, bed_time_efficiency=92.0
    )
    print(f"[Recovery Sleep Engine Output] {res}")