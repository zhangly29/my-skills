"""Shape validators for Java Reading Project workspace data.

Four top-level entry points correspond to the four data shapes called out in
the SKILL:

- ``validate_progress_state``         -> progress-state.yaml
- ``validate_adaptive_training_data`` -> adaptive-training-data.yaml
- ``validate_progress_update``        -> builder progress_update object
- ``validate_recommendation``         -> start-project recommendation data layer

Each function appends human-readable error strings to a shared list. A list
of cross-shape policy checks (``run_policy_checks``) is run separately when the
caller passes ``--policy``.
"""

from __future__ import annotations

from typing import Any

from _checks import (
    check_adaptive_controls,
    require_bool,
    require_dict,
    require_enum,
    require_int,
    require_iso_date,
    require_iso_datetime,
    require_keys,
    require_list,
    require_number,
    require_regex,
    require_string,
    require_string_list,
)
from _schemas import (
    ABANDON_TRANSITIONS,
    ADAPTIVE_LEVEL_ENUM,
    ADAPTIVE_PLAN_REQUIRED,
    ADAPTIVE_PROFILE_REQUIRED,
    ADAPTIVE_SAMPLE_REQUIRED,
    ADAPTIVE_SUMMARY_REQUIRED,
    ADAPTIVE_TRAINING_TOP_REQUIRED,
    ALLOWED_STATUS_TRANSITIONS,
    ASSESSMENT_REQUIRED,
    ASSESSMENT_STATUS_ENUM,
    ASSESSMENT_SUBITEM_ENUM,
    BUILD_MODE_ENUM,
    COMPLETED_PROJECT_REQUIRED,
    CONFIDENCE_BAND_ENUM,
    DOUBLE_DEMO_PLAN_REQUIRED,
    ENTRY_MODE_ENUM,
    EQUIPMENT_REQUIRED,
    INCIDENT_KIND_ENUM,
    INCIDENT_PACKET_REQUIRED,
    INLINE_EQUIPMENT_REQUIRED,
    MASTERY_STATUS_ENUM,
    MODEL_PREDICTED_RATING_VALUES,
    NODE_ID_REGEX,
    NODE_MASTERY_ASSESSMENT_ENUM,
    NODE_MASTERY_REQUIRED,
    PROGRESS_REQUIRED_FIELDS,
    PROGRESS_STATE_TOP_OPTIONAL,
    PROGRESS_STATE_TOP_REQUIRED,
    PROGRESS_STATUS_ENUM,
    PROGRESS_UPDATE_REQUIRED_FIELDS,
    PROMPT_ID_REGEX,
    PROMPT_TYPE_ENUM,
    RECOMMENDATION_REQUIRED_FIELDS,
    SIZE_ENUM,
    TEACHING_MODE_ENUM,
    TRAINING_MODE_ENUM,
    USER_RATING_VALUES,
    VALIDATION_STATUS_ENUM,
    WEAKPOINT_REQUIRED,
    WEAKPOINT_STATUS_ENUM,
)


# ---------- progress-state.yaml ----------

def validate_progress_state(data: Any, errors: list[str]) -> None:
    path = "progress_state"
    if not require_dict(data, path, errors):
        return
    require_keys(data, PROGRESS_STATE_TOP_REQUIRED, path, errors)

    if "version" in data:
        require_int(data["version"], f"{path}.version", errors, minimum=1)

    if "progress" in data:
        _validate_progress_block(data["progress"], f"{path}.progress", errors)

    if "completed_projects" in data and data["completed_projects"] is not None:
        if require_list(data["completed_projects"], f"{path}.completed_projects", errors):
            for idx, entry in enumerate(data["completed_projects"]):
                _validate_completed_project(entry, f"{path}.completed_projects[{idx}]", errors)

    if "weakpoints" in data and data["weakpoints"] is not None:
        if require_list(data["weakpoints"], f"{path}.weakpoints", errors):
            for idx, entry in enumerate(data["weakpoints"]):
                _validate_weakpoint(entry, f"{path}.weakpoints[{idx}]", errors)

    if "node_mastery" in data and data["node_mastery"] is not None:
        if require_dict(data["node_mastery"], f"{path}.node_mastery", errors):
            for node_id, entry in data["node_mastery"].items():
                _validate_node_mastery(entry, f"{path}.node_mastery[{node_id!r}]", errors)

    if "equipment_unlocked" in data and data["equipment_unlocked"] is not None:
        if require_list(data["equipment_unlocked"], f"{path}.equipment_unlocked", errors):
            for idx, entry in enumerate(data["equipment_unlocked"]):
                _validate_workspace_equipment(entry, f"{path}.equipment_unlocked[{idx}]", errors)

    if "adaptive_summary" in data and data["adaptive_summary"] is not None:
        if require_dict(data["adaptive_summary"], f"{path}.adaptive_summary", errors):
            for node_id, entry in data["adaptive_summary"].items():
                _validate_adaptive_summary(entry, f"{path}.adaptive_summary[{node_id!r}]", errors)

    if "next_project_bias" in data and data["next_project_bias"] is not None:
        if require_dict(data["next_project_bias"], f"{path}.next_project_bias", errors):
            for node_id, entry in data["next_project_bias"].items():
                _validate_next_project_bias(entry, f"{path}.next_project_bias[{node_id!r}]", errors)

    extra = set(data) - set(PROGRESS_STATE_TOP_REQUIRED) - set(PROGRESS_STATE_TOP_OPTIONAL)
    if extra:
        errors.append(f"{path}: unexpected top-level keys {sorted(extra)}")


def _validate_progress_block(progress: Any, path: str, errors: list[str]) -> None:
    if not require_dict(progress, path, errors):
        return
    require_keys(progress, PROGRESS_REQUIRED_FIELDS, path, errors)

    status = progress.get("status")
    require_enum(status, PROGRESS_STATUS_ENUM, f"{path}.status", errors)

    require_enum(
        progress.get("current_size"), SIZE_ENUM, f"{path}.current_size", errors, allow_none=True
    )
    require_enum(
        progress.get("current_entry_mode"),
        ENTRY_MODE_ENUM,
        f"{path}.current_entry_mode",
        errors,
        allow_none=True,
    )
    require_enum(
        progress.get("current_adaptive_level"),
        ADAPTIVE_LEVEL_ENUM,
        f"{path}.current_adaptive_level",
        errors,
        allow_none=True,
    )
    require_enum(
        progress.get("teaching_mode"), TEACHING_MODE_ENUM, f"{path}.teaching_mode", errors
    )
    require_enum(progress.get("build_mode"), BUILD_MODE_ENUM, f"{path}.build_mode", errors)

    if progress.get("current_node") is not None:
        require_regex(
            progress["current_node"], NODE_ID_REGEX, f"{path}.current_node", errors
        )

    if progress.get("current_adaptive_controls") is not None:
        check_adaptive_controls(
            progress["current_adaptive_controls"],
            f"{path}.current_adaptive_controls",
            errors,
        )

    require_string(progress.get("current_project"), f"{path}.current_project", errors, allow_none=True)
    require_string(progress.get("current_milestone"), f"{path}.current_milestone", errors, allow_none=True)
    require_string(progress.get("current_slice"), f"{path}.current_slice", errors, allow_none=True)
    require_string(
        progress.get("current_investigation_focus"),
        f"{path}.current_investigation_focus",
        errors,
        allow_none=True,
    )
    require_string(
        progress.get("current_follow_block"), f"{path}.current_follow_block", errors, allow_none=True
    )
    require_iso_datetime(progress.get("paused_at"), f"{path}.paused_at", errors, allow_none=True)
    require_string(progress.get("pause_reason"), f"{path}.pause_reason", errors, allow_none=True)

    # Active-state coherence: paused requires current_project; building requires current_slice.
    if status == "paused" and progress.get("current_project") is None:
        errors.append(f"{path}: status=paused requires current_project to be set")
    if status == "building" and progress.get("current_slice") is None:
        errors.append(f"{path}: status=building requires current_slice to be set")
    if status in {"selected", "building", "assessment_pending", "paused"} and (
        progress.get("current_project") is None
    ):
        errors.append(f"{path}: status={status} requires current_project to be set")


def _validate_completed_project(entry: Any, path: str, errors: list[str]) -> None:
    if not require_dict(entry, path, errors):
        return
    require_keys(entry, COMPLETED_PROJECT_REQUIRED, path, errors)

    require_regex(entry.get("node_id"), NODE_ID_REGEX, f"{path}.node_id", errors)
    require_enum(entry.get("size"), SIZE_ENUM, f"{path}.size", errors)
    require_enum(entry.get("entry_mode"), ENTRY_MODE_ENUM, f"{path}.entry_mode", errors)
    require_enum(entry.get("adaptive_level"), ADAPTIVE_LEVEL_ENUM, f"{path}.adaptive_level", errors)
    require_enum(entry.get("build_mode"), BUILD_MODE_ENUM, f"{path}.build_mode", errors)
    require_enum(entry.get("training_mode"), TRAINING_MODE_ENUM, f"{path}.training_mode", errors)
    require_bool(entry.get("build_passed"), f"{path}.build_passed", errors)
    require_bool(entry.get("demo_passed"), f"{path}.demo_passed", errors)
    require_string(entry.get("project_name"), f"{path}.project_name", errors)
    require_string(entry.get("boundary_id"), f"{path}.boundary_id", errors)
    require_string(entry.get("seed_id"), f"{path}.seed_id", errors)
    require_string(entry.get("cross_id"), f"{path}.cross_id", errors, allow_none=True)

    if entry.get("adaptive_controls") is not None:
        check_adaptive_controls(entry["adaptive_controls"], f"{path}.adaptive_controls", errors)

    # list-of-strings fields
    for key in (
        "primary_training",
        "secondary_training",
        "background_only",
        "primary_data_structures",
        "out_of_scope",
        "concepts_covered",
        "user_questions_summary",
        "weakpoints_found",
        "teaching_slices_summary",
        "fm_exposed",
        "fm_resolved",
    ):
        if key in entry:
            require_string_list(entry[key], f"{path}.{key}", errors)

    # equipment_unlocked[] (inline)
    if "equipment_unlocked" in entry and require_list(
        entry["equipment_unlocked"], f"{path}.equipment_unlocked", errors
    ):
        for idx, eq in enumerate(entry["equipment_unlocked"]):
            _validate_inline_equipment(eq, f"{path}.equipment_unlocked[{idx}]", errors)

    # equipment_used object
    if "equipment_used" in entry:
        _validate_count_examples(entry["equipment_used"], f"{path}.equipment_used", errors)

    # transfer_evidence object
    if "transfer_evidence" in entry:
        _validate_count_examples(entry["transfer_evidence"], f"{path}.transfer_evidence", errors)

    # teaching_questions object
    tq = entry.get("teaching_questions")
    if require_dict(tq, f"{path}.teaching_questions", errors):
        require_int(tq.get("answered"), f"{path}.teaching_questions.answered", errors, minimum=0)
        require_int(tq.get("unanswered"), f"{path}.teaching_questions.unanswered", errors, minimum=0)

    # assessment object
    if "assessment" in entry:
        _validate_assessment(entry["assessment"], f"{path}.assessment", errors)


def _validate_inline_equipment(eq: Any, path: str, errors: list[str]) -> None:
    if not require_dict(eq, path, errors):
        return
    require_keys(eq, INLINE_EQUIPMENT_REQUIRED, path, errors)
    require_string(eq.get("name"), f"{path}.name", errors)
    require_string(eq.get("source_slice"), f"{path}.source_slice", errors)
    require_string(eq.get("use_sentence"), f"{path}.use_sentence", errors)
    require_string_list(eq.get("transfer_contexts"), f"{path}.transfer_contexts", errors, min_len=1)
    require_string_list(eq.get("code_evidence"), f"{path}.code_evidence", errors, min_len=1)


def _validate_workspace_equipment(eq: Any, path: str, errors: list[str]) -> None:
    if not require_dict(eq, path, errors):
        return
    require_keys(eq, EQUIPMENT_REQUIRED, path, errors)
    require_string(eq.get("name"), f"{path}.name", errors)
    require_regex(eq.get("node_id"), NODE_ID_REGEX, f"{path}.node_id", errors)
    require_string(eq.get("source_slice"), f"{path}.source_slice", errors)
    require_string(eq.get("use_sentence"), f"{path}.use_sentence", errors)
    require_string_list(eq.get("transfer_contexts"), f"{path}.transfer_contexts", errors, min_len=1)
    require_string_list(eq.get("code_evidence"), f"{path}.code_evidence", errors, min_len=1)
    if eq.get("unlocked_at") is not None:
        require_iso_datetime(eq["unlocked_at"], f"{path}.unlocked_at", errors, allow_none=True)
    if eq.get("last_used_at") is not None:
        require_iso_datetime(eq["last_used_at"], f"{path}.last_used_at", errors, allow_none=True)
    if "use_count" in eq:
        require_int(eq.get("use_count"), f"{path}.use_count", errors, minimum=0)


def _validate_count_examples(obj: Any, path: str, errors: list[str]) -> None:
    if not require_dict(obj, path, errors):
        return
    require_int(obj.get("count"), f"{path}.count", errors, minimum=0)
    if "examples" in obj:
        require_string_list(obj["examples"], f"{path}.examples", errors)


def _validate_assessment(assessment: Any, path: str, errors: list[str]) -> None:
    if not require_dict(assessment, path, errors):
        return
    require_keys(assessment, ASSESSMENT_REQUIRED, path, errors)
    require_enum(assessment.get("status"), ASSESSMENT_STATUS_ENUM, f"{path}.status", errors)
    for subitem in (
        "main_flow_reconstruction",
        "boundary_ownership",
        "failure_classification",
        "bad_design_diagnosis",
        "transfer_check",
    ):
        require_enum(assessment.get(subitem), ASSESSMENT_SUBITEM_ENUM, f"{path}.{subitem}", errors)
    if "evidence_summary" in assessment:
        require_string_list(assessment["evidence_summary"], f"{path}.evidence_summary", errors)


def _validate_weakpoint(entry: Any, path: str, errors: list[str]) -> None:
    if not require_dict(entry, path, errors):
        return
    require_keys(entry, WEAKPOINT_REQUIRED, path, errors)
    require_regex(entry.get("node_id"), NODE_ID_REGEX, f"{path}.node_id", errors)
    require_enum(entry.get("status"), WEAKPOINT_STATUS_ENUM, f"{path}.status", errors)
    require_string(entry.get("boundary_id"), f"{path}.boundary_id", errors)
    require_string(entry.get("concept"), f"{path}.concept", errors)
    require_string(entry.get("issue"), f"{path}.issue", errors)
    require_string(entry.get("evidence"), f"{path}.evidence", errors)
    require_string(entry.get("source_project"), f"{path}.source_project", errors)
    require_iso_date(entry.get("last_seen"), f"{path}.last_seen", errors)
    if "evidence_refs" in entry and require_list(
        entry["evidence_refs"], f"{path}.evidence_refs", errors
    ):
        for idx, ref in enumerate(entry["evidence_refs"]):
            if not require_dict(ref, f"{path}.evidence_refs[{idx}]", errors):
                continue
            require_string(ref.get("project"), f"{path}.evidence_refs[{idx}].project", errors)
            require_string(ref.get("file"), f"{path}.evidence_refs[{idx}].file", errors)
            require_string(ref.get("slice"), f"{path}.evidence_refs[{idx}].slice", errors)


def _validate_node_mastery(entry: Any, path: str, errors: list[str]) -> None:
    if not require_dict(entry, path, errors):
        return
    require_keys(entry, NODE_MASTERY_REQUIRED, path, errors)
    require_enum(entry.get("status"), MASTERY_STATUS_ENUM, f"{path}.status", errors)
    require_enum(entry.get("assessment"), NODE_MASTERY_ASSESSMENT_ENUM, f"{path}.assessment", errors)
    require_string_list(
        entry.get("completed_required_boundaries"),
        f"{path}.completed_required_boundaries",
        errors,
    )
    require_string_list(
        entry.get("remaining_required_boundaries"),
        f"{path}.remaining_required_boundaries",
        errors,
    )
    require_string(entry.get("note"), f"{path}.note", errors)
    if entry.get("evidence_limited_estimate") is not None:
        require_string(
            entry["evidence_limited_estimate"],
            f"{path}.evidence_limited_estimate",
            errors,
            allow_none=True,
        )


def _validate_adaptive_summary(entry: Any, path: str, errors: list[str]) -> None:
    if not require_dict(entry, path, errors):
        return
    require_keys(entry, ADAPTIVE_SUMMARY_REQUIRED, path, errors)
    require_iso_datetime(entry.get("asked_at"), f"{path}.asked_at", errors)
    require_int(entry.get("sample_count"), f"{path}.sample_count", errors, minimum=0)
    # workspace-level adaptive_summary uses confidence band enum
    require_enum(entry.get("confidence"), CONFIDENCE_BAND_ENUM, f"{path}.confidence", errors)
    require_number(entry.get("target_rating"), f"{path}.target_rating", errors, minimum=1.0, maximum=3.0)
    require_enum(entry.get("current_level"), ADAPTIVE_LEVEL_ENUM, f"{path}.current_level", errors)
    require_string_list(entry.get("strongest_boundaries"), f"{path}.strongest_boundaries", errors)
    require_string_list(entry.get("hardest_boundaries"), f"{path}.hardest_boundaries", errors)
    require_string_list(entry.get("hardest_fm"), f"{path}.hardest_fm", errors)
    check_adaptive_controls(entry.get("preferred_controls"), f"{path}.preferred_controls", errors)


def _validate_next_project_bias(entry: Any, path: str, errors: list[str]) -> None:
    if not require_dict(entry, path, errors):
        return
    # All fields optional, but at least one of prefer_boundary/prefer/avoid should be set.
    has_signal = any(k in entry for k in ("prefer_boundary", "prefer", "avoid"))
    if not has_signal:
        errors.append(f"{path}: expected at least one of prefer_boundary/prefer/avoid")
    if "prefer" in entry:
        require_string_list(entry["prefer"], f"{path}.prefer", errors)
    if "avoid" in entry:
        require_string_list(entry["avoid"], f"{path}.avoid", errors)
    if "prefer_boundary" in entry:
        require_string(entry["prefer_boundary"], f"{path}.prefer_boundary", errors)
    if "reason" in entry:
        require_string(entry["reason"], f"{path}.reason", errors)
    if "suggested_command" in entry:
        require_string(entry["suggested_command"], f"{path}.suggested_command", errors)


# ---------- adaptive-training-data.yaml ----------

def validate_adaptive_training_data(data: Any, errors: list[str]) -> None:
    path = "adaptive_training_data"
    if not require_dict(data, path, errors):
        return
    require_keys(data, ADAPTIVE_TRAINING_TOP_REQUIRED, path, errors)
    require_int(data.get("version"), f"{path}.version", errors, minimum=1)

    nodes = data.get("nodes")
    if nodes is None or not nodes:
        return  # empty nodes map is valid (fresh workspace)
    if not require_dict(nodes, f"{path}.nodes", errors):
        return

    for node_id, node in nodes.items():
        node_path = f"{path}.nodes[{node_id!r}]"
        if not require_regex(node_id, NODE_ID_REGEX, f"{node_path}.<key>", errors):
            continue
        if not require_dict(node, node_path, errors):
            continue
        _validate_adaptive_profile(node.get("profile"), f"{node_path}.profile", errors)
        samples = node.get("samples", [])
        if require_list(samples, f"{node_path}.samples", errors):
            seen_prompt_ids: set[str] = set()
            for idx, sample in enumerate(samples):
                _validate_adaptive_sample(
                    sample, f"{node_path}.samples[{idx}]", errors, node_id, seen_prompt_ids
                )


def _validate_adaptive_profile(profile: Any, path: str, errors: list[str]) -> None:
    if not require_dict(profile, path, errors):
        return
    require_keys(profile, ADAPTIVE_PROFILE_REQUIRED, path, errors)
    require_iso_datetime(profile.get("asked_at"), f"{path}.asked_at", errors)
    require_int(profile.get("sample_count"), f"{path}.sample_count", errors, minimum=0)
    # adaptive-training-data uses float confidence in [0, 1]
    require_number(profile.get("confidence"), f"{path}.confidence", errors, minimum=0.0, maximum=1.0)
    require_number(profile.get("target_rating"), f"{path}.target_rating", errors, minimum=1.0, maximum=3.0)
    require_enum(profile.get("current_level"), ADAPTIVE_LEVEL_ENUM, f"{path}.current_level", errors)
    require_string_list(profile.get("strongest_boundaries"), f"{path}.strongest_boundaries", errors)
    require_string_list(profile.get("hardest_boundaries"), f"{path}.hardest_boundaries", errors)
    require_string_list(profile.get("hardest_fm"), f"{path}.hardest_fm", errors)
    check_adaptive_controls(profile.get("preferred_controls"), f"{path}.preferred_controls", errors)


def _validate_adaptive_sample(
    sample: Any,
    path: str,
    errors: list[str],
    expected_node_id: str,
    seen_prompt_ids: set[str],
) -> None:
    if not require_dict(sample, path, errors):
        return
    require_keys(sample, ADAPTIVE_SAMPLE_REQUIRED, path, errors)

    prompt_id = sample.get("prompt_id")
    if isinstance(prompt_id, str):
        require_regex(prompt_id, PROMPT_ID_REGEX, f"{path}.prompt_id", errors)
        if prompt_id in seen_prompt_ids:
            errors.append(f"{path}.prompt_id: duplicate prompt_id {prompt_id!r}")
        seen_prompt_ids.add(prompt_id)

    if sample.get("node_id") != expected_node_id:
        errors.append(
            f"{path}.node_id: expected {expected_node_id!r}, got {sample.get('node_id')!r}"
        )

    require_enum(sample.get("prompt_type"), PROMPT_TYPE_ENUM, f"{path}.prompt_type", errors)
    require_string(sample.get("boundary_id"), f"{path}.boundary_id", errors)
    require_string(sample.get("fm_id"), f"{path}.fm_id", errors)
    require_string(sample.get("prompt_summary"), f"{path}.prompt_summary", errors)
    require_string_list(sample.get("source_refs"), f"{path}.source_refs", errors, min_len=1)
    require_enum(
        sample.get("model_predicted_rating"),
        MODEL_PREDICTED_RATING_VALUES,
        f"{path}.model_predicted_rating",
        errors,
    )
    require_enum(sample.get("user_rating"), USER_RATING_VALUES, f"{path}.user_rating", errors)
    require_iso_datetime(sample.get("created_at"), f"{path}.created_at", errors)

    # delta consistency check
    predicted = sample.get("model_predicted_rating")
    actual = sample.get("user_rating")
    delta = sample.get("delta")
    if (
        isinstance(predicted, int)
        and isinstance(actual, int)
        and isinstance(delta, int)
        and delta != actual - predicted
    ):
        errors.append(
            f"{path}.delta: expected {actual - predicted} (user_rating - model_predicted_rating), got {delta}"
        )


# ---------- progress_update (builder output) ----------

def validate_progress_update(data: Any, errors: list[str]) -> None:
    """Reuses _validate_completed_project — same field contract minus 'next_project_bias' which is sibling."""
    path = "progress_update"
    if not require_dict(data, path, errors):
        return
    require_keys(data, PROGRESS_UPDATE_REQUIRED_FIELDS, path, errors)

    # Validate the body via completed_project rules (it merges into completed_projects[]).
    body = {k: v for k, v in data.items() if k != "next_project_bias"}
    _validate_completed_project(body, path, errors)

    # next_project_bias must be a map keyed by node_id.
    npb = data.get("next_project_bias")
    if npb is None:
        return
    if not require_dict(npb, f"{path}.next_project_bias", errors):
        return
    for node_id, entry in npb.items():
        _validate_next_project_bias(entry, f"{path}.next_project_bias[{node_id!r}]", errors)


# ---------- recommendation ----------

def validate_recommendation(data: Any, errors: list[str]) -> None:
    """Validates the data layer of a recommendation (post-approval = approved_recommendation)."""
    path = "recommendation"
    if not require_dict(data, path, errors):
        return

    # Accept either a top-level `recommendation:` or `approved_recommendation:` wrapper,
    # or a flat dict. Unwrap if wrapped.
    if "recommendation" in data and isinstance(data["recommendation"], dict) and len(data) == 1:
        data = data["recommendation"]
    elif "approved_recommendation" in data and isinstance(data["approved_recommendation"], dict) and len(data) == 1:
        data = data["approved_recommendation"]

    require_keys(data, RECOMMENDATION_REQUIRED_FIELDS, path, errors)

    require_enum(data.get("source"), {"corpus"}, f"{path}.source", errors)
    require_enum(data.get("entry_mode"), ENTRY_MODE_ENUM, f"{path}.entry_mode", errors)
    require_enum(data.get("training_mode"), TRAINING_MODE_ENUM, f"{path}.training_mode", errors)
    require_enum(
        data.get("validation_status"), VALIDATION_STATUS_ENUM, f"{path}.validation_status", errors
    )
    require_enum(data.get("size"), SIZE_ENUM, f"{path}.size", errors)
    require_string(data.get("project_name"), f"{path}.project_name", errors)
    require_string(data.get("boundary_id"), f"{path}.boundary_id", errors, allow_none=True)
    require_string(data.get("seed_id"), f"{path}.seed_id", errors, allow_none=True)
    require_string(data.get("cross_id"), f"{path}.cross_id", errors, allow_none=True)

    # load_packet
    lp = data.get("load_packet")
    if require_dict(lp, f"{path}.load_packet", errors):
        require_string_list(lp.get("required"), f"{path}.load_packet.required", errors, min_len=1)

    # incident_packet
    ip = data.get("incident_packet")
    if require_dict(ip, f"{path}.incident_packet", errors):
        require_keys(ip, INCIDENT_PACKET_REQUIRED, f"{path}.incident_packet", errors)
        require_enum(ip.get("kind"), INCIDENT_KIND_ENUM, f"{path}.incident_packet.kind", errors)
        # When kind=not_supported, corpus_todo must be set.
        if ip.get("kind") == "not_supported":
            if not data.get("corpus_todo"):
                errors.append(
                    f"{path}.corpus_todo: required when incident_packet.kind=not_supported"
                )

    # double_demo_plan
    ddp = data.get("double_demo_plan")
    if require_dict(ddp, f"{path}.double_demo_plan", errors):
        require_keys(ddp, DOUBLE_DEMO_PLAN_REQUIRED, f"{path}.double_demo_plan", errors)
        require_bool(ddp.get("supported"), f"{path}.double_demo_plan.supported", errors)
        if ddp.get("supported") is True:
            for k in ("naive_command", "correct_command", "exposed_fm"):
                if k not in ddp:
                    errors.append(f"{path}.double_demo_plan: missing '{k}' when supported=true")
            if "exposed_fm" in ddp:
                require_string_list(ddp["exposed_fm"], f"{path}.double_demo_plan.exposed_fm", errors)

    # adaptive_plan
    ap = data.get("adaptive_plan")
    if require_dict(ap, f"{path}.adaptive_plan", errors):
        require_keys(ap, ADAPTIVE_PLAN_REQUIRED, f"{path}.adaptive_plan", errors)
        require_enum(
            ap.get("current_level"), ADAPTIVE_LEVEL_ENUM, f"{path}.adaptive_plan.current_level", errors
        )
        require_string_list(ap.get("basis"), f"{path}.adaptive_plan.basis", errors, min_len=1)
        check_adaptive_controls(ap.get("controls"), f"{path}.adaptive_plan.controls", errors)

    # array fields
    require_string_list(
        data.get("role_lens"), f"{path}.role_lens", errors, min_len=2, max_len=4
    )
    require_string_list(
        data.get("curiosity_trail"), f"{path}.curiosity_trail", errors, min_len=2, max_len=4
    )
    require_string_list(
        data.get("teaching_slice_candidates"),
        f"{path}.teaching_slice_candidates",
        errors,
        min_len=3,
        max_len=6,
    )
    require_string_list(
        data.get("primary_training"), f"{path}.primary_training", errors, min_len=1, max_len=2
    )
    for key in (
        "secondary_training",
        "background_only",
        "primary_data_structures",
        "out_of_scope",
    ):
        if key in data:
            require_string_list(data[key], f"{path}.{key}", errors)

    # equipment_callback_candidate: list[string] or null
    eqcb = data.get("equipment_callback_candidate")
    if eqcb is not None:
        require_string_list(eqcb, f"{path}.equipment_callback_candidate", errors, max_len=3)


# ---------- transition check ----------

def check_status_transition(from_status: str, to_status: str, errors: list[str]) -> None:
    """Validate that a single status transition is permitted by runtime-control.md."""
    if from_status not in ALLOWED_STATUS_TRANSITIONS:
        errors.append(f"transition: unknown source status {from_status!r}")
        return
    allowed = ALLOWED_STATUS_TRANSITIONS[from_status]
    if to_status not in allowed:
        errors.append(
            f"transition: {from_status!r} -> {to_status!r} not allowed; "
            f"allowed: {sorted(allowed)}"
        )
        return
    if (from_status, to_status) in ABANDON_TRANSITIONS:
        errors.append(
            f"transition: {from_status!r} -> {to_status!r} requires explicit abandonment confirmation"
        )


# ---------- cross-shape policy checks ----------

def run_policy_checks(
    state: Any,
    adaptive: Any,
    errors: list[str],
) -> None:
    """Run non-structural policy checks. Each function appends to errors."""
    if isinstance(state, dict):
        _policy_assessment_subitem_consistency(state, errors)
        _policy_equipment_consistency(state, errors)
        _policy_no_duplicate_active_project(state, errors)
        _policy_completed_project_uniqueness(state, errors)
    if isinstance(state, dict) and isinstance(adaptive, dict):
        _policy_no_stretch_without_assessment(state, adaptive, errors)


def _policy_assessment_subitem_consistency(state: dict, errors: list[str]) -> None:
    """assessment.status=completed forbids subitems remaining 'pending'."""
    for idx, entry in enumerate(state.get("completed_projects") or []):
        if not isinstance(entry, dict):
            continue
        assessment = entry.get("assessment", {})
        if not isinstance(assessment, dict):
            continue
        if assessment.get("status") == "completed":
            for sub in (
                "main_flow_reconstruction",
                "boundary_ownership",
                "failure_classification",
                "bad_design_diagnosis",
                "transfer_check",
            ):
                if assessment.get(sub) == "pending":
                    errors.append(
                        f"policy[assessment_subitem]: "
                        f"completed_projects[{idx}].assessment.{sub}=pending "
                        f"contradicts status=completed"
                    )


def _policy_equipment_consistency(state: dict, errors: list[str]) -> None:
    """Workspace equipment_unlocked must reference equipment defined in some completed_project entry."""
    workspace_equipment = state.get("equipment_unlocked") or []
    completed = state.get("completed_projects") or []

    inline_equipment: dict[tuple[str, str], dict] = {}
    for entry in completed:
        if not isinstance(entry, dict):
            continue
        project_name = entry.get("project_name")
        for eq in entry.get("equipment_unlocked") or []:
            if isinstance(eq, dict) and "name" in eq and "source_slice" in eq:
                inline_equipment[(eq["name"], eq["source_slice"])] = {
                    "project_name": project_name,
                    "transfer_contexts": eq.get("transfer_contexts", []),
                }

    for idx, ws in enumerate(workspace_equipment):
        if not isinstance(ws, dict):
            continue
        key = (ws.get("name"), ws.get("source_slice"))
        if key not in inline_equipment:
            errors.append(
                f"policy[equipment]: workspace equipment_unlocked[{idx}] "
                f"name={ws.get('name')!r} source_slice={ws.get('source_slice')!r} "
                f"has no matching entry in any completed_projects[].equipment_unlocked"
            )


def _policy_no_duplicate_active_project(state: dict, errors: list[str]) -> None:
    """progress.current_project must not appear in completed_projects unless progress.status=completed."""
    progress = state.get("progress") or {}
    current = progress.get("current_project")
    status = progress.get("status")
    if not current:
        return
    completed_names = {
        e.get("project_name") for e in (state.get("completed_projects") or []) if isinstance(e, dict)
    }
    if current in completed_names and status not in {"completed", "idle"}:
        errors.append(
            f"policy[active_project]: progress.current_project={current!r} is already in "
            f"completed_projects, but progress.status={status!r} (expected completed or idle)"
        )


def _policy_completed_project_uniqueness(state: dict, errors: list[str]) -> None:
    """completed_projects[].project_name must be unique."""
    seen: dict[str, int] = {}
    for idx, entry in enumerate(state.get("completed_projects") or []):
        if not isinstance(entry, dict):
            continue
        name = entry.get("project_name")
        if not isinstance(name, str):
            continue
        if name in seen:
            errors.append(
                f"policy[uniqueness]: completed_projects[{idx}].project_name={name!r} "
                f"duplicates completed_projects[{seen[name]}]"
            )
        else:
            seen[name] = idx


def _policy_no_stretch_without_assessment(state: dict, adaptive: dict, errors: list[str]) -> None:
    """A node may set adaptive current_level=stretch only after a completed assessment.

    Reflects adaptive-difficulty.md: ask data alone may set supportive or standard;
    do not set stretch without assessment evidence or explicit transfer evidence.
    """
    nodes = (adaptive.get("nodes") or {}) if isinstance(adaptive, dict) else {}
    completed = state.get("completed_projects") or []
    completed_assessments_by_node: dict[str, set[str]] = {}
    for entry in completed:
        if not isinstance(entry, dict):
            continue
        node_id = entry.get("node_id")
        status = (entry.get("assessment") or {}).get("status")
        if isinstance(node_id, str) and status == "completed":
            completed_assessments_by_node.setdefault(node_id, set()).add(entry.get("project_name") or "")

    for node_id, node_data in nodes.items():
        if not isinstance(node_data, dict):
            continue
        profile = node_data.get("profile") or {}
        if profile.get("current_level") == "stretch":
            if node_id not in completed_assessments_by_node:
                errors.append(
                    f"policy[stretch]: adaptive_training_data.nodes[{node_id!r}].profile.current_level=stretch "
                    f"but no completed_projects entry with assessment.status=completed for node {node_id!r}"
                )

    # Same check against workspace adaptive_summary
    for node_id, summary in (state.get("adaptive_summary") or {}).items():
        if isinstance(summary, dict) and summary.get("current_level") == "stretch":
            if node_id not in completed_assessments_by_node:
                errors.append(
                    f"policy[stretch]: progress_state.adaptive_summary[{node_id!r}].current_level=stretch "
                    f"but no completed_projects entry with assessment.status=completed for node {node_id!r}"
                )
