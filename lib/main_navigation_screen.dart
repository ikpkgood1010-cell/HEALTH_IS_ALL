import 'package:flutter/material.dart';
import 'home_screen.dart';
import 'quest_screen.dart';
import 'shop_screen.dart';

/// HEALTH IS ALL - Main Bottom Navigation Container
/// Dual-Excellence: 건강 화면 우선 접근성과 게임성 상점/퀘스트의 유기적 결합
class MainNavigationScreen extends StatefulWidget {
const MainNavigationScreen({Key? key}) : super(key: key);

@override
State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
int _currentIndex = 0;

// 화면 목록 (1순위: 홈/건강, 2순위: 퀘스트, 3순위: 상점)
final List<Widget> _screens = [
const HomeScreen(),
const QuestScreen(),
const ShopScreen(currentExp: 120), // 모의 데이터 연결
 ];

@override
Widget build(BuildContext context) {
return Scaffold(
body: IndexedStack(
index: _currentIndex,
children: _screens,
),
bottomNavigationBar: Container(
decoration: BoxDecoration(
boxShadow: [
BoxShadow(
color: Colors.black.withOpacity(0.06),
blurRadius: 10,
offset: const Offset(0, -2),
),
 ],
),
child: BottomNavigationBar(
currentIndex: _currentIndex,
onTap: (index) {
setState(() {
_currentIndex = index;
});
},
selectedItemColor: Colors.green.shade700,
unselectedItemColor: Colors.grey.shade500,
selectedLabelStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
type: BottomNavigationBarType.fixed,
items: const [
BottomNavigationBarItem(
icon: Icon(Icons.favorite),
activeIcon: Icon(Icons.favorite, color: Colors.green),
label: '건강 홈',
),
BottomNavigationBarItem(
icon: Icon(Icons.assignment),
activeIcon: Icon(Icons.assignment, color: Colors.blue),
label: '퀘스트',
),
BottomNavigationBarItem(
icon: Icon(Icons.store),
activeIcon: Icon(Icons.store, color: Colors.purple),
label: '건강이 상점',
),
 ],
),
),
);
}
}