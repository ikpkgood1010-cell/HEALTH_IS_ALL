# HEALTH IS ALL 전투 스프라이트 요청서 V1

## 제작 범위와 순서

공식 초상 84장을 모두 다시 애니메이션으로 만들지 않는다. MVP는 **6직업 × 남녀 = 12명**의
전투 기본 스프라이트만 먼저 만든다. 전직 차수는 초상·도감에서 즉시 바뀌며, 전투에서는
차수별 무기 보석·망토색·오라 같은 가벼운 보정으로 시작한다. 84명 전체의 차수별 전투
애니메이션은 플레이 검증 후 확장한다.

생성 순서는 `idle → walk → 기본 공격 → 직업 스킬 → hit → defeat`다. 한 요청에서 여러 동작,
여러 직업, 여러 성별을 섞지 않는다. 항상 **용사 1명 + 동작 1개**만 요청한다.

## 모든 요청에 반드시 붙일 공통 블록

```text
Use the attached approved HEALTH IS ALL hero portrait as the only character reference.
Do not redesign the hero. Preserve the exact hair color and silhouette, face shape, gender,
class weapon, primary palette, crown/head ornament, cape silhouette, and gem colors.

Create a 32-bit soft chunky pixel-art MOBILE BATTLE SPRITE SHEET, not a painted illustration,
not 3D, not anime, not vector art, not smooth anti-aliased art.

Canvas: one horizontal strip, exactly 4 equal square cells in a row. Each cell is 256 by 256 px;
the full sheet is 1024 by 256 px. Every cell uses the identical camera scale and the identical
floor baseline: both feet touch y=222 inside each 256px cell. Keep 12px of empty safe margin on
all sides. The full body and weapon must stay inside the cell; do not crop hands, staff, bow,
shield, cape, arrows, or effects.

Hero faces RIGHT. This is mandatory for every friendly hero. Keep a side-facing 3/4 battle pose.
Use a thick dark navy 2px pixel outline, crisp hard pixels, no blurry edge, no realistic texture,
no text, no letters, no numbers, no logos, no UI, no border, no shadow beneath the feet.

Background must be one completely flat chroma-key magenta #FF00FF, with no gradient, texture,
sparkle, smoke, shadow, or magenta pixels on the hero. Do not use white as the background.
The magenta background will be removed after generation.

Match the attached portrait's established HEALTH IS ALL pixel style exactly. This is an in-game
combat sprite, so simplify tiny decorative details but preserve the hero's recognizable silhouette.
```

## 동작별 추가 블록

### 1. Idle — 4 프레임

```text
Action: IDLE LOOP. Frame 1 neutral ready stance. Frame 2 body rises 2px and cape/hair shifts 1px.
Frame 3 neutral ready stance again. Frame 4 body lowers 1px and cape/hair settles. Weapon never
changes hands. No attack, projectile, spell, impact, camera movement, extra character, or effect.
The fourth frame must loop cleanly into the first frame.
```

### 2. Walk — 4 프레임

```text
Action: WALK LOOP TO THE RIGHT. Frame 1 left foot forward. Frame 2 passing pose. Frame 3 right
foot forward. Frame 4 passing pose returning to frame 1. Maintain the hero at the same horizontal
center in every cell: the app moves the sprite, not the artwork. Weapon and shield stay readable;
cape/hair move only slightly. No dust, speed line, attack, projectile, spell, or camera movement.
```

### 3. Basic attack — 4 프레임

```text
Action: BASIC ATTACK TO THE RIGHT. Frame 1 short wind-up. Frame 2 strongest attack pose.
Frame 3 impact extension. Frame 4 recovery pose that can return to idle. Keep the character's feet
on the same floor baseline. Use only a tiny class-colored impact flash at the weapon tip in frame 3;
no enemy, no damage number, no large visual effect, no screen shake, and no projectile unless this
class is archer or mage.
```

### 4. Hit — 4 프레임

```text
Action: HIT REACTION. Frame 1 normal ready pose. Frame 2 torso recoils 3px backward with a tiny
white impact flash on the chest. Frame 3 recoil settles. Frame 4 returns toward idle. Do not add
blood, enemy, number, text, explosion, knockdown, or camera shake.
```

### 5. Defeat — 4 프레임

```text
Action: DEFEAT. Frame 1 weakened stance. Frame 2 knees buckle. Frame 3 character falls toward the
ground facing right. Frame 4 lies still entirely inside the cell on the floor baseline. Preserve
weapons and clothing; no gore, disappearance, enemy, UI, or text.
```

## 직업별 스킬 요청 추가 문장

공통 블록과 `BASIC ATTACK` 또는 별도 스킬 요청 뒤에, 해당 직업 문장 하나만 붙인다.

| 직업 | 스킬 문장 |
| --- | --- |
| 탱커 | `Class skill: raise the shield toward the right, then produce a compact teal-and-gold fortress barrier in front of the shield. The barrier must remain inside the cell and use no background rectangle.` |
| 전사 | `Class skill: make one heavy greatsword slash toward the right. Use a compact warm gold and red arc that follows the sword edge only; do not cover the hero.` |
| 궁수 | `Class skill: draw the bow, release one teal-and-gold arrow to the right, then recover. The arrow must remain inside the cell; no enemy target or large trail.` |
| 마법사 | `Class skill: raise the staff and book, then release one compact purple crystal star projectile to the right. Keep the spell small enough that the entire hero stays visible.` |
| 도적 | `Class skill: cross both daggers in a fast right-facing slash. Use two short purple-and-teal arcs only; do not create a full-screen blur, clone, or teleport.` |
| 치유사 | `Class skill: raise the staff and create one small mint-and-gold lotus healing pulse centered on the hero's chest. No health bar, no text, no giant aura, and no other character.` |

## 요청 예시 — 남성 탱커 Idle

```text
[공통 블록 전체]

Character: male tanker, use the attached male tanker official portrait. Preserve his dark navy,
teal, gold and silver fortress armor, shield, mace, cape and crown silhouette.

[Idle 4 프레임 블록 전체]
```

## 요청 예시 — 여성 궁수 기본 공격

```text
[공통 블록 전체]

Character: female archer, use the attached female archer official portrait. Preserve her green,
gold and silver leaf armor, longbow, quiver, hair silhouette and crown ornament.

[Basic attack 4 프레임 블록 전체]

Class skill: draw the bow, release one teal-and-gold arrow to the right, then recover. The arrow
must remain inside the cell; no enemy target or large trail.
```

## 금지 사항 요약

- 카드, 덱, 턴, 제한시간, UI 프레임, 수치, 글자, 워터마크
- 배경 장면, 적 캐릭터, 다른 아군, 바닥 그림자, 카메라 줌
- 흰색/검정색 배경, 불투명 체크무늬, 흐린 테두리, 반실사 렌더링
- 한 장에 여러 동작·여러 캐릭터·여러 무기를 섞는 구성

## 생성 후 보관 규칙

원본 출력은 수정하지 않고 `assets/source/`에 보관한다. 승인된 결과만 배경 제거·정규화해
`assets/approved/combat-sprites/`에 넣는다. 파일명은
`{class}_{gender}_t{tier}_{action}_{frame-count}.png` 형식을 사용한다.
