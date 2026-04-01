"""DAG resolution and execution for the unified pipeline."""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SectionNode:
    """Minimal DAG node describing a section and its dependencies."""

    id: str
    depends_on: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DAGLayer:
    """A group of sections that can execute in parallel."""

    index: int
    section_ids: list[str]


class CycleDetectedError(ValueError):
    """Raised when section dependencies contain a cycle."""


class DAGResolver:
    """Resolves execution layers and runs them with optional parallelism."""

    def resolve(self, sections: list[SectionNode]) -> list[DAGLayer]:
        """Kahn's topological sort → execution layers.

        Returns DAGLayer objects where each layer's sections have all
        dependencies satisfied by prior layers. Sections within a layer
        are parallel-safe.
        """
        section_ids = [section.id for section in sections]
        known_ids = set(section_ids)
        unknown_dependencies = sorted(
            {
                dependency
                for section in sections
                for dependency in section.depends_on
                if dependency not in known_ids
            }
        )
        if unknown_dependencies:
            raise ValueError(
                "Unknown dependency references: " + ", ".join(unknown_dependencies)
            )

        indegree: dict[str, int] = {section.id: 0 for section in sections}
        adjacency: dict[str, list[str]] = defaultdict(list)
        for section in sections:
            for dependency in section.depends_on:
                adjacency[dependency].append(section.id)
                indegree[section.id] += 1

        ready = sorted(section_id for section_id, degree in indegree.items() if degree == 0)
        layers: list[DAGLayer] = []
        resolved_count = 0

        while ready:
            current_layer = ready
            layers.append(DAGLayer(index=len(layers), section_ids=current_layer))
            resolved_count += len(current_layer)

            next_ready: list[str] = []
            for section_id in current_layer:
                for dependent_id in sorted(adjacency.get(section_id, [])):
                    indegree[dependent_id] -= 1
                    if indegree[dependent_id] == 0:
                        next_ready.append(dependent_id)
            ready = sorted(next_ready)

        if resolved_count != len(sections):
            unresolved = sorted(section_id for section_id, degree in indegree.items() if degree > 0)
            raise CycleDetectedError(
                "Dependency cycle detected among sections: " + ", ".join(unresolved)
            )

        return layers

    def execute(
        self,
        layers: list[DAGLayer],
        runner_fn,
        max_workers: int = 4,
    ) -> dict[str, Any]:
        results: dict[str, Any] = {}
        is_sequential = all(len(layer.section_ids) == 1 for layer in layers)

        if is_sequential:
            for layer in layers:
                section_id = layer.section_ids[0]
                try:
                    results[section_id] = runner_fn(section_id)
                except Exception as exc:  # pragma: no cover
                    results[section_id] = exc
            return results

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for layer in layers:
                sids = layer.section_ids
                if len(sids) == 1:
                    section_id = sids[0]
                    try:
                        results[section_id] = runner_fn(section_id)
                    except Exception as exc:  # pragma: no cover
                        results[section_id] = exc
                    continue

                future_map = {
                    executor.submit(runner_fn, section_id): section_id
                    for section_id in sids
                }
                for future in as_completed(future_map):
                    section_id = future_map[future]
                    try:
                        results[section_id] = future.result()
                    except Exception as exc:
                        results[section_id] = exc

        return results
