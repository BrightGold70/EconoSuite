"""Unified Pipeline Engine."""

from ._patterns import RE_FLAG_TAG, RE_LIT_TAG
from .block_store import BlockOutput, BlockStore
from .dag import CycleDetectedError, DAGLayer, DAGResolver, SectionNode
from .double_lock import AnchorEntry, AnchorSet, AuditResult, DoubleLockAuditor
from .plugin import PipelinePlugin, resolve_plugin
from .strategy import (
    CompilationConfig,
    QualityConfig,
    SectionConfig,
    StrategyConfig,
    StrategyLoader,
)
from .unified_engine import EngineConfig, EngineResult, SectionResult, UnifiedEngine

__all__ = [
    "AnchorEntry",
    "AnchorSet",
    "AuditResult",
    "BlockOutput",
    "BlockStore",
    "CompilationConfig",
    "CycleDetectedError",
    "DAGLayer",
    "DAGResolver",
    "DoubleLockAuditor",
    "EngineConfig",
    "EngineResult",
    "PipelinePlugin",
    "QualityConfig",
    "RE_FLAG_TAG",
    "RE_LIT_TAG",
    "SectionConfig",
    "SectionNode",
    "SectionResult",
    "StrategyConfig",
    "StrategyLoader",
    "UnifiedEngine",
    "resolve_plugin",
]
