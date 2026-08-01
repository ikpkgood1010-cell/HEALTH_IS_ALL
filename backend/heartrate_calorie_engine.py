"""
HEALTH IS ALL - Real-time Wearable Heart Rate & Dynamic Calorie Engine
Filename: heartrate_calorie_engine.py
Path: HEALTH IS ALL/backend/heartrate_calorie_engine.py
Purpose: 웨어러블 심박수 데이터 기반 HR Zone, Keytel 칼로리, EPOC 및 정령 아우라 계산 백엔드 엔진
"""

import math
import random
from typing import Dict, Any, Optional

class HeartRateCalorieEngine:
    """
    실시간 심박수 분석 및 dynamic 칼로리/정령 버프 산출 엔진
    """

    @staticmethod
    def calculate_max_hr(age: int) -> float:
        """
        Tanaka 공식을 이용한 최대 심박수 산출
        """
        safe_age = max(10, min(100, age))
        return 208.0 - (0.7 * safe_age)

    @staticmethod
    def determine_hr_zone(current_bpm: float, max_hr: float) -> Dict[str, Any]:
        """
        현재 심박수 비율에 따른 HR Zone 및 정령 아우라 상태 결정
        """
        hr_ratio = current_bpm / max_hr if max_hr > 0 else 0.0

        if hr_ratio >= 0.90:
            zone = 5
            zone_name = "극한 (Extreme)"
            aura_state = "OVERHEAT" if hr_ratio >= 0.95 else "ANAEROBIC_AURA"
            buff_multiplier = 2.0
        elif hr_ratio >= 0.80:
            zone = 4
            zone_name = "무산소 (Anaerobic)"
            aura_state = "ANAEROBIC_AURA"
            buff_multiplier = 1.6
        elif hr_ratio >= 0.70:
            zone = 3
            zone_name = "유산소 (Aerobic)"
            aura_state = "AEROBIC_AURA"
            buff_multiplier = 1.3
        elif hr_ratio >= 0.60:
            zone = 2
            zone_name = "지방 연소 (Fat Burn)"
            aura_state = "FAT_BURN_AURA"
            buff_multiplier = 1.1
        elif hr_ratio >= 0.50:
            zone = 1
            zone_name = "웜업 (Warm-up)"
            aura_state = "WARMUP_AURA"
            buff_multiplier = 1.0
        else:
            zone = 0
            zone_name = "휴식 (Rest)"
            aura_state = "IDLE"
            buff_multiplier = 1.0

        return {
            "zone": zone,
            "zone_name": zone_name,
            "hr_percentage": round(hr_ratio * 100, 1),
            "aura_state": aura_state,
            "buff_multiplier": buff_multiplier
        }

    @staticmethod
    def calculate_dynamic_burn(
        age: int,
        weight_kg: float,
        gender: str,
        current_bpm: float,
        duration_minutes: float,
        zone4_minutes: float = 0.0,
        zone5_minutes: float = 0.0,
        is_sensor_connected: bool = True,
        mets_fallback: float = 6.0
    ) -> Dict[str, Any]:
        """
        Keytel 다변수 칼로리 수식 및 EPOC 보너스 계산 (센서 유실 시 Fallback 자동 전환)
        """
        # 이상값 보정 (Exception handling)
        if current_bpm < 30 or current_bpm > 230:
            current_bpm = 120.0  # 직전 안정이상치 대치

        max_hr = HeartRateCalorieEngine.calculate_max_hr(age)
        zone_info = HeartRateCalorieEngine.determine_hr_zone(current_bpm, max_hr)

        if is_sensor_connected and duration_minutes > 0:
            # 1. Keytel 정밀 수식 적용
            time_hours = duration_minutes / 60.0
            if gender.upper() == "MALE" or gender.upper() == "M":
                cal_per_min = ((-55.0969 + (0.6309 * current_bpm) + (0.1988 * weight_kg) + (0.2017 * age)) / 4.184)
            else:
                cal_per_min = ((-20.4022 + (0.4472 * current_bpm) - (0.1263 * weight_kg) + (0.074 * age)) / 4.184)

            cal_per_min = max(1.0, cal_per_min)
            base_calories = cal_per_min * duration_minutes

            # 2. EPOC 보너스 산출 (고강도 운동 후 추가 산소 소비)
            epoc_bonus = (zone4_minutes * 1.8) + (zone5_minutes * 3.2)

            # 3. 미세 난수 인자 적용 (0.95 ~ 1.05)
            jitter = random.uniform(0.95, 1.05)
            total_burned = (base_calories + epoc_bonus) * jitter
            is_fallback = False
        else:
            # 4. Fallback 수식 (METs 기반 간이 계산)
            # Calories = METs * Weight(kg) * (Duration_min / 60)
            total_burned = mets_fallback * weight_kg * (duration_minutes / 60.0)
            epoc_bonus = 0.0
            is_fallback = True

        # 정령 버프 에너지 환산
        spirit_energy_gained = int(total_burned * zone_info["buff_multiplier"] * 0.5)

        return {
            "total_calories_burned": round(total_burned, 1),
            "epoc_bonus_calories": round(epoc_bonus, 1),
            "hr_zone": zone_info["zone"],
            "hr_zone_name": zone_info["zone_name"],
            "aura_state": zone_info["aura_state"],
            "spirit_energy_gained": spirit_energy_gained,
            "is_fallback_used": is_fallback,
            "safety_warning": zone_info["aura_state"] == "OVERHEAT"
        }

if __name__ == "__main__":
    engine = HeartRateCalorieEngine()
    res = engine.calculate_dynamic_burn(
        age=30, weight_kg=75.0, gender="MALE", current_bpm=165.0,
        duration_minutes=45.0, zone4_minutes=15.0, zone5_minutes=5.0
    )
    print(f"[HeartRate Burn Calculation] {res}")