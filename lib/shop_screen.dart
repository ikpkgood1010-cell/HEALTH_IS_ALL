import 'package:flutter/material.dart';

/// HEALTH IS ALL - '건강이' Shop & Customization Screen
/// SSOT Standard: Exp, 건강이
class ShopScreen extends StatefulWidget {
  final int currentExp;

  const ShopScreen({Key? key, required this.currentExp}) : super(key: key);

  @override
  State<ShopScreen> createState() => _ShopScreenState();
}

class _ShopScreenState extends State<ShopScreen> {
  late int _userExp;

  final List<Map<String, dynamic>> _skins = [
    {
      'id': 'skin_green',
      'name': '새싹 건강이',
      'cost': 0,
      'isUnlocked': true,
      'color': Colors.lightGreen,
      'desc': "기본 '건강이'의 풋풋한 새싹 스킨",
    },
    {
      'id': 'skin_runner',
      'name': '러너 건강이',
      'cost': 150,
      'isUnlocked': false,
      'color': Colors.orangeAccent,
      'desc': '달리기 활력이 흘러넘치는 에너지 스킨',
    },
    {
      'id': 'skin_doctor',
      'name': '닥터 건강이',
      'cost': 300,
      'isUnlocked': false,
      'color': Colors.lightBlue,
      'desc': '건강 상식을 정밀하게 관리해주는 스마트 스킨',
    },
  ];

  @override
  void initState() {
    super.initState();
    _userExp = widget.currentExp;
  }

  void _buySkin(int index) {
    final skin = _skins[index];
    if (_userExp >= skin['cost']) {
      setState(() {
        _userExp -= skin['cost'] as int;
        skin['isUnlocked'] = true;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("'${skin['name']}' 스킨을 해금했습니다!")),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('보유 Exp가 부족합니다. 건강 활동으로 Exp를 더 모아보세요!')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("'건강이' 상점", style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 1,
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: Center(
              child: Chip(
                avatar: const Icon(Icons.stars, color: Colors.amber, size: 20),
                label: Text('$_userExp Exp', style: const TextStyle(fontWeight: FontWeight.bold)),
                backgroundColor: Colors.purple.shade50,
              ),
            ),
          ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: _skins.length,
        itemBuilder: (context, index) {
          final item = _skins[index];
          final bool unlocked = item['isUnlocked'] as bool;
          return Card(
            margin: const EdgeInsets.only(bottom: 14.0),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: ListTile(
              contentPadding: const EdgeInsets.all(16),
              leading: CircleAvatar(
                radius: 28,
                backgroundColor: item['color'] as Color,
                child: const Icon(Icons.face, color: Colors.white, size: 32),
              ),
              title: Text(item['name'] as String, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              subtitle: Text(item['desc'] as String),
              trailing: unlocked
                  ? const ElevatedButton(
                      onPressed: null,
                      child: Text('보유 중'),
                    )
                  : ElevatedButton(
                      onPressed: () => _buySkin(index),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.purple),
                      child: Text("${item['cost']} Exp"),
                    ),
            ),
          );
        },
      ),
    );
  }
}
