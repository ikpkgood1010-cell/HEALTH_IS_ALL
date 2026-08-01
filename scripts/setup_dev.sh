#!/bin/bash
# 개발 환경 자동 구축 스크립트

echo "1. Python 가상환경을 생성합니다..."
python3 -m venv venv
source venv/bin/activate

echo "2. 백엔드 필요 패키지를 설치합니다..."
pip install --upgrade pip
pip install -r requirements.txt

echo "3. Flutter 패키지를 설치합니다..."
flutter pub get

echo "개발 환경 구축이 완료되었습니다!"