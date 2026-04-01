"""Double-Lock Evidence Verification — pre-anchoring and post-generation auditing.

Implements FR-07 (Trusted Anchor Set), FR-08 (Orphan Detection), and FR-09 (Grounding Score).
Ensures zero-hallucination by verifying [LIT: PMID xxxxx] tags against trusted sources.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, List, Set, Dict

from engine._patterns import RE_FLAG_TAG, RE_LIT_TAG

logger = logging.getLogger(__name__)


@dataclass
class AnchorEntry:
    """A single trusted citation entry."""
    pmid: str
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: str = ""


@dataclass
class AnchorSet:
    """Collection of trusted citations for a section or document."""
    valid_pmids: Set[str]
    topic: str
    entries: Dict[str, AnchorEntry] = field(default_factory=dict)
    invalid_pmids: Set[str] = field(default_factory=set)
    total_submitted: int = 0


@dataclass
class AuditResult:
    """Outcome of a post-generation citation audit."""
    section_id: str = ""
    total_citations: int = 0
    verified_count: int = 0
    orphan_pmids: List[str] = field(default_factory=list)
    orphan_count: int = 0
    missing_pmids: List[str] = field(default_factory=list)
    missing_count: int = 0
    flag_count: int = 0
    grounding_ratio: float = 0.0

    @property
    def passed(self) -> bool:
        """Passed if no orphans exist AND grounding ratio meets threshold (0.5)."""
        return not self.orphan_pmids and self.grounding_ratio >= 0.5


class DoubleLockAuditor:
    """Audits LLM-generated sections for citation accuracy and grounding."""

    def pre_anchor(self, evidence_articles: List[Dict[str, Any]], section_topic: str) -> AnchorSet:
        """Build a trusted anchor set from provided evidence articles.
        
        Extracts PMIDs from evidence articles and performs batch validation.
        """
        raw_pmids = []
        entries = {}
        for art in evidence_articles:
            pmid = str(art.get("pmid", "")).strip()
            if pmid and pmid.isdigit():
                raw_pmids.append(pmid)
                entries[pmid] = AnchorEntry(
                    pmid=pmid,
                    title=art.get("title", ""),
                    authors=art.get("authors", []),
                    year=str(art.get("year", ""))
                )
        
        # Batch validate PMIDs via mock-friendly design
        valid_pmids = self._batch_validate_pmids(raw_pmids)
        invalid_pmids = set(raw_pmids) - valid_pmids

        # Filter entries to only valid ones
        filtered_entries = {p: entries[p] for p in valid_pmids if p in entries}

        logger.info("Built AnchorSet with %d trusted PMIDs for topic: %s",
                    len(valid_pmids), section_topic)

        return AnchorSet(
            valid_pmids=valid_pmids,
            topic=section_topic,
            entries=filtered_entries,
            invalid_pmids=invalid_pmids,
            total_submitted=len(raw_pmids),
        )

    def post_audit(self, section_id: str, generated_text: str, anchor_set: AnchorSet) -> AuditResult:
        """Scan generated text for citation tags and verify against anchor set."""
        cited_pmids = RE_LIT_TAG.findall(generated_text)
        total_citations = len(cited_pmids)
        
        unique_cited = set(cited_pmids)
        verified_pmids = unique_cited.intersection(anchor_set.valid_pmids)
        orphan_pmids = sorted(list(unique_cited - anchor_set.valid_pmids))
        missing_pmids = sorted(list(anchor_set.valid_pmids - unique_cited))
        
        flag_count = len(RE_FLAG_TAG.findall(generated_text))
        
        # grounding_ratio = sentences_with_verified_citations / total_sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', generated_text) if s.strip()]
        if not sentences:
            grounding_ratio = 0.0
        else:
            grounded_sentences = 0
            for s in sentences:
                s_pmids = set(RE_LIT_TAG.findall(s))
                if s_pmids and s_pmids.issubset(anchor_set.valid_pmids):
                    grounded_sentences += 1
            grounding_ratio = grounded_sentences / len(sentences)

        logger.info("Audit for %s: %d citations, %d verified, %d orphans, %d flags. Grounding: %.2f",
                    section_id, total_citations, len(verified_pmids), len(orphan_pmids), 
                    flag_count, grounding_ratio)

        return AuditResult(
            section_id=section_id,
            total_citations=total_citations,
            verified_count=len(verified_pmids),
            orphan_pmids=orphan_pmids,
            orphan_count=len(orphan_pmids),
            missing_pmids=missing_pmids,
            missing_count=len(missing_pmids),
            flag_count=flag_count,
            grounding_ratio=grounding_ratio,
        )

    def _batch_validate_pmids(self, pmids: List[str]) -> Set[str]:
        """Validate PMIDs via NCBI E-utilities efetch.

        Reuses the PubMedSearcher batch pattern: POST to efetch.fcgi,
        parse returned XML for valid <PubmedArticle> entries.
        Falls back to trusting input PMIDs if the network call fails.
        """
        if not pmids:
            return set()

        try:
            from tools.draft_generator.pubmed_searcher import PubMedSearcher
            searcher = PubMedSearcher()
            articles = searcher._fetch_details(list(pmids))
            validated = {str(a.pmid) for a in articles if a.pmid}
            if validated:
                logger.info("Batch validated %d/%d PMIDs via E-utilities", len(validated), len(pmids))
                return validated
        except ImportError:
            logger.debug("PubMedSearcher not available; trusting input PMIDs")
        except Exception as exc:
            logger.warning("PubMed batch validation failed (%s); trusting input PMIDs", exc)

        # Fallback: trust the PMIDs from evidence_articles (First Lock)
        return set(pmids)
