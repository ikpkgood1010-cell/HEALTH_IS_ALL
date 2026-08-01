"""
HEALTH IS ALL - Monthly Health Report Engine
Filename: monthly_report_engine.py
Path: HEALTH IS ALL/backend/monthly_report_engine.py
Purpose: 30일간의 영양, 운동, 수분 데이터를 정밀 분석하여 월간 건강 개선 지수(MHII) 및 다정한 힐링 총평을 도출하는 백엔드 엔진
"""

import random
from typing import Dict, Any, List

class MonthlyReportEngine:
    """
    월간 건강 리포트 산출 및 데이터 시각화 지원 엔진
    """

    @staticmethod
    def generate_monthly_report(
        daily_logs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        30일간의 일일 로그를 종합 분석하여 MHII 지수 및 정령 총평 도출
        """
        if not daily_logs or len(daily_logs) < 3:
            return MonthlyReportEngine._build_fallback_report()

        jitter = random.uniform(0.97, 1.03)

        total_steps = sum(log.get("steps", 0) for log in daily_logs)
        total_nutri = sum(log.get("nutri_score", 70.0) for log in daily_logs)
        total_water = sum(log.get("water_ml", 1500) for log in daily_logs)
        days_count = len(daily_logs)

        avg_steps = total_steps / days_count
        avg_nutri = total_nutri / days_count
        avg_water = total_water / days_count

        # 월간 건강 개선 지수 (MHII) 계산 수식
        raw_mhii = (
            (min(12000, avg_steps) / 10000.0) * 35.0 +
            (min(100.0, avg_nutri) * 0.45) +
            (min(2500, avg_water) / 2000.0) * 20.0
        )
        mhii_score = round(min(100.0, max(0.0, raw_mhii * jitter)), 1)

        # 다정한 어조의 정령 총평 메시지 도출
        if mhii_score >= 85.0:
            spirit_comment = (
                f"이번 달은 정말 눈부신 한 달이었어요! 평균 {int(avg_steps):,}보를 걸으시며 "
                f"수호 정령의 신비로운 정원을 푸르게 피워내셨습니다 ✨"
            )
            badge_name = "🌟 푸른 정원의 수호자"
        elif mhii_score >= 65.0:
            spirit_comment = (
                f"꾸준히 몸을 돌봐주신 덕분에 정령이 한층 더 튼튼해졌어요. "
                f"평균 {int(avg_steps):,}보의 걸음이 정령에게 따뜻한 온기를 전했습니다 🌿"
            )
            badge_name = "🌿 따스한 온기의 든든한 동반자"
        else:
            spirit_comment = (
                f"바쁜 일상 속에서도 소중하게 건강을 챙겨주셔서 고마워요. "
                f"다음 달에도 정령과 함께 차근차근 걸어가 봐요 💕"
            )
            badge_name = "🌱 씨앗을 품은 희망의 탐험가"

        return {
            "days_recorded": days_count,
            "avg_daily_steps": int(avg_steps),
            "avg_nutri_score": round(avg_nutri, 1),
            "avg_water_ml": int(avg_water),
            "mhii_score": mhii_score,
            "badge_name": badge_name,
            "spirit_comment": spirit_comment,
            "is_fallback": False
        }

    @staticmethod
    def _build_fallback_report() -> Dict[str, Any]:
        return {
            "days_recorded": 0,
            "avg_daily_steps": 7500,
            "avg_nutri_score": 80.0,
            "avg_water_ml": 1600,
            "mhii_score": 78.5,
            "badge_name": "🌱 씨앗을 품은 희망의 탐험가",
            "spirit_comment": "소중한 기록들이 차곡차곡 모이고 있어요. 수호 정령이 곁에서 언제나 응원할게요 🌿",
            "is_fallback": True
        }

if __name__ == "__main__":
    engine = MonthlyReportEngine()
    mock_logs = [
        {"steps": 8500, "nutri_score": 88.0, "water_ml": 1800} for _ in range(30)
    ]
    res = engine.generate_monthly_report(mock_logs)
    print(f"[Monthly Report Engine Output] {res}")