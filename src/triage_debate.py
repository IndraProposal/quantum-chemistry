#!/usr/bin/env python3
"""
Triage Debate Protocol v0 ("Gibberish v0") Reference Engine.
Canonical implementation of backstage triage debate parsing, validation,
consensus merging, and guardrail enforcement for Mindrock Autonomous Agents.
"""

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Dict, List, Optional, Tuple


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def from_str(cls, val: str) -> "Confidence":
        normalized = val.strip().lower()
        if "high" in normalized or "высок" in normalized:
            return cls.HIGH
        elif "med" in normalized or "средн" in normalized:
            return cls.MEDIUM
        elif "low" in normalized or "низк" in normalized:
            return cls.LOW
        raise ValueError(f"Invalid confidence level: {val}")


class TriggerType(str, Enum):
    POSTMASTER = "incident-postmaster"
    QA_GATE = "qa-gate-dispute"
    SCHEDULED = "scheduled-escalation"


class DebateState(str, Enum):
    OPENED = "OPENED"
    IN_DEBATE = "IN_DEBATE"
    CONSENSUS_REACHED = "CONSENSUS_REACHED"
    DEADLOCK_ESCALATED = "DEADLOCK_ESCALATED"


class GuardrailViolation(Exception):
    """Raised when an agent attempts an unauthorized state mutation during triage debate."""
    pass


@dataclass
class GibberishMessage:
    thesis: str
    facts: str
    interpretation: str
    confidence: Confidence
    verify: str
    decision: str
    extra_fields: Dict[str, str] = field(default_factory=dict)
    author: Optional[str] = None

    @classmethod
    def parse_from_text(cls, text: str, author: Optional[str] = None) -> "GibberishMessage":
        """
        Parses a Gibberish v0 formatted text block into a GibberishMessage.
        Recognizes: ТЕЗИС, ФАКТЫ, ИНТЕРПРЕТАЦИЯ, УВЕРЕННОСТЬ, ПРОВЕРИТЬ, РЕШЕНИЕ
        and any optional fields like СВЯЗЬ С ...
        """
        clean_text = text.strip()
        
        # Regex patterns for the 6 core fields (case insensitive)
        patterns = {
            "thesis": r"(?:ТЕЗИС|THESIS):\s*(.*?)(?=\n(?:ФАКТЫ|FACTS|ИНТЕРПРЕТАЦИЯ|INTERPRETATION|УВЕРЕННОСТЬ|CONFIDENCE|ПРОВЕРИТЬ|VERIFY|РЕШЕНИЕ|DECISION|СВЯЗЬ)|$)",
            "facts": r"(?:ФАКТЫ|FACTS):\s*(.*?)(?=\n(?:ТЕЗИС|THESIS|ИНТЕРПРЕТАЦИЯ|INTERPRETATION|УВЕРЕННОСТЬ|CONFIDENCE|ПРОВЕРИТЬ|VERIFY|РЕШЕНИЕ|DECISION|СВЯЗЬ)|$)",
            "interpretation": r"(?:ИНТЕРПРЕТАЦИЯ|INTERPRETATION):\s*(.*?)(?=\n(?:ТЕЗИС|THESIS|ФАКТЫ|FACTS|УВЕРЕННОСТЬ|CONFIDENCE|ПРОВЕРИТЬ|VERIFY|РЕШЕНИЕ|DECISION|СВЯЗЬ)|$)",
            "confidence": r"(?:УВЕРЕННОСТЬ|CONFIDENCE):\s*(.*?)(?=\n(?:ТЕЗИС|THESIS|ФАКТЫ|FACTS|ИНТЕРПРЕТАЦИЯ|INTERPRETATION|ПРОВЕРИТЬ|VERIFY|РЕШЕНИЕ|DECISION|СВЯЗЬ)|$)",
            "verify": r"(?:ПРОВЕРИТЬ|VERIFY):\s*(.*?)(?=\n(?:ТЕЗИС|THESIS|ФАКТЫ|FACTS|ИНТЕРПРЕТАЦИЯ|INTERPRETATION|УВЕРЕННОСТЬ|CONFIDENCE|РЕШЕНИЕ|DECISION|СВЯЗЬ)|$)",
            "decision": r"(?:РЕШЕНИЕ|DECISION):\s*(.*?)(?=\n(?:ТЕЗИС|THESIS|ФАКТЫ|FACTS|ИНТЕРПРЕТАЦИЯ|INTERPRETATION|УВЕРЕННОСТЬ|CONFIDENCE|ПРОВЕРИТЬ|VERIFY|СВЯЗЬ)|$)",
        }

        extracted = {}
        for key, pat in patterns.items():
            match = re.search(pat, clean_text, re.DOTALL | re.IGNORECASE)
            if not match:
                raise ValueError(f"Missing required Gibberish v0 field: '{key.upper()}'")
            extracted[key] = match.group(1).strip()

        # Parse confidence
        confidence_enum = Confidence.from_str(extracted["confidence"])

        # Check for extra fields (e.g. СВЯЗЬ С MIN-136)
        extra = {}
        relation_match = re.search(r"(?:СВЯЗЬ(?:\s+С\s+[^:]+)?|RELATION):\s*(.*?)(?=\n(?:ТЕЗИС|ФАКТЫ|ИНТЕРПРЕТАЦИЯ|УВЕРЕННОСТЬ|ПРОВЕРИТЬ|РЕШЕНИЕ)|$)", clean_text, re.DOTALL | re.IGNORECASE)
        if relation_match:
            extra["relation"] = relation_match.group(1).strip()

        return cls(
            thesis=extracted["thesis"],
            facts=extracted["facts"],
            interpretation=extracted["interpretation"],
            confidence=confidence_enum,
            verify=extracted["verify"],
            decision=extracted["decision"],
            extra_fields=extra,
            author=author
        )

    def to_text(self) -> str:
        lines = [
            f"ТЕЗИС: {self.thesis}",
            f"ФАКТЫ: {self.facts}",
            f"ИНТЕРПРЕТАЦИЯ: {self.interpretation}",
            f"УВЕРЕННОСТЬ: {self.confidence.value}",
        ]
        if "relation" in self.extra_fields:
            lines.append(f"СВЯЗЬ: {self.extra_fields['relation']}")
        lines.append(f"ПРОВЕРИТЬ: {self.verify}")
        lines.append(f"РЕШЕНИЕ: {self.decision}")
        return "\n".join(lines)


@dataclass
class DebateRound:
    round_id: int
    issue_id: str
    trigger: TriggerType
    participants: List[str]
    messages: List[GibberishMessage] = field(default_factory=list)
    state: DebateState = DebateState.OPENED

    def add_message(self, msg: GibberishMessage):
        self.messages.append(msg)
        if len(self.messages) >= 2:
            self.state = DebateState.IN_DEBATE


class GuardrailEnforcer:
    """Strictly enforces read-only operations during triage debate."""
    ALLOWED_ACTIONS = {"read_logs", "read_commit", "fetch_status", "query_linear", "read_file", "parse_pipeline"}
    MUTATION_ACTIONS = {"rerun_pipeline", "git_push", "modify_secret", "merge_pr", "delete_branch", "restart_service"}

    @classmethod
    def check_action(cls, action: str, tap_approved: bool = False):
        if action in cls.MUTATION_ACTIONS and not tap_approved:
            raise GuardrailViolation(
                f"Action '{action}' is a forbidden mutation during backstage triage. "
                "Mutations require an explicit human tap authorization."
            )
        return True


class TriageMerger:
    """Synthesizes multiple agent triage inputs into a canonical consensus or escalation."""

    @classmethod
    def synthesize_consensus(
        cls,
        debate: DebateRound,
        merger_agent: str = "Muse"
    ) -> Tuple[DebateState, str]:
        if len(debate.messages) < 2:
            return debate.state, "Debate requires at least 2 diagnostic participants."

        msg1 = debate.messages[0]
        msg2 = debate.messages[1]

        # Check for confidence divergence or conflicting decision
        confidences = [m.confidence for m in debate.messages]
        has_divergence = len(set(confidences)) > 1 or (
            Confidence.LOW in confidences and Confidence.HIGH in confidences
        )

        # Check decision semantic alignment
        decisions_agree = (
            ("шум" in msg1.decision.lower() and "шум" in msg2.decision.lower()) or
            ("retry" in msg1.decision.lower() and "retry" in msg2.decision.lower()) or
            ("close" in msg1.decision.lower() and "close" in msg2.decision.lower()) or
            ("зеркал" in msg1.decision.lower() and "зеркал" in msg2.decision.lower()) or
            (msg1.decision.strip().lower() == msg2.decision.strip().lower())
        )

        participants_str = " ↔ ".join(debate.participants)
        
        if has_divergence and not decisions_agree:
            debate.state = DebateState.DEADLOCK_ESCALATED
            body = (
                f"⚠️ **Triage-дебаты #{debate.round_id} — ТУПИК / ЭСКАЛАЦИЯ**\n"
                f"<!-- triage-debate:deadlock -->\n"
                f"Участники: {participants_str} | Мерджер: {merger_agent}\n\n"
                f"РАСХОЖДЕНИЕ (DISSENT):\n"
                f"- {debate.participants[0]}: {msg1.thesis} (Уверенность: {msg1.confidence.value}) -> РЕШЕНИЕ: {msg1.decision}\n"
                f"- {debate.participants[1]}: {msg2.thesis} (Уверенность: {msg2.confidence.value}) -> РЕШЕНИЕ: {msg2.decision}\n\n"
                f"Требуется 1 тап Принципала (@pavel.cherkashin) в «My Issues» для выбора решения."
            )
            return debate.state, body

        # Reach consensus
        debate.state = DebateState.CONSENSUS_REACHED
        
        # Primary thesis & synthesis
        chosen_thesis = msg1.thesis
        unified_facts = f"{msg1.facts} | Дополнительно: {msg2.facts}" if msg1.facts != msg2.facts else msg1.facts
        unified_interpretation = f"{msg1.interpretation} {msg2.interpretation}".strip()
        unified_confidence = min(confidences, key=lambda c: [Confidence.HIGH, Confidence.MEDIUM, Confidence.LOW].index(c))
        unified_verify = f"{msg1.verify}; {msg2.verify}" if msg1.verify != msg2.verify else msg1.verify
        unified_decision = msg1.decision

        body_lines = [
            f"🧪 **Triage-дебаты #{debate.round_id} — КОНСЕНСУС** (пилот протокола backstage-диагностики; участники: {participants_str})",
            f"<!-- triage-debate:consensus -->",
            "",
            f"ТЕЗИС: {chosen_thesis}",
            f"ФАКТЫ: {unified_facts}",
            f"ИНТЕРПРЕТАЦИЯ: {unified_interpretation}",
            f"УВЕРЕННОСТЬ: {unified_confidence.value}.",
        ]

        # Preserve relations if any
        all_relations = [m.extra_fields.get("relation") for m in debate.messages if "relation" in m.extra_fields]
        if all_relations:
            body_lines.append(f"СВЯЗЬ С {debate.issue_id}: {' '.join(all_relations)}")

        body_lines.append(f"ПРОВЕРИТЬ: {unified_verify}")
        body_lines.append(f"РЕШЕНИЕ: {unified_decision}")

        return debate.state, "\n".join(body_lines)
