#!/usr/bin/env python3
"""Validate Java Reading Project workspace YAML data shapes.

This CLI validates the data contracts described in:

- runtime-control.md  §Progress Data Shapes        -> progress-state.yaml
- adaptive-difficulty.md §Data Shape               -> adaptive-training-data.yaml
- runtime-control.md  §Progress Update Required... -> progress_update (builder output)
- start-project.md    §Recommendation Format       -> recommendation (data layer)

Examples:

    # Validate workspace state files
    uv run python validate-progress.py --state ../../progress-state.yaml
    uv run python validate-progress.py --adaptive ../../adaptive-training-data.yaml

    # Validate builder intermediates from stdin
    cat /tmp/update.yaml | uv run python validate-progress.py --progress-update -
    cat /tmp/rec.yaml    | uv run python validate-progress.py --recommendation -

    # Auto-discover all known files in a workspace
    uv run python validate-progress.py --all /home/me/project/java-read

    # Cross-shape policy checks (in addition to structural validation)
    uv run python validate-progress.py --all /home/me/project/java-read --policy

    # Check that a single status transition is permitted
    uv run python validate-progress.py --check-transition selected:building

Exit codes:
    0 — all selected validations passed
    1 — at least one validation failed
    2 — usage error (e.g., no flags, file missing)

Output: human-readable; errors aggregated and printed together. See
``java-reading-corpus/tools/validate-corpus.py`` for the matching style.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

# Allow this script to be invoked from anywhere by ensuring its directory is on
# the import path for the sibling _schemas / _checks / _shapes modules.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _shapes import (  # noqa: E402  (after sys.path tweak)
    check_status_transition,
    run_policy_checks,
    validate_adaptive_training_data,
    validate_progress_state,
    validate_progress_update,
    validate_recommendation,
)


def load_yaml_input(source: str) -> Any:
    """Load YAML from a path or '-' (stdin)."""
    if source == "-":
        text = sys.stdin.read()
        if not text.strip():
            raise ValueError("empty stdin input")
        return yaml.safe_load(text)
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {source}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def report(errors: list[str], label: str) -> int:
    """Print errors for a validation pass and return 0 or 1."""
    if errors:
        print(f"{label}: validation failed")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"{label}: validation passed")
    return 0


def discover_workspace_files(workspace: Path) -> dict[str, Path | None]:
    """Find the known files in a workspace directory."""
    return {
        "state": workspace / "progress-state.yaml" if (workspace / "progress-state.yaml").exists() else None,
        "adaptive": workspace / "adaptive-training-data.yaml" if (workspace / "adaptive-training-data.yaml").exists() else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="validate-progress.py",
        description="Validate Java Reading Project workspace YAML data shapes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Pass '-' as the value of --progress-update or --recommendation to "
            "read from stdin."
        ),
    )
    parser.add_argument("--state", type=str, help="path to progress-state.yaml")
    parser.add_argument("--adaptive", type=str, help="path to adaptive-training-data.yaml")
    parser.add_argument(
        "--progress-update",
        type=str,
        dest="progress_update",
        help="path to progress_update YAML, or '-' for stdin",
    )
    parser.add_argument(
        "--recommendation",
        type=str,
        help="path to recommendation YAML, or '-' for stdin",
    )
    parser.add_argument(
        "--all",
        type=str,
        dest="all_workspace",
        help="workspace directory; auto-discover and validate progress-state.yaml + adaptive-training-data.yaml",
    )
    parser.add_argument(
        "--policy",
        action="store_true",
        help="also run cross-shape policy checks (assessment subitem consistency, stretch requires assessment, etc.)",
    )
    parser.add_argument(
        "--check-transition",
        type=str,
        dest="check_transition",
        metavar="FROM:TO",
        help="check a single status transition is allowed (e.g., 'selected:building')",
    )
    args = parser.parse_args()

    # Require at least one mode flag.
    if not any(
        [
            args.state,
            args.adaptive,
            args.progress_update,
            args.recommendation,
            args.all_workspace,
            args.check_transition,
        ]
    ):
        parser.print_usage(sys.stderr)
        print("error: at least one of --state/--adaptive/--progress-update/--recommendation/--all/--check-transition is required", file=sys.stderr)
        return 2

    exit_code = 0
    state_data: Any = None
    adaptive_data: Any = None

    if args.check_transition:
        if ":" not in args.check_transition:
            print(f"error: --check-transition expects FROM:TO, got {args.check_transition!r}", file=sys.stderr)
            return 2
        frm, to = args.check_transition.split(":", 1)
        errors: list[str] = []
        check_status_transition(frm.strip(), to.strip(), errors)
        exit_code |= report(errors, f"transition {frm}->{to}")

    if args.all_workspace:
        workspace = Path(args.all_workspace)
        if not workspace.is_dir():
            print(f"error: --all expects a directory, got {args.all_workspace!r}", file=sys.stderr)
            return 2
        discovered = discover_workspace_files(workspace)
        if not any(discovered.values()):
            print(f"error: no known YAML files found under {workspace}", file=sys.stderr)
            return 2
        args.state = args.state or (str(discovered["state"]) if discovered["state"] else None)
        args.adaptive = args.adaptive or (str(discovered["adaptive"]) if discovered["adaptive"] else None)

    if args.state:
        try:
            state_data = load_yaml_input(args.state)
        except (FileNotFoundError, ValueError, yaml.YAMLError) as e:
            print(f"error: failed to load --state: {e}", file=sys.stderr)
            return 2
        errors = []
        validate_progress_state(state_data, errors)
        exit_code |= report(errors, "progress-state.yaml")

    if args.adaptive:
        try:
            adaptive_data = load_yaml_input(args.adaptive)
        except (FileNotFoundError, ValueError, yaml.YAMLError) as e:
            print(f"error: failed to load --adaptive: {e}", file=sys.stderr)
            return 2
        errors = []
        validate_adaptive_training_data(adaptive_data, errors)
        exit_code |= report(errors, "adaptive-training-data.yaml")

    if args.progress_update:
        try:
            data = load_yaml_input(args.progress_update)
        except (FileNotFoundError, ValueError, yaml.YAMLError) as e:
            print(f"error: failed to load --progress-update: {e}", file=sys.stderr)
            return 2
        errors = []
        validate_progress_update(data, errors)
        exit_code |= report(errors, "progress_update")

    if args.recommendation:
        try:
            data = load_yaml_input(args.recommendation)
        except (FileNotFoundError, ValueError, yaml.YAMLError) as e:
            print(f"error: failed to load --recommendation: {e}", file=sys.stderr)
            return 2
        errors = []
        validate_recommendation(data, errors)
        exit_code |= report(errors, "recommendation")

    if args.policy:
        if state_data is None and adaptive_data is None:
            print("warning: --policy passed without --state or --adaptive; nothing to cross-check", file=sys.stderr)
        else:
            errors = []
            run_policy_checks(state_data, adaptive_data, errors)
            exit_code |= report(errors, "cross-shape policy")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
