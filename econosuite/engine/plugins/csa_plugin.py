"""CSA Plugin — First-class R integration as DAG TaskNode (FR-14).

Elevates the clinical-statistics-analyzer R codebase from a passive filesystem
dependency to an active TaskNode triggered synchronously by the DAG Engine.
Ensures R output is available before dependent LLM sections begin drafting.

Design Ref: §3.6 — CSAPlugin
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CSAResult:
    """Result from executing a CSA R script task."""

    task_id: str  # e.g. "csa:table1"
    script: str  # e.g. "02_table1.R"
    output_path: Path | None = None
    output_data: dict[str, Any] = field(default_factory=dict)
    success: bool = False
    error: str = ""
    stdout: str = ""
    stderr: str = ""


class CSAPlugin:
    """Elevates CSA R scripts from passive deps to active DAG TaskNodes.

    Each CSA task maps to an R script in clinical-statistics-analyzer/scripts/.
    The DAG engine calls run_task() for CSA nodes before dependent LLM sections,
    eliminating context drift between R-statistics and LLM text synthesis.
    """

    SCRIPT_MAP: dict[str, str] = {
        "csa:table1": "02_table1.R",
        "csa:survival": "03_survival.R",
        "csa:adverse_events": "04_adverse_events.R",
        "csa:response": "05_response.R",
        "csa:subgroup": "06_subgroup.R",
    }

    def __init__(
        self,
        csa_dir: Path | str | None = None,
        dataset_path: Path | str | None = None,
        output_dir: Path | str | None = None,
        timeout: int = 300,
    ) -> None:
        self._csa_dir = Path(csa_dir) if csa_dir else self._find_csa_dir()
        self._dataset_path = Path(dataset_path) if dataset_path else None
        self._output_dir = Path(output_dir) if output_dir else Path(
            os.environ.get("CSA_OUTPUT_DIR", "/tmp/csa_output")
        )
        self._timeout = timeout
        self._results: dict[str, CSAResult] = {}

    def run_task(self, task_id: str) -> CSAResult:
        """Execute R script for a CSA task node.

        Returns CSAResult with parsed JSON output if available.
        """
        script = self.SCRIPT_MAP.get(task_id)
        if not script:
            result = CSAResult(task_id=task_id, script="", error=f"Unknown CSA task: {task_id}")
            self._results[task_id] = result
            return result

        script_path = self._csa_dir / "scripts" / script
        if not script_path.exists():
            result = CSAResult(
                task_id=task_id, script=script,
                error=f"R script not found: {script_path}",
            )
            self._results[task_id] = result
            return result

        self._output_dir.mkdir(parents=True, exist_ok=True)

        # Build command
        cmd = ["Rscript", str(script_path)]
        if self._dataset_path:
            cmd.append(str(self._dataset_path))

        env = {**os.environ, "CSA_OUTPUT_DIR": str(self._output_dir)}

        logger.info("CSA task %s: running %s", task_id, script)

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self._timeout,
                env=env,
            )

            # Parse JSON sidecar output
            task_stem = task_id.split(":")[1] if ":" in task_id else task_id
            json_out = self._output_dir / f"{task_stem}.json"
            output_data = {}
            if json_out.exists():
                try:
                    output_data = json.loads(json_out.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    logger.warning("CSA JSON parse failed for %s: %s", task_id, exc)

            result = CSAResult(
                task_id=task_id,
                script=script,
                output_path=json_out if json_out.exists() else None,
                output_data=output_data,
                success=proc.returncode == 0,
                error=proc.stderr if proc.returncode != 0 else "",
                stdout=proc.stdout,
                stderr=proc.stderr,
            )

        except subprocess.TimeoutExpired:
            result = CSAResult(
                task_id=task_id, script=script,
                error=f"Timeout after {self._timeout}s",
            )
        except FileNotFoundError:
            result = CSAResult(
                task_id=task_id, script=script,
                error="Rscript not found — R runtime not installed",
            )
        except Exception as exc:
            result = CSAResult(
                task_id=task_id, script=script,
                error=str(exc),
            )

        self._results[task_id] = result
        if result.success:
            logger.info("CSA task %s: completed (%d bytes output)", task_id, len(str(result.output_data)))
        else:
            logger.warning("CSA task %s: failed — %s", task_id, result.error)

        return result

    def get_output(self, task_id: str) -> dict[str, Any]:
        """Get cached output from a completed CSA task."""
        if task_id in self._results and self._results[task_id].success:
            return self._results[task_id].output_data
        return {}

    def get_result(self, task_id: str) -> CSAResult | None:
        """Get full CSAResult for a task."""
        return self._results.get(task_id)

    def all_results(self) -> dict[str, CSAResult]:
        """Return all task results."""
        return dict(self._results)

    @staticmethod
    def _find_csa_dir() -> Path:
        """Auto-discover CSA directory relative to HPW."""
        candidates = [
            Path(__file__).parents[2] / "clinical-statistics-analyzer",
            Path(__file__).parents[3] / "clinical-statistics-analyzer",
            Path.home() / "Coding" / "HemaSuite" / "clinical-statistics-analyzer",
        ]
        for c in candidates:
            if c.exists():
                return c
        return Path("clinical-statistics-analyzer")  # fallback
