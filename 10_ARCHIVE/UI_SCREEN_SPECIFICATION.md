# UI SCREEN SPECIFICATION

Document Name: UI_SCREEN_SPECIFICATION.md
Version: 1.0
Status: Draft
Owner: Guild Health Architecture
Last Updated: 2026-07-28
Purpose: Define the official screen specifications, user interface component layouts, state representations, modal behaviors, and accessibility guidelines for Guild Health. This document serves as the single source of truth for UI implementation across Flutter presentation layers.

---

# 1. Home Dashboard (`/home`)

- **Purpose**: Primary landing screen providing a unified snapshot of daily health vitals, active RPG quests, and AI coach summaries.
- **Key Layout Sections**:
  - **Header**: User Avatar, Current Level/Title, Daily Streak Counter, and Notification Bell icon.
  - **Health Score Card**: Central gauge widget displaying the real-time calculated Health Score with trend indicator (up/down).
  - **Daily Vitals Grid**: Quick-access summary tiles for Meals, Exercise, Water, and Sleep.
  - **Active Quests Widget**: Carousel showing top 3 active daily quests with progress bars.
  - **AI Coach Insight Banner**: Collapsible card with the latest personalized health recommendation.
- **Primary Actions**: Tap vital tiles to navigate to detail/recording screens; tap quest cards to claim rewards.

---

# 2. Meal Recording Screen (`/meals/record`)

- **Purpose**: Log daily meals, food intake, calories, and macronutrients.
- **Key Layout Sections**:
  - **Meal Type Selector**: Segmented control (`Breakfast`, `Lunch`, `Dinner`, `Snack`).
  - **Input Methods**:
    - AI Camera/Photo Upload trigger button.
    - Barcode scanner shortcut.
    - Manual search text input with auto-complete.
  - **Selected Items List**: Itemized list displaying food name, portion size, calories, and macro breakdown (Protein/Carb/Fat).
  - **Daily Macro Summary Gauge**: Real-time progress bar comparing logged calories against daily targets.
- **Primary Actions**: "Save Meal Record" Floating Action Button (FAB) or bottom fixed button.

---

# 3. Exercise Recording Screen (`/exercise/record`)

- **Purpose**: Log physical activities, workouts, duration, and estimated calorie burn.
- **Key Layout Sections**:
  - **Activity Category Selector**: Grid options (`Running`, `Cycling`, `Strength Training`, `Walking`, `Custom`).
  - **Timer & Duration Card**: Interactive digital stopwatch/timer or manual duration input.
  - **Intensity Slider**: Perceived Exertion Scale (RPE 1-10).
  - **Metrics Summary**: Real-time display of calculated calories burned, distance (if GPS active), and earned RPG EXP points.
- **Primary Actions**: "Start Activity" / "Complete Workout" primary button.

---

# 4. Health Analysis Screen (`/analysis`)

- **Purpose**: Detailed analytical views and historical trend charts for user health metrics.
- **Key Layout Sections**:
  - **Timeframe Selector**: Tab bar (`Day`, `Week`, `Month`, `Year`).
  - **Metric Tabs**: Switch between `Health Score`, `Nutritional Balance`, `Activity & Workout`, and `Sleep/Recovery`.
  - **Interactive Trend Charts**: Multi-line/bar charts showing metric progression over time.
  - **AI Pattern Insights**: Bulleted narrative explaining positive patterns or warning signals detected by the Health Engine.
- **Primary Actions**: Date picker filter; export report button.

---

# 5. AI Coach Screen (`/ai-coach`)

- **Purpose**: Conversational AI guidance interface providing personalized health coaching and Q&A.
- **Key Layout Sections**:
  - **Coach Avatar & Status Header**: Visual indicator of AI companion mode and online status.
  - **Chat Thread View**: Chronological message list with distinct speech bubbles for User and AI Coach.
  - **Suggested Prompt Chips**: Horizontal scrollable list of quick questions (e.g., "Analyze my lunch", "Suggest a 15-min workout").
  - **Bottom Input Bar**: Multiline text input field, voice input button, and attachment button.
- **Primary Actions**: Send message button.

---

# 6. Quest Screen (`/quests`)

- **Purpose**: View, track, and accept daily, weekly, and special guild gamification quests.
- **Key Layout Sections**:
  - **Quest Category Tabs**: `Daily Quests`, `Weekly Quests`, `Guild Raid Quests`.
  - **Quest Cards List**: Each card displays quest title, description, progress bar (e.g., 2/3 meals logged), reward badges (EXP, Gold, Guild Points), and "Claim" / "In Progress" status buttons.
- **Primary Actions**: Claim reward button with animation trigger.

---

# 7. Guild Screen (`/guild`)

- **Purpose**: Social community hub for guild members to collaborate on group health goals.
- **Key Layout Sections**:
  - **Guild Header**: Guild banner image, name, level, member count, and total Guild Score.
  - **Guild Leaderboard**: Ranked list of top contributing guild members for the current cycle.
  - **Group Challenge Progress**: Shared progress gauge toward collective health targets.
  - **Guild Activity Feed / Chat**: Real-time chat and milestone announcement stream.
- **Primary Actions**: "Contribute Health Points" or "Join Guild Raid" button.

---

# 8. Companion Screen (`/companion`)

- **Purpose**: Interact with and customize the user's personal virtual health companion pet.
- **Key Layout Sections**:
  - **3D/2D Companion Stage**: Interactive animated display of the companion responding to touch gestures.
  - **Companion Vitals Bars**: Mood, Energy, and Health level indicators tied directly to the user's real-world health logs.
  - **Customization Wardrobe**: Grid picker for companion skins, accessories, and background environments.
- **Primary Actions**: Interact / Feed companion button.

---

# 9. Profile Screen (`/profile`)

- **Purpose**: Manage personal health profile, RPG level progression, and earned achievements.
- **Key Layout Sections**:
  - **User Overview Card**: Profile photo, display name, user title, Level badge, and total EXP bar.
  - **Achievements Grid**: Trophy matrix displaying unlocked and locked health milestone badges.
  - **Personal Health Parameters**: Age, height, target weight, dietary preferences, and daily calorie/water targets.
- **Primary Actions**: "Edit Profile" button; share achievement card button.

---

# 10. Settings Screen (`/settings`)

- **Purpose**: Configure application preferences, privacy settings, device integrations, and account options.
- **Key Layout Sections**:
  - **Device & Health Sync**: Toggle switches for Apple Health, Google Health Connect, and wearable sensors.
  - **Notifications**: Granular preference toggles for quest reminders, meal alerts, and AI coach messages.
  - **Account & Security**: Biometric lock toggle, password change, and privacy settings.
  - **App Information**: Version details, terms of service, and sign-out/delete account buttons.
- **Primary Actions**: Save preferences switch actions.

---

# 11. Login Screen (`/login`)

- **Purpose**: User authentication and identity verification.
- **Key Layout Sections**:
  - **Brand Header**: Guild Health logo and welcoming tagline.
  - **Social Sign-In Buttons**: Full-width "Continue with Apple" and "Continue with Google" buttons.
  - **Email Credentials Form**: Email text field, password text field with visibility toggle, and "Forgot Password?" link.
- **Primary Actions**: "Sign In" primary button; "Create Account" link navigation.

---

# 12. Signup Screen (`/signup`)

- **Purpose**: Account creation and initial multi-step onboarding flow.
- **Key Layout Sections**:
  - **Step Progress Indicator**: Visual progress bar indicating current onboarding step (1. Account -> 2. Basic Profile -> 3. Health Goals).
  - **Input Form Fields**: Contextual form inputs depending on current step.
- **Primary Actions**: "Next Step" / "Complete Registration" button.

---

# 13. Loading State Specification

- **Skeleton Loaders**: Use animated skeleton placeholders matching the exact card/list dimensions of the target screen instead of blocking spinners for content-heavy views.
- **Full-Screen Overlays**: Use a semi-transparent modal overlay with a branded progress indicator for blocking operations (e.g., account creation, health data sync).
- **In-Line Spinners**: Smaller 24dp circular progress indicators placed inside buttons during async action processing.

---

# 14. Empty State Specification

- **Visual Element**: Custom illustrated graphic or icon themed around the missing data context.
- **Headline Text**: Clear concise statement explaining the empty condition (e.g., "No Meals Logged Today").
- **Body Explanation**: Encouraging explanation (e.g., "Log your breakfast to kickstart your daily quest!").
- **Call-To-Action (CTA) Button**: Prominent action button directing the user to the recording/creation screen.

---

# 15. Error State Specification

- **Inline Component Errors**: Display a localized error card with a retry button (`AppErrorCard`) when a widget fails to load data.
- **Network / Offline Banner**: Top sticky banner displaying "Offline Mode - Changes will sync when reconnected".
- **Critical Failure Screens**: Centered layout with warning illustration, user-friendly masked message, and a primary "Tap to Retry" button.

---

# 16. Bottom Navigation Bar

- **Visibility**: Displayed across top-level primary screens (`Home`, `Quests`, `AI Coach`, `Guild`, `Profile`). Hidden during deep flows (e.g., Meal Recording, Settings).
- **Items (5 Tabs)**:
  1. **Home**: Icon `home_outlined` / `home_filled`.
  2. **Quests**: Icon `assignment_outlined` / `assignment_filled`.
  3. **AI Coach**: Icon `smart_toy_outlined` / `smart_toy_filled` with glowing accent badge.
  4. **Guild**: Icon `groups_outlined` / `groups_filled`.
  5. **Profile**: Icon `person_outlined` / `person_filled`.
- **Behavior**: Haptic feedback on tab selection; active tab highlighted with primary color token.

---

# 17. Floating Action Button (FAB) Rules

- **Default Position**: Bottom-right floating anchored above the Bottom Navigation Bar.
- **Primary Use Case**: Quick-action logging menu (`+` icon). Tapping expands a radial/speed-dial menu with shortcuts for `Log Meal`, `Log Exercise`, and `Log Water`.
- **Contextual Hiding**: FAB must smoothly scroll off-screen when scrolling down long lists and reappear when scrolling up.

---

# 18. Dialog Rules

- **Alert Dialogs**: Used for destructive or irreversible actions (e.g., Delete Record, Leave Guild). Must contain: Title, concise message, "Cancel" secondary button, and affirmative/destructive primary button.
- **Confirmation Dialogs**: Used for claiming high-value quest rewards or leveling up, featuring celebratory visual effects (confetti/particles).

---

# 19. Bottom Sheet Rules

- **Modal Bottom Sheets**: Used for secondary contextual forms or quick filters (e.g., meal portion adjustment, time filter selector).
- **Drag Handle**: Top centered 4dp x 32dp visual drag handle.
- **Dismissal**: Supports swipe-down gesture or backdrop tapping to dismiss.

---

# 20. Accessibility (a11y) Requirements

- **Touch Targets**: All interactive buttons and touch points must be at least 48x48dp.
- **Color Contrast**: Text and visual elements must maintain a minimum WCAG AA contrast ratio of 4.5:1 against backgrounds.
- **Screen Reader Support**: All UI widgets, images, and buttons must include explicit `Semantics` labels and hints for TalkBack/VoiceOver.
- **Font Scaling**: Layouts must gracefully adapt to dynamic text sizing up to 200% scaling without text clipping or horizontal overflow.

---

# 21. Related Documents

- `DESIGN_SYSTEM.md`
- `FEATURE_IMPLEMENTATION_GUIDE.md`
- `FLUTTER_PROJECT_STRUCTURE.md`
- `HEALTH_ENGINE.md`
- `CODE_GENERATION_RULES.md`