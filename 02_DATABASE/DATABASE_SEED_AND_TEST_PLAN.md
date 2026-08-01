Database Seed & Test Plan (DB 시드 데이터 및 통합 테스트 계획서)

1. 개요
본 문서는 HEALTH IS ALL 프로젝트의 데이터베이스 초기 구축을 위한 마스터 시드 데이터(Master Seed Data) 명세와, 시스템 주요 파이프라인의 안정성을 검증하기 위한 통합 테스트 계획(Integration Test Plan) 을 정립합니다. 본 개발 환경(Dev) 및 테스트 환경(Staging)에서 일관된 테스트 재현성을 확보하는 것을 목적으로 합니다.

───

2. 마스터 시드 데이터 명세 (Master Seed Data SQL)

2.1. 운동 마스터 데이터 (exercise_masters)
• 목적: METs 기반 소모 칼로리 및 기본 보상 산출 기준 데이터

sql
INSERT INTO exercise_masters (code, name, met_value, category, default_duration_min) VALUES
('RUNNING_OUTDOOR', '야외 조깅', 8.0, 'CARDIO', 30),
('WALKING_CASUAL', '가벼운 산책', 3.5, 'CARDIO', 20),
('STRENGTH_TRAINING', '웨이트 트레이닝', 6.0, 'ANAEROBIC', 45),
('YOGA_STRETCHING', '요가 및 스트레칭', 2.5, 'FLEXIBILITY', 30),
('CYCLING_MODERATE', '실외 자전거', 6.8, 'CARDIO', 30);