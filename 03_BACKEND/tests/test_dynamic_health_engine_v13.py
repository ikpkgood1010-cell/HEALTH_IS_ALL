"""
HEALTH IS ALL - Engine V13 Unit Tests
File Path: HEALTH IS ALL/03_BACKEND/tests/test_dynamic_health_engine_v13.py
"""

import pytest
from dynamic_health_engine_v13 import (
    DynamicHealthEngineV13,
    HealthInputData,
    CalculationMode
)

@pytest.fixture
def engine():
    return DynamicHealthEngineV13()

def test_dynamic_multi_mode_success(engine):
    """정상 파라미터 입력 시 다변수 동적 공식(DYNAMIC_MULTI) 연산 검증"""
    health_data = HealthInputData(
        steps=8500,
        burned_kcal=400.0,
        avg_hr=135.0,
        max_hr=180.0,
        circadian_factor=1.15,
        nutritive_synergy=1.20
    )
    
    result = engine.calculate_rewards(user_id="USR_TEST_01", health_data=health_data)
    
    # hr_ratio = 135/180 = 0.75
    # final_exp = 400 * (1 + 0.75) * 1.15 * 1.20 = 400 * 1.75 * 1.38 = 966
    assert result.calculation_mode == CalculationMode.DYNAMIC_MULTI
    assert result.exp_gained == 966
    assert result.spirit_affinity_delta > 0
    assert "lines_count" in result.health_tip

def test_fallback_simple_mode_on_missing_param(engine):
    """파라미터 누락 발생 시 2단계 Fallback(FALLBACK_SIMPLE) 자동 전환 검증"""
    health_data = HealthInputData(
        steps=5000,
        burned_kcal=250.0,
        avg_hr=120.0,
        max_hr=0.0, # max_hr 0으로 분모 예외 유발
        circadian_factor=None,
        nutritive_synergy=None
    )
    
    result = engine.calculate_rewards(user_id="USR_TEST_02", health_data=health_data)
    
    # Fallback 연산: 250.0 * 1.0 = 250 EXP
    assert result.calculation_mode == CalculationMode.FALLBACK_SIMPLE
    assert result.exp_gained == 250
    assert result.snack_reward_count == 1