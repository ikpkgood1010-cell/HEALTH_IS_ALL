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
    required String idempotencyKey,
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
            'idempotency_key': idempotencyKey,
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

    final json =
        jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    return HealthRecordResult.fromJson(json);
  }

  /// GET /api/v1/health-i/status/{user_id}
  Future<HealthIStatus> fetchHealthIStatus(String userId) async {
    final uri = Uri.parse('$baseUrl/api/v1/health-i/status/$userId');
    final response =
        await _client.get(uri).timeout(const Duration(seconds: 10));

    if (response.statusCode != 200) {
      throw HealthIApiException(
        '상태 조회 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }

    final json =
        jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    return HealthIStatus.fromJson(json);
  }

  /// Settles or returns the current 12-hour automatic adventure.
  Future<AdventureState> settleAdventure(String userId) async {
    final uri = Uri.parse('$baseUrl/api/v1/game/adventures/settle');
    final response = await _client
        .post(
          uri,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'user_id': userId}),
        )
        .timeout(const Duration(seconds: 10));
    if (response.statusCode != 200) {
      throw HealthIApiException(
        '자동 모험 정산 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }
    return AdventureState.fromJson(
      jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>,
    );
  }

  /// Claims one adventure. The server safely returns the original claim on retry.
  Future<AdventureClaimResult> claimAdventure({
    required String userId,
    required String adventureId,
  }) async {
    final uri = Uri.parse(
      '$baseUrl/api/v1/game/adventures/$adventureId/claim',
    );
    final response = await _client
        .post(
          uri,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'user_id': userId}),
        )
        .timeout(const Duration(seconds: 10));
    if (response.statusCode != 200) {
      throw HealthIApiException(
        '모험 보상 수령 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }
    return AdventureClaimResult.fromJson(
      jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>,
    );
  }

  Future<TrainingGroundsStatus> fetchTrainingGrounds(String userId) async {
    final uri = Uri.parse(
      '$baseUrl/api/v1/game/facilities/training-grounds/$userId',
    );
    final response =
        await _client.get(uri).timeout(const Duration(seconds: 10));
    if (response.statusCode != 200) {
      throw HealthIApiException(
        '훈련장 조회 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }
    return TrainingGroundsStatus.fromJson(
      jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>,
    );
  }

  /// Returns story-earned heroes. Reading the roster never unlocks a hero.
  Future<List<HeroCompanion>> fetchHeroRoster(String userId) async {
    final uri = Uri.parse('$baseUrl/api/v1/game/heroes/$userId');
    final response =
        await _client.get(uri).timeout(const Duration(seconds: 10));
    if (response.statusCode != 200) {
      throw HealthIApiException(
        '모험대 조회 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }
    final json =
        jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    return (json['items'] as List<dynamic>? ?? const [])
        .whereType<Map<String, dynamic>>()
        .map(HeroCompanion.fromJson)
        .toList(growable: false);
  }

  /// Returns saved adventures only. This endpoint never settles or rewards.
  Future<List<AdventureState>> fetchAdventureHistory(
    String userId, {
    int limit = 5,
  }) async {
    final uri = Uri.parse(
      '$baseUrl/api/v1/game/adventures/history/$userId?limit=$limit',
    );
    final response =
        await _client.get(uri).timeout(const Duration(seconds: 10));
    if (response.statusCode != 200) {
      throw HealthIApiException(
        '모험 회상 조회 실패 (status: ${response.statusCode})',
        statusCode: response.statusCode,
      );
    }
    final json =
        jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
    return (json['items'] as List<dynamic>? ?? const [])
        .whereType<Map<String, dynamic>>()
        .map(AdventureState.fromJson)
        .toList(growable: false);
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
  final bool duplicate;

  HealthRecordResult({
    required this.success,
    required this.recordId,
    required this.expGained,
    required this.currentDailyExp,
    required this.message,
    required this.duplicate,
  });

  factory HealthRecordResult.fromJson(Map<String, dynamic> json) {
    return HealthRecordResult(
      success: json['success'] as bool? ?? false,
      recordId: json['record_id'] as String? ?? '',
      expGained: (json['exp_gained'] as num?)?.toInt() ?? 0,
      currentDailyExp: (json['current_daily_exp'] as num?)?.toInt() ?? 0,
      message: json['message'] as String? ?? '',
      duplicate: json['duplicate'] as bool? ?? false,
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
      lastUpdated: DateTime.tryParse(json['last_updated'] as String? ?? '') ??
          DateTime.now(),
      todayConsumedCalories:
          (json['today_consumed_calories'] as num?)?.toDouble() ?? 0.0,
      todayWorkoutMinutes:
          (json['today_workout_minutes'] as num?)?.toDouble() ?? 0.0,
      todayWaterLiters: (json['today_water_liters'] as num?)?.toDouble() ?? 0.0,
      streakDays: (json['streak_days'] as num?)?.toInt() ?? 0,
    );
  }
}

class AdventureRoom {
  final int position;
  final String roomType;
  final String title;
  final String resultCode;
  final String resultTitle;
  final String outcome;

  const AdventureRoom({
    required this.position,
    required this.roomType,
    required this.title,
    required this.resultCode,
    required this.resultTitle,
    required this.outcome,
  });

  factory AdventureRoom.fromJson(Map<String, dynamic> json) => AdventureRoom(
        position: (json['position'] as num?)?.toInt() ?? 0,
        roomType: json['room_type'] as String? ?? 'COMBAT',
        title: json['title'] as String? ?? '모험 경로',
        resultCode: json['result_code'] as String? ?? 'STORY_RESULT',
        resultTitle: json['result_title'] as String? ?? '모험 기록',
        outcome: json['outcome'] as String? ?? '',
      );
}

class HeroCompanion {
  final String heroCode;
  final String name;
  final String title;
  final String role;
  final String element;
  final String joinMessage;
  final String gameplayEffect;
  final DateTime joinedAt;

  const HeroCompanion({
    required this.heroCode,
    required this.name,
    required this.title,
    required this.role,
    required this.element,
    required this.joinMessage,
    required this.gameplayEffect,
    required this.joinedAt,
  });

  factory HeroCompanion.fromJson(Map<String, dynamic> json) => HeroCompanion(
        heroCode: json['hero_code'] as String? ?? '',
        name: json['name'] as String? ?? '이름 없는 용사',
        title: json['title'] as String? ?? '길드 동료',
        role: json['role'] as String? ?? '탐험 용사',
        element: json['element'] as String? ?? 'FOREST',
        joinMessage: json['join_message'] as String? ?? '',
        gameplayEffect: json['gameplay_effect'] as String? ?? 'NONE',
        joinedAt: DateTime.tryParse(json['joined_at'] as String? ?? '') ??
            DateTime.fromMillisecondsSinceEpoch(0),
      );
}

class AdventureState {
  final String adventureId;
  final DateTime windowStart;
  final DateTime windowEnd;
  final int vitality;
  final int grossGuildCoins;
  final double offlineEfficiency;
  final double hbiScore;
  final int towerFloor;
  final List<AdventureRoom> rooms;
  final bool claimed;

  const AdventureState({
    required this.adventureId,
    required this.windowStart,
    required this.windowEnd,
    required this.vitality,
    required this.grossGuildCoins,
    required this.offlineEfficiency,
    required this.hbiScore,
    required this.towerFloor,
    required this.rooms,
    required this.claimed,
  });

  factory AdventureState.fromJson(Map<String, dynamic> json) {
    return AdventureState(
      adventureId: json['adventure_id'] as String? ?? '',
      windowStart: DateTime.parse(json['window_start'] as String),
      windowEnd: DateTime.parse(json['window_end'] as String),
      vitality: (json['vitality'] as num?)?.toInt() ?? 0,
      grossGuildCoins: (json['gross_guild_coins'] as num?)?.toInt() ?? 0,
      offlineEfficiency: (json['offline_efficiency'] as num?)?.toDouble() ?? .7,
      hbiScore: (json['hbi_score'] as num?)?.toDouble() ?? 0,
      towerFloor: (json['tower_floor'] as num?)?.toInt() ?? 1,
      rooms: (json['rooms'] as List<dynamic>? ?? const [])
          .whereType<Map<String, dynamic>>()
          .map(AdventureRoom.fromJson)
          .toList(growable: false),
      claimed: json['claimed'] as bool? ?? false,
    );
  }

  AdventureState copyWith({bool? claimed}) => AdventureState(
        adventureId: adventureId,
        windowStart: windowStart,
        windowEnd: windowEnd,
        vitality: vitality,
        grossGuildCoins: grossGuildCoins,
        offlineEfficiency: offlineEfficiency,
        hbiScore: hbiScore,
        towerFloor: towerFloor,
        rooms: rooms,
        claimed: claimed ?? this.claimed,
      );
}

class AdventureClaimResult {
  final String adventureId;
  final String claimId;
  final bool alreadyClaimed;
  final int grossGuildCoins;
  final int facilityInvested;
  final int guildCoinsReceived;
  final HeroCompanion? joinedHero;

  const AdventureClaimResult({
    required this.adventureId,
    required this.claimId,
    required this.alreadyClaimed,
    required this.grossGuildCoins,
    required this.facilityInvested,
    required this.guildCoinsReceived,
    required this.joinedHero,
  });

  factory AdventureClaimResult.fromJson(Map<String, dynamic> json) {
    return AdventureClaimResult(
      adventureId: json['adventure_id'] as String? ?? '',
      claimId: json['claim_id'] as String? ?? '',
      alreadyClaimed: json['already_claimed'] as bool? ?? false,
      grossGuildCoins: (json['gross_guild_coins'] as num?)?.toInt() ?? 0,
      facilityInvested: (json['facility_invested'] as num?)?.toInt() ?? 0,
      guildCoinsReceived: (json['guild_coins_received'] as num?)?.toInt() ?? 0,
      joinedHero: json['joined_hero'] is Map<String, dynamic>
          ? HeroCompanion.fromJson(
              json['joined_hero'] as Map<String, dynamic>,
            )
          : null,
    );
  }
}

class TrainingGroundsStatus {
  final int level;
  final int totalInvested;
  final int currentLevelProgress;
  final int nextLevelCost;
  final double progressRatio;
  final int guildCoinBalance;
  final String description;
  final String stageCode;
  final String stageName;
  final String stageMessage;
  final int? nextMilestoneLevel;

  const TrainingGroundsStatus({
    required this.level,
    required this.totalInvested,
    required this.currentLevelProgress,
    required this.nextLevelCost,
    required this.progressRatio,
    required this.guildCoinBalance,
    required this.description,
    required this.stageCode,
    required this.stageName,
    required this.stageMessage,
    required this.nextMilestoneLevel,
  });

  factory TrainingGroundsStatus.fromJson(Map<String, dynamic> json) {
    return TrainingGroundsStatus(
      level: (json['level'] as num?)?.toInt() ?? 1,
      totalInvested: (json['total_invested'] as num?)?.toInt() ?? 0,
      currentLevelProgress:
          (json['current_level_progress'] as num?)?.toInt() ?? 0,
      nextLevelCost: (json['next_level_cost'] as num?)?.toInt() ?? 100,
      progressRatio: (json['progress_ratio'] as num?)?.toDouble() ?? 0,
      guildCoinBalance: (json['guild_coin_balance'] as num?)?.toInt() ?? 0,
      description: json['description'] as String? ?? '',
      stageCode: json['stage_code'] as String? ?? 'FIELD_CAMP',
      stageName: json['stage_name'] as String? ?? '들판 훈련터',
      stageMessage:
          json['stage_message'] as String? ?? '작은 훈련터가 건강한 모험을 차근차근 기억하고 있어요.',
      nextMilestoneLevel: (json['next_milestone_level'] as num?)?.toInt(),
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
