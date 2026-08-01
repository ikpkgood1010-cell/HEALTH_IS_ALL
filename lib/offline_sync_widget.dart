import 'package:flutter/material.dart';

/// HEALTH IS ALL - Offline Status & Sync Progress Widget
/// Filename: offline_sync_widget.dart
/// Path: HEALTH IS ALL/lib/offline_sync_widget.dart
/// Purpose: 오프라인 모드 안내, 로컬 보관 큐 개수 표시 및 동기화 카드 UI
class OfflineSyncWidget extends StatelessWidget {
  final bool isOffline;
  final int pendingCount;
  final String syncMessage;

  const OfflineSyncWidget({
    Key? key,
    this.isOffline = false,
    this.pendingCount = 3,
    this.syncMessage = '정령이 비밀 노트에 소중히 기록해두고 있어요 📝 network가 연결되면 한 번에 전해줄게요!',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 6,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      color: isOffline ? const Color(0xFF2C2219) : const Color(0xFF1A1D26),
      child: Padding(
        padding: const EdgeInsets.all(18.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header Row
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Icon(
                      isOffline ? Icons.wifi_off_rounded : Icons.cloud_done_rounded,
                      color: isOffline ? Colors.orangeAccent : Colors.lightGreenAccent,
                      size: 22,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      isOffline ? '오프라인 기록 모드' : '동기화 완료',
                      style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: (isOffline ? Colors.orangeAccent : Colors.lightGreenAccent).withOpacity(0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: isOffline ? Colors.orangeAccent : Colors.lightGreenAccent),
                  ),
                  child: Text(
                    isOffline ? '보관 중 $pendingCount건' : '안전함',
                    style: TextStyle(
                      color: isOffline ? Colors.orangeAccent : Colors.lightGreenAccent,
                      fontSize: 11,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Message Banner
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isOffline ? const Color(0xFF382B20) : const Color(0xFF242836),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Text(
                syncMessage,
                style: TextStyle(color: Colors.grey[300], fontSize: 12, height: 1.4),
              ),
            ),
          ],
        ),
      ),
    );
  }
}