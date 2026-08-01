GAMEPLAY_LOOP_MASTER

Version: 1.0
Status: SSOT
Priority: Critical

───

목적

Health is All의 핵심 게임 루프를 정의한다.

본 문서는 게임 플레이의 단일 SSOT이다.

다른 문서에서는 본 문서를 참조하며,
동일 내용을 중복 정의하지 않는다.

───

핵심 철학

건강 행동이 게임을 시작한다.

게임은 건강 행동을 강화한다.

게임은 건강 행동을 대체하지 않는다.

Priority

Health
Habit
Emotion
Reward
Collection

───

Core Gameplay Loop

사용자 행동

↓

AI 분석

↓

건강이 반응

↓

즉시 피드백

↓

Exp 지급

↓

Point 지급

↓

Quest 진행

↓

Collection 진행

↓

건강이 성장

↓

새로운 목표 제안

↓

다음 행동 유도

───

Loop 1

식단

↓

AI 분석

↓

건강이 대사

↓

영양 피드백

↓

Exp

↓

Memory 생성

↓

다음 식사 제안

───

Loop 2

운동

↓

운동 완료

↓

건강이 응원

↓

Exp

↓

Combo 확인

↓

Quest 진행

↓

칭호 진행

↓

다음 운동 추천

───

Loop 3

수면

기상

↓

수면 분석

↓

건강이 컨디션 변화

↓

Recovery Bonus

↓

Exp

↓

오늘 목표 제안

───

Loop 4

Habit

Habit 완료

↓

Habit Chain

↓

Combo Bonus

↓

건강이 기분 상승

↓

Collection 증가

↓

다음 Habit 추천

───

Loop 5

Goal

Goal Progress

↓

Milestone

↓

건강이 이벤트

↓

Reward

↓

새 Goal 생성

───

사용자에게 보여야 하는 순서

사용자가 행동한다.

↓

건강이가 반응한다.

↓

보상이 나온다.

↓

숫자가 증가한다.

↓

다음 행동을 제안한다.

사용자는 숫자가 아니라

건강이의 반응을 먼저 본다.

───

절대 금지

운동

↓

Exp만 지급

식단

↓

Point만 지급

Quest

↓

보상만 지급

건강이 반응 없는 Reward

감정 없는 레벨업

───

Reward 우선순위

1

건강이 반응

2

Animation

3

Sound

4

Reward

5

Exp

6

Point

숫자는 가장 마지막이다.

───

Emotion Rule

모든 건강 행동은

반드시

건강이 감정

또는

표정

또는

대사

중 최소 하나를 발생시켜야 한다.

───

Daily Retention Rule

앱을 종료하기 전

사용자는

다음 행동 하나를 반드시 예약한다.

예

오늘 저녁 산책

내일 아침 물 마시기

점심 단백질 챙기기

예약 없는 종료는 지양한다.

───

Design Principle

건강 행동

↓

감정

↓

성취감

↓

보상

↓

성장

↓

다음 행동

이 순서는 절대 변경하지 않는다.

───

Related Documents

GAME_SYSTEM.md

QUEST_SYSTEM.md

REWARD_SYSTEM.md

HEALTH_AI.md

EMOTION_ENGINE.md

PLAYER_RETENTION.md