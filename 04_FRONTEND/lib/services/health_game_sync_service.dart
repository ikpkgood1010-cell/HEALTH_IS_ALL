import 'dart:convert';
import 'package:flutter/foundation.dart';

enum CalculationMode { DYNAMIC_MULTI, FALLBACK_SIMPLE }

class DualBalanceRewardModel {
  final CalculationMode mode;
  final int expGained;
  final int spiritAffinityDelta;
  final int snackRewardCount;
  final String healthTipMessage;

  DualBalanceRewardModel({
    required this.mode,
    required this.expGained,
    required this.spiritAffinityDelta,
    required this.snackRewardCount,
    required this.healthTipMessage,
  });

  factory DualBalanceRewardModel.fromJson(Map<String, dynamic> json) {
    return DualBalanceRewardModel(
      mode: json['calculation_mode'] == 'DYNAMIC_MULTI'
          ? CalculationMode.DYNAMIC_MULTI
          : CalculationMode.FALLBACK_SIMPLE,
      expGained: json['game_output']['exp_gained'] ?? 0,
      spiritAffinityDelta: json['game_output']['spirit_affinity_delta'] ?? 0,
      snackRewardCount: json['game_output']['snack_reward_count'] ?? 0,
      healthTipMessage: json['health_tip']['message'] ?? '',
    );
  }
}

class HealthGameSyncService extends ChangeNotifier {
  DualBalanceRewardModel? _lastReward;
  bool _isProcessing = false;

  DualBalanceRewardModel? get lastReward => _lastReward;
  bool get isProcessing => _isProcessing;

  /// 연산 서버 API 응답을 수신하여 UI 상태 갱신
  void handleRewardResponse(Map<String, dynamic> jsonResponse) {
    _isProcessing = true;
    notifyListeners();

    try {
      _lastReward = DualBalanceRewardModel.fromJson(jsonResponse['payload']);
      if (_lastReward?.mode == CalculationMode.FALLBACK_SIMPLE) {
        debugPrint('[DualBalance] Fallback 모드로 연산된 보상이 적용되었습니다.');
      }
    } catch (e) {
      debugPrint('[DualBalance] 응답 파싱 에러: $e');
    } finally {
      _isProcessing = false;
      notifyListeners();
    }
  }
}