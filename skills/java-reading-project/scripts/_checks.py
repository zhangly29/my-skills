"""Validation helpers used by `_shapes.py`.

Style follows java-reading-corpus/tools/validate-corpus.py: accumulate errors
into a list, never raise. Each helper appends one descriptive message per
violation and returns. Callers decide when to short-circuit.

The `path` argument in every helper is a human-readable JSON-path-like string
(e.g., "progress.current_adaptive_controls.explanation_density") used in error
messages. Keep paths absolute from the document root.
"""

from __future__ import annotations

import re
from typing import Any, Iterable


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def require_dict(value: Any, path: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected mapping, got {type(value).__name__}")
        return False
    return True


def require_list(value: Any, path: str, errors: list[str]) -> bool:
    if not isinstance(value, list):
        errors.append(f"{path}: expected list, got {type(value).__name__}")
        return False
    return True


def require_string(value: Any, path: str, errors: list[str], allow_none: bool = False) -> bool:
    if value is None and allow_none:
        return True
    if not isinstance(value, str):
        errors.append(f"{path}: expected string, got {type(value).__name__}")
        return False
    return True


def require_bool(value: Any, path: str, errors: list[str]) -> bool:
    if not isinstance(value, bool):
        errors.append(f"{path}: expected bool, got {type(value).__name__}")
        return False
    return True


def require_int(
    value: Any,
    path: str,
    errors: list[str],
    minimum: int | None = None,
    maximum: int | None = None,
) -> bool:
    # bool is a subclass of int in Python — reject it explicitly.
    if isinstance(value, bool) or not isinstance(value, int):
        errors.append(f"{path}: expected int, got {type(value).__name__}")
        return False
    if minimum is not None and value < minimum:
        errors.append(f"{path}: expected >= {minimum}, got {value}")
        return False
    if maximum is not None and value > maximum:
        errors.append(f"{path}: expected <= {maximum}, got {value}")
        return False
    return True


def require_number(
    value: Any,
    path: str,
    errors: list[str],
    minimum: float | None = None,
    maximum: float | None = None,
) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{path}: expected number, got {type(value).__name__}")
        return False
    if minimum is not None and value < minimum:
        errors.append(f"{path}: expected >= {minimum}, got {value}")
        return False
    if maximum is not None and value > maximum:
        errors.append(f"{path}: expected <= {maximum}, got {value}")
        return False
    return True


def require_keys(
    obj: dict,
    required: Iterable[str],
    path: str,
    errors: list[str],
) -> None:
    """Every key in `required` must be present in `obj` (value may be null)."""
    for key in required:
        if key not in obj:
            errors.append(f"{path}: missing required field '{key}'")


def require_enum(
    value: Any,
    allowed: set[str] | set[int],
    path: str,
    errors: list[str],
    allow_none: bool = False,
) -> bool:
    if value is None:
        if allow_none:
            return True
        errors.append(f"{path}: null is not allowed; expected one of {sorted(allowed)}")
        return False
    if value not in allowed:
        errors.append(f"{path}: {value!r} not in {sorted(allowed)}")
        return False
    return True


def require_regex(
    value: Any,
    pattern: re.Pattern[str],
    path: str,
    errors: list[str],
) -> bool:
    if not isinstance(value, str):
        errors.append(f"{path}: expected string for regex match, got {type(value).__name__}")
        return False
    if not pattern.match(value):
        errors.append(f"{path}: {value!r} does not match expected format {pattern.pattern}")
        return False
    return True


def require_iso_datetime(value: Any, path: str, errors: list[str], allow_none: bool = False) -> bool:
    from _schemas import ISO_DATETIME_REGEX

    if value is None and allow_none:
        return True
    return require_regex(value, ISO_DATETIME_REGEX, path, errors)


def require_iso_date(value: Any, path: str, errors: list[str], allow_none: bool = False) -> bool:
    from _schemas import ISO_DATE_REGEX

    if value is None and allow_none:
        return True
    return require_regex(value, ISO_DATE_REGEX, path, errors)


def require_string_list(
    value: Any,
    path: str,
    errors: list[str],
    min_len: int = 0,
    max_len: int | None = None,
    item_pattern: re.Pattern[str] | None = None,
) -> bool:
    if not require_list(value, path, errors):
        return False
    if len(value) < min_len:
        errors.append(f"{path}: expected >= {min_len} items, got {len(value)}")
        return False
    if max_len is not None and len(value) > max_len:
        errors.append(f"{path}: expected <= {max_len} items, got {len(value)}")
        return False
    ok = True
    for idx, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{path}[{idx}]: expected string, got {type(item).__name__}")
            ok = False
            continue
        if item_pattern is not None and not item_pattern.match(item):
            errors.append(
                f"{path}[{idx}]: {item!r} does not match {item_pattern.pattern}"
            )
            ok = False
    return ok


def check_adaptive_controls(controls: Any, path: str, errors: list[str]) -> None:
    """Validate the 5-field adaptive_controls object against ADAPTIVE_CONTROLS_ENUMS."""
    from _schemas import ADAPTIVE_CONTROLS_ENUMS

    if not require_dict(controls, path, errors):
        return
    for field, allowed in ADAPTIVE_CONTROLS_ENUMS.items():
        if field not in controls:
            errors.append(f"{path}: missing required field '{field}'")
            continue
        require_enum(controls[field], allowed, f"{path}.{field}", errors)
    extra = set(controls) - set(ADAPTIVE_CONTROLS_ENUMS)
    if extra:
        errors.append(f"{path}: unexpected fields {sorted(extra)}")
