# -*- coding: utf-8 -*-
"""
File Path: HEALTH IS ALL/03_BACKEND/health_system_logger_v1.py
Description:
    'HEALTH IS ALL' V1 실시간 성능 모니터링 및 KPI 측정 로거.
    HEALTH_MONITORING_SPEC_V1.mdux 규격을 준수하며, 비동기 메커니즘으로
    응답 지연 시간, Fallback 발생률, 푸시 성공률을 수집하고 분석합니다.
"""

import time
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealthSystemLoggerV1")

class HealthSystemLoggerV1:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "fallback_count": 0,
            "total_latency_ms": 0.0,
            "push_dispatched": 0,
            "push_failed": 0
        }

    def log_tip_request(self, latency_ms: float, mode: str) -> None:
        """
        팁 요청 성능 지표 수집 및 임계값 초과 여부 검사
        """
        self.metrics["total_requests"] += 1
        self.metrics["total_latency_ms"] += latency_ms

        if mode == "FALLBACK":
            self.metrics["fallback_count"] += 1
            logger.warning("[Metric Alert] Fallback 계산 모드가 감지되었습니다.")

        if latency_ms > 300.0:
            logger.warning(f"[Performance Alert] 지연 시간이 임계값을 초과했습니다: {latency_ms:.2f}ms")

    def get_kpi_report(self) -> Dict[str, Any]:
        """
        현재 시스템 KPI 집계 및 종합 상태 판정
        """
        total = self.metrics["total_requests"]
        if total == 0:
            return {"status": "NO_DATA"}

        avg_latency = self.metrics["total_latency_ms"] / total
        fallback_rate = (self.metrics["fallback_count"] / total) * 100.0

        # 상태 판정 규칙 적용
        health_status = "HEALTHY"
        if fallback_rate >= 5.0 or avg_latency > 300.0:
            health_status = "WARNING"

        return {
            "total_requests": total,
            "avg_latency_ms": round(avg_latency, 2),
            "fallback_rate_pct": round(fallback_rate, 2),
            "health_status": health_status
        }

if __name__ == "__main__":
    sys_logger = HealthSystemLoggerV1()

    # 모니터링 데이터 측정 시뮬레이션
    sys_logger.log_tip_request(45.2, "PRECISION")
    sys_logger.log_tip_request(62.1, "PRECISION")
    sys_logger.log_tip_request(310.5, "FALLBACK")

    report = sys_logger.get_kpi_report()
    print("\n=== [실시간 시스템 KPI 리포트] ===")
    print(f"총 요청 수: {report['total_requests']}")
    print(f"평균 지연 시간: {report['avg_latency_ms']} ms")
    print(f"Fallback 비율: {report['fallback_rate_pct']} %")
    print(f"시스템 판정 상태: {report['health_status']}")