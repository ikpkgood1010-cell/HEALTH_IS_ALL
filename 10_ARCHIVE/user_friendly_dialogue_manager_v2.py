# 파일 경로: HEALTH IS ALL/05_AI/user_friendly_dialogue_manager_v2.py
# 파일명: user_friendly_dialogue_manager_v2.py
# 설명: 호감형 대화 및 1~3줄 건강 꿀팁 생성 매니저 v2

import random
from typing import Dict, Any

class UserFriendlyDialogueManagerV2:
    """
    HEALTH IS ALL - Dialogue & Popup Manager Engine v2
    사용자에게 호감적이고 친근한 피드백 대화와
    1~3줄 분량의 실용적인 건강/식단 꿀팁을 생성합니다.
    """

    def __init__(self):
        self.version = "2.0.0"
        
        # 1~3줄 분량의 핵심 건강/식단/운동 꿀팁 데이터베이스
        self.health_tips = [
            "💡 **오늘의 꿀팁**: 식사 시 채소 -> 단백질 -> 탄수화물 순서로 드시면 혈당 스파이크를 효과적으로 막을 수 있어요!",
            "💡 **오늘의 꿀팁**: 정제 설탕이나 밀가루 대신 천연 대체당이나 스팀 요리를 활용하면 몸의 부기를 쏙 빼줍니다.",
            "💡 **오늘의 꿀팁**: 30분 정도의 가벼운 산책만으로도 뇌내 엔도르핀이 분비되어 하루 스트레스의 40% 이상이 해소돼요!",
            "💡 **오늘의 꿀팁**: 세차나 집안일 같은 고강도 활동도 훌륭한 전신 유산소 운동입니다. 오늘 소비한 칼로리를 확인해보세요!",
            "💡 **오늘의 꿀팁**: 수면 전 1시간 동안 스마트폰 대신 따뜻한 차 한 잔을 마시면 깊은 수면(Rem Sleep) 도달 시간이 20분 단축됩니다."
        ]

        self.praise_messages = [
            "정말 대단해요! 꾸준히 실천하는 모습이 너무 멋집니다! ✨",
            "오늘도 자신과의 약속을 멋지게 지켜내셨군요! 정령도 함께 기뻐하고 있어요! 🌿",
            "와우! 건강한 선택을 하셨네요. 차곡차곡 쌓인 노력이 곧 빛을 발할 거예요! 🏆"
        ]

    def generate_friendly_dialogue(
        self, 
        event_type: str, 
        user_name: str = "회원"
    ) -> Dict[str, Any]:
        """
        상황별 호감형 대화 팝업 데이터 생성
        """
        praise = random.choice(self.praise_messages)
        tip = random.choice(self.health_tips)

        if event_type == "MEAL_LOGGED":
            main_msg = f"오늘 식단 기록 완료! {user_name}님의 건강한 식습관이 정령의 활력을 키워주었어요."
            spirit_emotion = "HAPPY"
        elif event_type == "EXERCISE_COMPLETED":
            main_msg = f"오늘 운동 목표 달성! {user_name}님의 열정 덕분에 오늘 던전 탐험도 대성공입니다!"
            spirit_emotion = "PASSIONATE"
        else:
            main_msg = f"안녕하세요 {user_name}님! 오늘도 활기차고 건강한 하루를 시작해볼까요?"
            spirit_emotion = "NORMAL"

        return {
            "title": "정령의 건강 메세지 💌",
            "main_message": main_msg,
            "praise_message": praise,
            "micro_tip": tip,
            "spirit_emotion": spirit_emotion,
            "auto_wrap": True
        }

if __name__ == "__main__":
    manager = UserFriendlyDialogueManagerV2()
    dialogue = manager.generate_friendly_dialogue("MEAL_LOGGED", "플레이어")
    print("Generated Dialogue:", dialogue)