import 'dart:convert';
import 'package:hive_flutter/hive_flutter.dart';

/// ============================================================================
/// Offline Cache & Sync Repository (v1.0)
/// Based on: Flutter_Architecture_Setup.md & Screen_Specification_Master.md
/// ============================================================================

/// 오프라인 캐시 레코드 모델
class CachedRecord {
final String id;
final String type; // 'meal', 'exercise', 'habit', 'spirit_bp'
final Map<String, dynamic> data;
final DateTime createdAt;
bool isSynced;

CachedRecord({
required this.id,
required this.type,
required this.data,
required this.createdAt,
this.isSynced = false,
});

Map<String, dynamic> toJson() => {
'id': id,
'type': type,
'data': data,
'createdAt': createdAt.toIso8601String(),
'isSynced': isSynced,
};

factory CachedRecord.fromJson(Map<String, dynamic> json) => CachedRecord(
id: json['id'] as String,
type: json['type'] as String,
data: Map<String, dynamic>.from(json['data'] as Map),
createdAt: DateTime.parse(json['createdAt'] as String),
isSynced: json['isSynced'] as bool? ?? false,
);
}

/// Hive 기반 오프라인 저장소 및 서버 동기화 파이프라인
class OfflineCacheRepository {
static const String _healthCacheBoxName = 'health_records_cache';
static const String _userStateBoxName = 'user_state_cache';

late Box<String> _recordsBox;
late Box<String> _userStateBox;

/// 로컬 데이터베이스(Hive) 초기화
Future<void> initialize() async {
await Hive.initFlutter();
_recordsBox = await Hive.openBox<String>(_healthCacheBoxName);
_userStateBox = await Hive.openBox<String>(_userStateBoxName);
}

/// 1. 레코드 저장 (오프라인 우선 쓰기)
Future<void> saveRecord(CachedRecord record) async {
final jsonString = jsonEncode(record.toJson());
await _recordsBox.put(record.id, jsonString);
}

/// 2. 전체 미동기화 레코드 조회 (서버 업로드용)
List<CachedRecord> getUnsyncedRecords() {
final allRecords = _getAllRecords();
return allRecords.where((record) => !record.isSynced).toList();
}

/// 3. 동기화 완료 상태 업데이트
Future<void> markAsSynced(List<String> recordIds) async {
for (final id in recordIds) {
final jsonString = _recordsBox.get(id);
if (jsonString != null) {
final record = CachedRecord.fromJson(jsonDecode(jsonString));
record.isSynced = true;
await _recordsBox.put(id, jsonEncode(record.toJson()));
}
}
}

/// 4. 유저 홈 상태 캐싱 (Read Model 빠른 로딩용)
Future<void> cacheHomeReadModel(Map<String, dynamic> homeData) async {
final jsonString = jsonEncode({
'data': homeData,
'cachedAt': DateTime.now().toIso8601String(),
});
await _userStateBox.put('home_read_model', jsonString);
}

/// 캐시된 홈 상태 읽기
Map<String, dynamic>? getCachedHomeReadModel() {
final jsonString = _userStateBox.get('home_read_model');
if (jsonString == null) return null;

try {
final decoded = jsonDecode(jsonString) as Map<String, dynamic>;
return decoded['data'] as Map<String, dynamic>?;
} catch (_) {
return null;
}
}

/// 내부 전체 레코드 파싱 파이프라인
List<CachedRecord> _getAllRecords() {
final List<CachedRecord> list = [];
for (var key in _recordsBox.keys) {
final jsonString = _recordsBox.get(key);
if (jsonString != null) {
try {
list.add(CachedRecord.fromJson(jsonDecode(jsonString)));
} catch (_) {
// 손상된 데이터 패스
}
}
}
list.sort((a, b) => b.createdAt.compareTo(a.createdAt));
return list;
}

/// 오래된 캐시 데이터 정리 (30일 이상 경과한 동기화 완료 데이터)
Future<void> purgeExpiredRecords() async {
final now = DateTime.now();
final keysToDelete = <dynamic>[];

for (var key in _recordsBox.keys) {
final jsonString = _recordsBox.get(key);
if (jsonString != null) {
try {
final record = CachedRecord.fromJson(jsonDecode(jsonString));
if (record.isSynced && now.difference(record.createdAt).inDays > 30) {
keysToDelete.add(key);
}
} catch (_) {
// 손상된 데이터 패스
}
}
}

await _recordsBox.deleteAll(keysToDelete);
}

/// 전체 캐시 비우기 (로그아웃 시)
Future<void> clearAll() async {
await _recordsBox.clear();
await _userStateBox.clear();
}
}