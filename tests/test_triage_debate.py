#!/usr/bin/env python3
"""
Unit and integration test suite for Triage Debate Protocol v0.
"""

import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from triage_debate import (
    Confidence,
    DebateRound,
    DebateState,
    GibberishMessage,
    GuardrailEnforcer,
    GuardrailViolation,
    TriageMerger,
    TriggerType,
)


class TestTriageDebateProtocol(unittest.TestCase):

    def test_min150_pilot_comment_parsing(self):
        """Validates that the exact MIN-150 pilot comment parses into Gibberish v0 structure."""
        min150_raw = """
🧪 **Triage-дебаты #1 — КОНСЕНСУС** (пилот протокола backstage-диагностики; участники: ChatGPT read-only triage ↔ Muse)

ТЕЗИС: pipeline #2974623550 «failed» при 0 jobs — пустой граф, не реальный сбой. Шум, не инцидент.
ФАКТЫ: первый push в ветку feat/min-136-cve-u-stage-7 (before_sha=000…0); коммит 45586b41 «chore(evidence): finalize Stage 7 Dean sign-off», автор Pasha Mango, push — Павел по SSH с Wolfram; started_at=null, duration=null, jobs=[].
ИНТЕРПРЕТАЦИЯ: GitLab создал pipeline, ни одна job не сгенерировалась (CI для ветки не даёт jobs) → статус failed. Падать было нечему.
УВЕРЕННОСТЬ: high.
СВЯЗЬ С MIN-136: REWORK-1 FAIL был про рассинхрон зеркал (GitLab 7b04f82 ≠ GitHub 45586b4). Push 45586b41 довёл GitLab-ветку до SHA, который был на GitHub, — рассинхрон закрыт. Гейт Stage 7 («зеркала синхронны» + «verify-showcase.sh зелен») от GitLab CI не зависит.
ПРОВЕРИТЬ: GitHub-зеркало сейчас на 45586b41 (нужен URL зеркала от Павла).
РЕШЕНИЕ: retry не нужен и вреден (воспроизведёт пустоту). После проверки зеркала — закрыть тикет как шум.
"""
        msg = GibberishMessage.parse_from_text(min150_raw, author="ChatGPT")
        self.assertIn("пустой граф", msg.thesis)
        self.assertIn("45586b41", msg.facts)
        self.assertIn("Падать было нечему", msg.interpretation)
        self.assertEqual(msg.confidence, Confidence.HIGH)
        self.assertIn("рассинхрон зеркал", msg.extra_fields.get("relation", ""))
        self.assertIn("GitHub-зеркало сейчас на 45586b41", msg.verify)
        self.assertIn("закрыть тикет как шум", msg.decision)

    def test_two_agent_consensus_synthesis(self):
        """Simulates 2 agents debating an incident and achieving consensus."""
        agent1_turn = """
ТЕЗИС: Ошибка сборки вызвана отсутствием зависимости в chroot-окружении Darwin.
ФАКТЫ: Exit code 127 в job 412; missing binary: `lean`. Commit e8831a9.
ИНТЕРПРЕТАЦИЯ: Слот darwin не имеет установленного lean-пакета в $PATH runner'а.
УВЕРЕННОСТЬ: high
ПРОВЕРИТЬ: `which lean` на хосте darwin.
РЕШЕНИЕ: Установить lean в nix/elan профиль на darwin.
"""
        agent2_turn = """
ТЕЗИС: Среда darwin-on-macbookpro не имеет lean в PATH для runner-сессий.
ФАКТЫ: fleetd log: runner exited 127; PATH=/usr/bin:/bin.
ИНТЕРПРЕТАЦИЯ: Системный путь fleetd не подгружает ~/.elan/bin при старте launchd daemon.
УВЕРЕННОСТЬ: high
ПРОВЕРИТЬ: EnvironmentVariables в com.mindrock.fleetd.plist на Darwin.
РЕШЕНИЕ: Добавить ~/.elan/bin в launchd plist на darwin.
"""
        msg1 = GibberishMessage.parse_from_text(agent1_turn, author="gemini@darwin")
        msg2 = GibberishMessage.parse_from_text(agent2_turn, author="agy@wolfram")

        round_1 = DebateRound(
            round_id=2,
            issue_id="MIN-170",
            trigger=TriggerType.POSTMASTER,
            participants=["gemini@darwin", "agy@wolfram"]
        )
        round_1.add_message(msg1)
        round_1.add_message(msg2)

        self.assertEqual(round_1.state, DebateState.IN_DEBATE)

        state, consensus_text = TriageMerger.synthesize_consensus(round_1, merger_agent="Muse")
        self.assertEqual(state, DebateState.CONSENSUS_REACHED)
        self.assertIn("<!-- triage-debate:consensus -->", consensus_text)
        self.assertIn("ТЕЗИС: Ошибка сборки вызвана", consensus_text)
        self.assertIn("УВЕРЕННОСТЬ: high", consensus_text)

    def test_dissent_triggers_deadlock_escalation(self):
        """Verifies that conflicting theses and confidence divergence trigger deadlock escalation for Pavel."""
        turn_a = """
ТЕЗИС: Пайплайн упал из-за фатального бага в коде валидации.
ФАКТЫ: Null pointer exception в строке 42.
ИНТЕРПРЕТАЦИЯ: Релиз нельзя катить, код сломан.
УВЕРЕННОСТЬ: high
ПРОВЕРИТЬ: Логи runner.rs строка 42.
РЕШЕНИЕ: Немедленно откатить коммит и открыть REWORK.
"""
        turn_b = """
ТЕЗИС: Это ложноположительное падение из-за таймаута сети при доступе к Linear API.
ФАКТЫ: 504 Gateway Timeout в сетевом стеке.
ИНТЕРПРЕТАЦИЯ: Код корректен, внешний API упал.
УВЕРЕННОСТЬ: low
ПРОВЕРИТЬ: Статус linearstatus.com.
РЕШЕНИЕ: Повторить пайплайн (retry) без изменений в коде.
"""
        msg_a = GibberishMessage.parse_from_text(turn_a, author="codex@wolfram")
        msg_b = GibberishMessage.parse_from_text(turn_b, author="agy@wolfram")

        round_conflict = DebateRound(
            round_id=3,
            issue_id="MIN-175",
            trigger=TriggerType.QA_GATE,
            participants=["codex@wolfram", "agy@wolfram"]
        )
        round_conflict.add_message(msg_a)
        round_conflict.add_message(msg_b)

        state, deadlock_text = TriageMerger.synthesize_consensus(round_conflict, merger_agent="Muse")
        self.assertEqual(state, DebateState.DEADLOCK_ESCALATED)
        self.assertIn("<!-- triage-debate:deadlock -->", deadlock_text)
        self.assertIn("РАСХОЖДЕНИЕ (DISSENT)", deadlock_text)
        self.assertIn("@pavel.cherkashin", deadlock_text)
        self.assertIn("«My Issues»", deadlock_text)

    def test_guardrails_prevent_unauthorized_mutations(self):
        """Ensures agents cannot trigger mutations (rerun, git_push) during read-only triage."""
        # Read-only actions should pass cleanly
        self.assertTrue(GuardrailEnforcer.check_action("read_logs"))
        self.assertTrue(GuardrailEnforcer.check_action("query_linear"))
        self.assertTrue(GuardrailEnforcer.check_action("parse_pipeline"))

        # Mutation attempts without human tap must raise GuardrailViolation
        with self.assertRaises(GuardrailViolation):
            GuardrailEnforcer.check_action("rerun_pipeline", tap_approved=False)

        with self.assertRaises(GuardrailViolation):
            GuardrailEnforcer.check_action("git_push", tap_approved=False)

        with self.assertRaises(GuardrailViolation):
            GuardrailEnforcer.check_action("merge_pr", tap_approved=False)

        # Mutation with explicit tap approval is permitted
        self.assertTrue(GuardrailEnforcer.check_action("rerun_pipeline", tap_approved=True))


if __name__ == "__main__":
    unittest.main()
