"""Shared regex patterns for evidence and validation tags."""

from __future__ import annotations

import re

RE_LIT_TAG = re.compile(r"\[LIT:\s*PMID\s*(\d+)\]")
RE_FLAG_TAG = re.compile(r"\[FLAG:\s*(.*?)\]")

__all__ = ["RE_LIT_TAG", "RE_FLAG_TAG"]
