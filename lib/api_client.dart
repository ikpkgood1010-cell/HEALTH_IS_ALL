import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_config.dart';

/// HEALTH IS ALL - Backend REST API Client
///
/// backend/main.py 의 실제 엔드포인트/요청·응답 스키마(backend/models.py)와
/// 정확히 일치하도록 작성되었다. 엔드포인트나 필드가 백엔드에서 바뀌면
/// 이 파일만 함께 수정하면 된다 (앱의 다른 코드는 ApiDataProvider를 통해서만
/// 이 클라이언트를 사용하므로 변경 영향 범위가 좁다).
class HealthIApiClient {
  /// 백엔드 서버 주소.
  /// baseUrl을 명시적으로 넘기지 않으면 api_config.dart가 플랫폼별로
  /// 자동 결정한다 (웹: 접속 origin, Android: 10.0.2.2, 그 외: localhost).
  /// --dart-define=API_BASE_URL=... 로 언제든 오버라이드 가능하다.
  final String baseUrl;
  final http.Client _client;

  HealthIApiClient({String? baseUrl, http.Client? client})
      : baseUrl = baseUrl ?? resolveApiBaseUrl(),
        _client = client ?? http.Client();

  /// POST /api/v1/health/record
  /// 식사/운동/수분/습관 등 모든 활동 기록에 사용하는 단일 엔드포인트.
  /// record_type 예: 'meal_log', 'workout_log', 'water_log', 'habit_complete'
  Future<HealthRecordResult> logHealthActivity({
    required String userId,
    required String recordType,
    required double value,
    Map<String, dynamic>? detailData,
  }) async {
    final uri = Uri.parse('$baseUrl/api/v1/health/record');
    final response = await _client
        .post(
          uri,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'user_id': userId,
            'record_type': recordType,
            'value': value,
            if (detailData != null) 'detail_data': detailData,
          }),
        )
        .timeout(const Duration(seconds: 10));

    if (response.statusCode != 200) {
      throw HealthIApiException(
        '기록 저장 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }

    final json = jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    return HealthRecordResult.fromJson(json);
  }

  /// GET /api/v1/health-i/status/{user_id}
  Future<HealthIStatus> fetchHealthIStatus(String userId) async {
    final uri = Uri.parse('$baseUrl/api/v1/health-i/status/$userId');
    final response = await _client.get(uri).timeout(const Duration(seconds: 10));

    if (response.statusCode != 200) {
      throw HealthIApiException(
        '상태 조회 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }

    final json = jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    return HealthIStatus.fromJson(json);
  }

  void dispose() {
    _client.close();
  }
}

/// backend/models.py: HealthRecordResponse 와 1:1 대응
class HealthRecordResult {
  final bool success;
  final String recordId;
  final int expGained;
  final int currentDailyExp;
  final String message;

  HealthRecordResult({
    required this.success,
    required this.recordId,
    required this.expGained,
    required this.currentDailyExp,
    required this.message,
  });

  factory HealthRecordResult.fromJson(Map<String, dynamic> json) {
    return HealthRecordResult(
      success: json['success'] as bool? ?? false,
      recordId: json['record_id'] as String? ?? '',
      expGained: (json['exp_gained'] as num?)?.toInt() ?? 0,
      currentDailyExp: (json['current_daily_exp'] as num?)?.toInt() ?? 0,
      message: json['message'] as String? ?? '',
    );
  }
}

/// backend/models.py: HealthIStateResponse 와 1:1 대응
class HealthIStatus {
  final String name;
  final int level;
  final int currentExp;
  final int dailyExpCap;
  final String emotionState;
  final String dialogue;
  final String equippedSkin;
  final DateTime lastUpdated;
  final double todayConsumedCalories;
  final double todayWorkoutMinutes;
  final double todayWaterLiters;
  final int streakDays;

  HealthIStatus({
    required this.name,
    required this.level,
    required this.currentExp,
    required this.dailyExpCap,
    required this.emotionState,
    required this.dialogue,
    required this.equippedSkin,
    required this.lastUpdated,
    required this.todayConsumedCalories,
    required this.todayWorkoutMinutes,
    required this.todayWaterLiters,
    required this.streakDays,
  });

  factory HealthIStatus.fromJson(Map<String, dynamic> json) {
    return HealthIStatus(
      name: json['name'] as String? ?? '건강이',
      level: (json['level'] as num?)?.toInt() ?? 1,
      currentExp: (json['current_exp'] as num?)?.toInt() ?? 0,
      dailyExpCap: (json['daily_exp_cap'] as num?)?.toInt() ?? 300,
      emotionState: json['emotion_state'] as String? ?? '평온함',
      dialogue: json['dialogue'] as String? ?? '',
      equippedSkin: json['equipped_skin'] as String? ?? 'default_skin',
      lastUpdated: DateTime.tryParse(json['last_updated'] as String? ?? '') ?? DateTime.now(),
      todayConsumedCalories: (json['today_consumed_calories'] as num?)?.toDouble() ?? 0.0,
      todayWorkoutMinutes: (json['today_workout_minutes'] as num?)?.toDouble() ?? 0.0,
      todayWaterLiters: (json['today_water_liters'] as num?)?.toDouble() ?? 0.0,
      streakDays: (json['streak_days'] as num?)?.toInt() ?? 0,
    );
  }
}

class HealthIApiException implements Exception {
  final String message;
  final int? statusCode;
  HealthIApiException(this.message, {this.statusCode});

  @override
  String toString() => 'HealthIApiException: $message';
}
