"""Runtime schema definitions for Java Reading Project workspace data.

This module is the single source of truth for enums, required fields, status
transitions, and id-format regexes used by `validate-progress.py`. The reference
markdown documents (runtime-control.md, evidence-policy.md, etc.) describe
intent; this file is the machine-checkable contract.

Reference packet ownership:
- progress-state.yaml shape:           runtime-control.md §Progress Data Shapes
- adaptive-training-data.yaml shape:   adaptive-difficulty.md §Data Shape
- progress_update required fields:     runtime-control.md §Progress Update Required Fields
- recommendation shape:                start-project.md §Recommendation Format (data layer)
"""

from __future__ import annotations

import re


# ---------- shared enums ----------

SIZE_ENUM = {"s", "m", "b"}

ENTRY_MODE_ENUM = {"incident-first", "design-document"}

TEACHING_MODE_ENUM = {"guided", "auto"}

BUILD_MODE_ENUM = {"normal", "follow", "micro-follow"}

TRAINING_MODE_ENUM = {"single", "mix"}

ADAPTIVE_LEVEL_ENUM = {"supportive", "standard", "stretch"}

PROGRESS_STATUS_ENUM = {
    "idle",
    "generating_recommendation",
    "selected",
    "building",
    "assessment_pending",
    "paused",
    "completed",
}

VALIDATION_STATUS_ENUM = {"validated", "runnable", "draft"}

ASSESSMENT_STATUS_ENUM = {"pending", "partial", "completed", "skipped"}

ASSESSMENT_SUBITEM_ENUM = {"pending", "weak", "adequate", "strong"}

MASTERY_STATUS_ENUM = {"learning", "proficient", "senior_ready"}

NODE_MASTERY_ASSESSMENT_ENUM = {"pending", "limited", "partial", "completed"}

CONFIDENCE_BAND_ENUM = {"low", "medium", "high"}

PROMPT_TYPE_ENUM = {
    "code-snippet",
    "incident",
    "concept",
    "bad-design",
    "syntax-bridge",
    "classification",
}

INCIDENT_KIND_ENUM = {
    "failed output",
    "log",
    "alert",
    "ticket",
    "exception trace",
    "not_supported",
}

ASK_SESSION_MODE_ENUM = {"initial", "follow_up", "incremental"}

ADAPTIVE_BASIS_ENUM = {"ask data", "assessment", "weakpoints", "default"}


# Adaptive controls — each control has its own enum, applied across multiple shapes.
ADAPTIVE_CONTROLS_ENUMS = {
    "explanation_density": {"more", "standard", "shorter"},
    "clue_exposure": {"conclusion-first", "balanced", "clue-first"},
    "jdk8_bridge": {"more", "standard", "brief"},
    "equipment_callback": {"direct", "hinted", "challenge"},
    "assessment_followup_depth": {"scaffolded", "standard", "deeper"},
}


# ---------- progress-state.yaml ----------

# progress.* required fields. Every field listed here must be present in the
# progress object even if its value is null.
PROGRESS_REQUIRED_FIELDS = (
    "current_node",
    "current_project",
    "current_size",
    "current_milestone",
    "current_slice",
    "current_entry_mode",
    "current_investigation_focus",
    "current_adaptive_level",
    "current_adaptive_controls",
    "teaching_mode",
    "build_mode",
    "current_follow_block",
    "status",
    "paused_at",
    "pause_reason",
)

# Top-level workspace-state collections.
PROGRESS_STATE_TOP_REQUIRED = ("version", "progress")
PROGRESS_STATE_TOP_OPTIONAL = (
    "completed_projects",
    "weakpoints",
    "node_mastery",
    "equipment_unlocked",
    "adaptive_summary",
    "next_project_bias",
)

# completed_projects[] entry — required fields.
# Matches runtime-control.md §Progress Update Required Fields plus a few entry-
# only metadata fields (training_mode, boundary_id, seed_id, etc. are all in
# both).
COMPLETED_PROJECT_REQUIRED = (
    "node_id",
    "project_name",
    "size",
    "entry_mode",
    "investigation_focus",
    "adaptive_level",
    "adaptive_controls",
    "build_mode",
    "training_mode",
    "boundary_id",
    "seed_id",
    "cross_id",
    "project_type",
    "enterprise_slice",
    "entry_fallback_reason",
    "domain",
    "io_shape",
    "artifact_shape",
    "core_flow",
    "primary_training",
    "secondary_training",
    "background_only",
    "primary_data_structures",
    "interaction_model",
    "mastery_signal",
    "out_of_scope",
    "concepts_covered",
    "user_questions_summary",
    "weakpoints_found",
    "teaching_slices_summary",
    "equipment_unlocked",
    "equipment_used",
    "fm_exposed",
    "fm_resolved",
    "transfer_evidence",
    "build_passed",
    "demo_passed",
    "teaching_questions",
    "assessment",
    "mastery_review",
)

# weakpoints[] entry.
WEAKPOINT_REQUIRED = (
    "node_id",
    "boundary_id",
    "status",
    "concept",
    "issue",
    "evidence",
    "evidence_refs",
    "source_project",
    "last_seen",
)
WEAKPOINT_STATUS_ENUM = {"open", "resolved"}
WEAKPOINT_OPTIONAL = ("fm_id",)  # legacy entries may omit fm_id

# equipment_unlocked[] entry (workspace level).
EQUIPMENT_REQUIRED = (
    "name",
    "node_id",
    "source_slice",
    "use_sentence",
    "transfer_contexts",
    "code_evidence",
)
EQUIPMENT_OPTIONAL = ("project_name", "unlocked_at", "last_used_at", "use_count")

# completed_projects[].equipment_unlocked[] entry (inline — slightly trimmer).
INLINE_EQUIPMENT_REQUIRED = (
    "name",
    "source_slice",
    "use_sentence",
    "transfer_contexts",
    "code_evidence",
)

# assessment object inside completed_projects[].
ASSESSMENT_REQUIRED = (
    "status",
    "main_flow_reconstruction",
    "boundary_ownership",
    "failure_classification",
    "bad_design_diagnosis",
    "transfer_check",
    "evidence_summary",
)

# mastery_review object inside completed_projects[].
MASTERY_REVIEW_OPTIONAL = ("status", "note", "evidence_refs")

# adaptive_summary.<node_id> entry.
ADAPTIVE_SUMMARY_REQUIRED = (
    "asked_at",
    "sample_count",
    "confidence",
    "target_rating",
    "current_level",
    "strongest_boundaries",
    "hardest_boundaries",
    "hardest_fm",
    "preferred_controls",
)
ADAPTIVE_SUMMARY_OPTIONAL = ("updated_at", "source")

# node_mastery.<node_id> entry.
NODE_MASTERY_REQUIRED = (
    "status",
    "assessment",
    "completed_required_boundaries",
    "remaining_required_boundaries",
    "note",
)
NODE_MASTERY_OPTIONAL = ("evidence_limited_estimate",)

# next_project_bias.<node_id> entry.
NEXT_PROJECT_BIAS_OPTIONAL = (
    "prefer_boundary",
    "prefer",
    "avoid",
    "reason",
    "suggested_command",
)


# ---------- adaptive-training-data.yaml ----------

ADAPTIVE_TRAINING_TOP_REQUIRED = ("version", "nodes")

ADAPTIVE_PROFILE_REQUIRED = (
    "asked_at",
    "sample_count",
    "confidence",
    "target_rating",
    "current_level",
    "strongest_boundaries",
    "hardest_boundaries",
    "hardest_fm",
    "preferred_controls",
)

ADAPTIVE_SAMPLE_REQUIRED = (
    "prompt_id",
    "node_id",
    "boundary_id",
    "fm_id",
    "prompt_type",
    "prompt_summary",
    "source_refs",
    "model_predicted_rating",
    "user_rating",
    "delta",
    "created_at",
)

USER_RATING_VALUES = {1, 2, 3}
MODEL_PREDICTED_RATING_VALUES = {1, 2, 3}


# prompt_id grammar:
#   {node_id}/{boundary_id|none}/{fm_id|none}/{prompt_type}/{timestamp}-{shortid}
# - node_id: digits.digits (e.g., "1.1")
# - boundary_id / fm_id: letters/digits/dash, or literal "none"
# - prompt_type: one of PROMPT_TYPE_ENUM
# - timestamp: UTC basic format YYYYMMDDTHHMMSSZ
# - shortid: 6-10 lowercase alphanumeric
PROMPT_ID_REGEX = re.compile(
    r"^\d+\.\d+/(?:[A-Za-z0-9\-_.]+|none)/(?:[A-Za-z0-9\-_.]+|none)/"
    r"(?:code-snippet|incident|concept|bad-design|syntax-bridge|classification)/"
    r"\d{8}T\d{6}Z-[a-z0-9]{6,10}$"
)


# ---------- progress_update (builder output) ----------

# Builder must produce this object before the controller merges it into
# {progress_state}.
PROGRESS_UPDATE_REQUIRED_FIELDS = (
    "node_id",
    "project_name",
    "size",
    "entry_mode",
    "entry_fallback_reason",
    "investigation_focus",
    "adaptive_level",
    "adaptive_controls",
    "build_mode",
    "training_mode",
    "boundary_id",
    "seed_id",
    "cross_id",
    "project_type",
    "enterprise_slice",
    "domain",
    "io_shape",
    "artifact_shape",
    "core_flow",
    "primary_training",
    "secondary_training",
    "background_only",
    "primary_data_structures",
    "interaction_model",
    "mastery_signal",
    "out_of_scope",
    "concepts_covered",
    "user_questions_summary",
    "weakpoints_found",
    "teaching_slices_summary",
    "equipment_unlocked",
    "equipment_used",
    "fm_exposed",
    "fm_resolved",
    "transfer_evidence",
    "build_passed",
    "demo_passed",
    "teaching_questions",
    "assessment",
    "mastery_review",
    "next_project_bias",
)


# ---------- recommendation (start-project output) ----------

# Matches start-project.md §Recommendation Format (data layer) and the
# approved_recommendation block in build-project.md §Builder Input.
RECOMMENDATION_REQUIRED_FIELDS = (
    "source",
    "entry_mode",
    "training_mode",
    "boundary_id",
    "seed_id",
    "cross_id",
    "validation_status",
    "load_packet",
    "project_name",
    "size",
    "enterprise_slice",
    "incident_packet",
    "corpus_todo",
    "cold_open",
    "role_assignment",
    "story_hook",
    "case_conflict",
    "antagonist_design",
    "equipment_callback_candidate",
    "double_demo_plan",
    "adaptive_plan",
    "role_lens",
    "curiosity_trail",
    "project_type",
    "domain",
    "io_shape",
    "artifact_shape",
    "core_flow",
    "primary_training",
    "secondary_training",
    "background_only",
    "primary_data_structures",
    "interaction_model",
    "teaching_slice_candidates",
    "mastery_signal",
    "out_of_scope",
)

INCIDENT_PACKET_REQUIRED = ("kind", "artifact", "investigation_prompt")

DOUBLE_DEMO_PLAN_REQUIRED = ("supported",)
DOUBLE_DEMO_PLAN_CONDITIONAL = ("naive_command", "correct_command", "exposed_fm")

ADAPTIVE_PLAN_REQUIRED = ("current_level", "basis", "controls")


# ---------- status transitions ----------

# Allowed transitions per runtime-control.md §Progress Status Transitions.
# `idle -> idle` is allowed only as a no-op (we don't enforce that).
# `generating_recommendation` is a transient, in-memory-only step: `jr start`
# writes nothing before recommendation approval, so the persisted happy path is
# `idle -> selected`. Both `idle -> generating_recommendation` (if ever staged)
# and the persisted `idle -> selected` are allowed.
# Any transition to `idle` from selected/building/assessment_pending/paused is
# only valid after explicit abandonment; the validator flags such transitions
# for review but does not block them when called via --check-transition.
ALLOWED_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "idle": {"generating_recommendation", "selected"},
    "generating_recommendation": {"selected", "idle"},
    "selected": {"building", "paused", "idle"},
    "building": {"assessment_pending", "paused", "idle"},
    "assessment_pending": {"completed", "paused", "idle"},
    "paused": {"selected", "building", "assessment_pending", "idle"},
    "completed": {"idle"},
}

# Transitions that require explicit abandonment confirmation.
ABANDON_TRANSITIONS: set[tuple[str, str]] = {
    ("selected", "idle"),
    ("building", "idle"),
    ("assessment_pending", "idle"),
    ("paused", "idle"),
}


# ---------- regex helpers ----------

NODE_ID_REGEX = re.compile(r"^\d+\.\d+$")
BOUNDARY_ID_REGEX = re.compile(r"^B-[A-Za-z0-9\-]+$")
FM_ID_REGEX = re.compile(r"^FM-[A-Za-z0-9\-]+$")
ISO_DATETIME_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+\-]\d{2}:?\d{2})$"
)
ISO_DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
