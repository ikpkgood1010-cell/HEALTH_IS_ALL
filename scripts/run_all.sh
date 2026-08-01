#!/bin/bash
# 전체 시스템 실행 스크립트

echo "1. 백엔드 API 서버를 시작합니다..."
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &

echo "2. Flutter 클라이언트를 웹 모드로 실행합니다..."
flutter run -d chrome