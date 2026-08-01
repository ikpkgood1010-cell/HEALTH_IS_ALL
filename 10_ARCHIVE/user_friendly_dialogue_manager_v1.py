"""
HEALTH IS ALL - User Friendly Dialogue Manager V1
이용자 친화적이고 공감대 형성을 위한 정령 팝업 및 대화 메시지 생성 모듈
"""

import random
from typing import Dict, Any

class UserFriendlyDialogueManagerV1:
    """사용자의 건강 행동에 따라 호감형 3줄 피드백 대화를 생성하는 클래스"""

    def __init__(self):
        self.version = "1.0.0"

    def generate_feedback_dialogue(
        self,
        activity_type: str,
        score: float,
        user_name: str = "건강 대장"
    ) -> Dict[str, str]:
        """
        활동 유형과 성과에 맞춘 친근한 대화 문구 생성 (최대 3줄)
        """
        if activity_type == "EXERCISE":
            if score >= 300:
                lines = [
                    f"오늘 정말 대단해요, {user_name}님!",
                    "열심히 활동하신 덕분에 저도 한층 더 건강해진 기분이에요.",
                    "충분한 수분 섭취와 휴식도 잊지 말고 챙겨주세요!"
                ]
            else:
                lines = [
                    f"차근차근 잘 해내고 계시네요, {user_name}님!",
                    "작은 움직임들이 모여 큰 변화를 만든답니다.",
                    "오늘도 함께할 수 있어서 정말 기뻐요!"
                ]
        elif activity_type == "DIET":
            if score >= 40:
                lines = [
                    "정말 건강하고 깔끔한 식단이에요!",
                    "몸도 마음도 가벼워지는 완벽한 영양 조합이네요.",
                    "다음 식사도 이렇게 즐겁게 준비해 볼까요?"
                ]
            else:
                lines = [
                    "오늘 한 끼도 정성껏 챙겨주셨네요!",
                    "자당이나 기름진 음식 대신 정갈한 음식을 선택해 보세요.",
                    "작은 습관 변화가 더 건강한 내일을 만든답니다!"
                ]
        else:
            lines = [
                f"오늘 하루도 정말 수고 많으셨어요, {user_name}님!",
                "규칙적인 수면과 건강한 습관이 최고의 보약이에요.",
                "내일도 정령이 곁에서 든든하게 응원할게요!"
            ]

        return {
            "title": "동반자 정령의 한마디",
            "message": "\n".join(lines),
            "line_1": lines[0],
            "line_2": lines[1],
            "line_3": lines[2]
        }

if __name__ == "__main__":
    manager = UserFriendlyDialogueManagerV1()
    feedback = manager.generate_feedback_dialogue("EXERCISE", 450.0)
    print("생성된 피드백 대화:\n", feedback["message"])