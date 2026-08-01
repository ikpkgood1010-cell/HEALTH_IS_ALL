import 'dart:async';
import 'dart:math';
import 'package:flutter/foundation.dart';

/// HEALTH IS ALL - Offline Outbox Sync Manager
/// Filename: offline_sync_manager.dart
/// Path: HEALTH IS ALL/lib/offline_sync_manager.dart
/// Purpose: 오프라인 아웃박스 큐 관리, 네트워크 연결 대기, 자동 플러시 및 보상 무결성 유지 위젯/클래스
enum SyncItemType { healthLog, spiritReward }
enum SyncStatus { pending, syncing, completed, failed }

class OutboxItem {
  final String queueId;
  final SyncItemType type;
  final Map<String, dynamic> payload;
  final double createdAtUtc;
  int retryCount;
  SyncStatus status;

  OutboxItem({
    required this.queueId,
    required this.type,
    required this.payload,
    required this.createdAtUtc,
    this.retryCount = 0,
    this.status = SyncStatus.pending,
  });

  int get syncWeight {
    int baseWeight = (type == SyncItemType.healthLog) ? 100 : 10;
    return baseWeight - retryCount;
  }

  Map<String, dynamic> toJson() => {
        'queue_id': queueId,
        'type': type == SyncItemType.healthLog ? 'HEALTH_LOG' : 'SPIRIT_REWARD',
        'payload': payload,
        'created_at_utc': createdAtUtc,
        'sync_weight': syncWeight,
        'retry_count': retryCount,
      };
}

class OfflineSyncManager extends ChangeNotifier {
  final List<OutboxItem> _outboxQueue = [];
  bool _isOnline = true;
  bool _isSyncing = false;

  List<OutboxItem> get pendingItems => _outboxQueue.where((e) => e.status == SyncStatus.pending).toList();
  bool get isOnline => _isOnline;
  bool get isSyncing => _isSyncing;
  int get pendingCount => pendingItems.length;

  /// 건강 기록 또는 정령 보상 아웃박스 추가
  void enqueueItem(SyncItemType type, Map<String, dynamic> payload) {
    final newItem = OutboxItem(
      queueId: 'Q_${DateTime.now().millisecondsSinceEpoch}_${Random().nextInt(9999)}',
      type: type,
      payload: payload,
      createdAtUtc: DateTime.now().toUtc().millisecondsSinceEpoch / 1000.0,
    );

    _outboxQueue.add(newItem);
    notifyListeners();

    // 온라인 상태라면 즉시 플러시 시도
    if (_isOnline && !_isSyncing) {
      triggerSync();
    }
  }

  /// 네트워크 상태 변경 시 감지
  void updateNetworkStatus(bool isConnected) {
    _isOnline = isConnected;
    notifyListeners();

    if (_isOnline && pendingCount > 0 && !_isSyncing) {
      triggerSync();
    }
  }

  /// 동기화 실행 (Outbox Flush)
  Future<void> triggerSync() async {
    if (!_isOnline || _isSyncing || pendingCount == 0) return;

    _isSyncing = true;
    notifyListeners();

    // 우선순위 정렬 (건강 기록 > 정령 보상)
    final itemsToSync = pendingItems..sort((a, b) => b.syncWeight.compareTo(a.syncWeight));

    for (var item in itemsToSync) {
      item.status = SyncStatus.syncing;
      notifyListeners();

      bool success = await _mockServerSync(item);

      if (success) {
        item.status = SyncStatus.completed;
      } else {
        item.retryCount++;
        item.status = SyncStatus.failed;
        // 지수 백오프 시간 계산
        double backoffSec = min(300.0, 2.0 * pow(2, item.retryCount) + Random().nextDouble());
        debugPrint('[SyncManager] Item ${item.queueId} failed. Retry in ${backoffSec.toStringAsFixed(1)}s');
      }
      notifyListeners();
    }

    // 완료된 항목 제거
    _outboxQueue.removeWhere((item) => item.status == SyncStatus.completed);
    _isSyncing = false;
    notifyListeners();
  }

  /// 가상 서버 동기화 통신 (실제 운영 시 http.post 교체)
  Future<bool> _mockServerSync(OutboxItem item) async {
    await Future.delayed(const Duration(milliseconds: 600));
    // 95% 확률로 성공 모사
    return Random().nextDouble() > 0.05;
  }
}