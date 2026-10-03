"""Unit tests for parsing and formatting helpers — no Ollama server required."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_service import LLMService
from debate_manager import DebateManager
from ui_components import DebateUI


class TestNormalizeFactCheck:
    def test_verified_label_kept(self):
        result = LLMService._normalize_fact_check("VERIFIED: The sky is blue.")
        assert result.startswith("VERIFIED:")

    def test_not_verified_maps_to_unverified(self):
        result = LLMService._normalize_fact_check("NOT VERIFIED: no evidence found.")
        assert result.startswith("UNVERIFIED:")

    def test_partially_verified_not_confused_with_verified(self):
        result = LLMService._normalize_fact_check("PARTIALLY VERIFIED: mostly true.")
        assert result.startswith("PARTIALLY VERIFIED:")

    def test_lowercase_label_normalized(self):
        result = LLMService._normalize_fact_check("verified: checks out.")
        assert result.startswith("VERIFIED:")

    def test_missing_label_defaults_to_unverified(self):
        result = LLMService._normalize_fact_check("I cannot determine this.")
        assert result.startswith("UNVERIFIED:")


class TestCleanup:
    def test_flattens_newlines(self):
        assert LLMService._cleanup("line one\nline two") == "line one line two."

    def test_adds_terminal_punctuation(self):
        assert LLMService._cleanup("no punctuation") == "no punctuation."

    def test_keeps_existing_punctuation(self):
        assert LLMService._cleanup("already punctuated!") == "already punctuated!"


class TestFormatScore:
    def test_half(self):
        assert DebateUI.format_score(0.5) == "½"

    def test_whole(self):
        assert DebateUI.format_score(2.0) == "2"

    def test_mixed(self):
        assert DebateUI.format_score(2.5) == "2½"


class TestEvaluateRound:
    def _manager(self):
        return DebateManager("test topic", "model-a", "model-b", judge_model="judge")

    def test_pro_win_scores_point(self, monkeypatch):
        debate = self._manager()
        monkeypatch.setattr(LLMService, "get_response",
                            staticmethod(lambda *a, **k: "PRO — Pro cited stronger evidence."))
        reason = debate.evaluate_round("pro arg", "con arg")
        assert debate.pro_wins == 1
        assert debate.con_wins == 0
        assert "stronger evidence" in reason

    def test_con_win_scores_point(self, monkeypatch):
        debate = self._manager()
        monkeypatch.setattr(LLMService, "get_response",
                            staticmethod(lambda *a, **k: "CON — Con refuted Pro directly."))
        reason = debate.evaluate_round("pro arg", "con arg")
        assert debate.con_wins == 1
        assert "refuted" in reason

    def test_tie_splits_point(self, monkeypatch):
        debate = self._manager()
        monkeypatch.setattr(LLMService, "get_response",
                            staticmethod(lambda *a, **k: "TIE — Both argued equally well."))
        debate.evaluate_round("pro arg", "con arg")
        assert debate.pro_wins == 0.5
        assert debate.con_wins == 0.5

    def test_unparseable_response_surfaces_warning(self, monkeypatch):
        debate = self._manager()
        monkeypatch.setattr(LLMService, "get_response",
                            staticmethod(lambda *a, **k: "Hmm, both sides made decent points honestly."))
        reason = debate.evaluate_round("pro arg", "con arg")
        assert debate.pro_wins == 0
        assert debate.con_wins == 0
        assert reason.startswith("⚠")

    def test_pro_substring_does_not_score(self, monkeypatch):
        # "PRO's argument was weaker" must not count as a Pro win
        debate = self._manager()
        monkeypatch.setattr(LLMService, "get_response",
                            staticmethod(lambda *a, **k: "CON — PRO's argument was weaker overall."))
        debate.evaluate_round("pro arg", "con arg")
        assert debate.con_wins == 1
        assert debate.pro_wins == 0

    def test_no_judge_returns_none(self):
        debate = DebateManager("t", "a", "b", judge_model=None)
        assert debate.evaluate_round("p", "c") is None
