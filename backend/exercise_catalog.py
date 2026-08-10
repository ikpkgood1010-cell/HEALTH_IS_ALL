"""Canonical exercise category and intensity codes from the approved spec."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExerciseCategoryGroup(str, Enum):
    CARDIO = "CARDIO"
    STRENGTH = "STRENGTH"
    FLEXIBILITY = "FLEXIBILITY"
    SPORTS = "SPORTS"


class IntensityLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ExerciseCategory(str, Enum):
    STAIR_CLIMBING_FAST = "STAIR_CLIMBING_FAST"
    HIKING_HARD = "HIKING_HARD"
    CROSSFIT = "CROSSFIT"
    HYROX = "HYROX"
    TRAMPOLINE_JUMPING = "TRAMPOLINE_JUMPING"
    HIIT = "HIIT"
    JUMP_ROPE = "JUMP_ROPE"
    KETTLEBELL_SWING = "KETTLEBELL_SWING"
    ROWING_FAST = "ROWING_FAST"
    ASSAULT_BIKE = "ASSAULT_BIKE"
    RUNNING = "RUNNING"
    SPINNING = "SPINNING"
    BURPEE_PLYOMETRICS = "BURPEE_PLYOMETRICS"
    STAIR_CLIMBING_SLOW = "STAIR_CLIMBING_SLOW"
    HIKING_EASY = "HIKING_EASY"
    ZUMBA = "ZUMBA"
    POWER_WALKING = "POWER_WALKING"
    PILATES = "PILATES"
    JOGGING = "JOGGING"
    SWIMMING = "SWIMMING"
    CYCLING = "CYCLING"
    WEIGHT_TRAINING = "WEIGHT_TRAINING"
    YOGA = "YOGA"
    STRETCHING_FOAM_ROLLER = "STRETCHING_FOAM_ROLLER"
    WALKING = "WALKING"
    TAI_CHI = "TAI_CHI"
    SWIMMING_LIGHT = "SWIMMING_LIGHT"


@dataclass(frozen=True)
class ExerciseDefinition:
    group: ExerciseCategoryGroup
    category: ExerciseCategory
    intensity: IntensityLevel


EXERCISE_CATALOG = (
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.STAIR_CLIMBING_FAST, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.SPORTS, ExerciseCategory.HIKING_HARD, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.STRENGTH, ExerciseCategory.CROSSFIT, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.STRENGTH, ExerciseCategory.HYROX, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.TRAMPOLINE_JUMPING, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.HIIT, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.JUMP_ROPE, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.STRENGTH, ExerciseCategory.KETTLEBELL_SWING, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.ROWING_FAST, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.ASSAULT_BIKE, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.RUNNING, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.SPINNING, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.STRENGTH, ExerciseCategory.BURPEE_PLYOMETRICS, IntensityLevel.HIGH),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.STAIR_CLIMBING_SLOW, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.SPORTS, ExerciseCategory.HIKING_EASY, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.ZUMBA, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.POWER_WALKING, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.FLEXIBILITY, ExerciseCategory.PILATES, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.JOGGING, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.SWIMMING, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.CYCLING, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.STRENGTH, ExerciseCategory.WEIGHT_TRAINING, IntensityLevel.MEDIUM),
    ExerciseDefinition(ExerciseCategoryGroup.FLEXIBILITY, ExerciseCategory.YOGA, IntensityLevel.LOW),
    ExerciseDefinition(ExerciseCategoryGroup.FLEXIBILITY, ExerciseCategory.STRETCHING_FOAM_ROLLER, IntensityLevel.LOW),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.WALKING, IntensityLevel.LOW),
    ExerciseDefinition(ExerciseCategoryGroup.FLEXIBILITY, ExerciseCategory.TAI_CHI, IntensityLevel.LOW),
    ExerciseDefinition(ExerciseCategoryGroup.CARDIO, ExerciseCategory.SWIMMING_LIGHT, IntensityLevel.LOW),
)
