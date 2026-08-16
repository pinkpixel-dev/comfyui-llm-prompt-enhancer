"""Tests for the Prompt Enhancer node.

These exercise the real prompt-selection and configuration logic. Nothing here
calls a paid API, and nothing is mocked - the code under test is pure enough to
run directly.

Run with:  python3 test_prompt_enhancer.py
"""

import unittest

import models
import prompts
from prompts import get_system_prompt
from prompt_enhancer_llm import PromptEnhancer


class TestSystemPromptSelection(unittest.TestCase):
    """get_system_prompt picks the right prompt for format + provider."""

    def test_tags_format_returns_tag_prompt(self):
        for provider in ("openai", "anthropic", "google", "ollama", "openrouter"):
            with self.subTest(provider=provider):
                self.assertIs(get_system_prompt("tags", provider), prompts.TAG_SYSTEM_PROMPT)

    def test_descriptive_format_returns_descriptive_prompt(self):
        for provider in ("openai", "anthropic", "google", "openrouter"):
            with self.subTest(provider=provider):
                self.assertIs(
                    get_system_prompt("descriptive", provider),
                    prompts.DESCRIPTIVE_SYSTEM_PROMPT,
                )

    def test_ollama_keeps_its_own_descriptive_prompt(self):
        result = get_system_prompt("descriptive", "ollama")
        self.assertIs(result, prompts.OLLAMA_DESCRIPTIVE_SYSTEM_PROMPT)
        # The wording that makes small local models behave.
        self.assertIn("Start with the focus object", result)

    def test_ollama_still_gets_tag_prompt_when_tags_selected(self):
        self.assertIs(get_system_prompt("tags", "ollama"), prompts.TAG_SYSTEM_PROMPT)

    def test_tag_prompt_asks_for_comma_separated_output(self):
        self.assertIn("comma-separated", prompts.TAG_SYSTEM_PROMPT)
        self.assertIn("SDXL", prompts.TAG_SYSTEM_PROMPT)

    def test_descriptive_prompts_are_distinct(self):
        self.assertNotEqual(
            prompts.DESCRIPTIVE_SYSTEM_PROMPT,
            prompts.OLLAMA_DESCRIPTIVE_SYSTEM_PROMPT,
        )


class TestModelLists(unittest.TestCase):
    """Model lists and defaults have to agree with each other."""

    def test_defaults_are_members_of_their_lists(self):
        pairs = [
            (models.OPENAI_DEFAULT, models.OPENAI_MODELS),
            (models.ANTHROPIC_DEFAULT, models.ANTHROPIC_MODELS),
            (models.GOOGLE_DEFAULT, models.GOOGLE_MODELS),
        ]
        for default, choices in pairs:
            with self.subTest(default=default):
                self.assertIn(default, choices)

    def test_no_duplicate_or_empty_entries(self):
        for choices in (models.OPENAI_MODELS, models.ANTHROPIC_MODELS, models.GOOGLE_MODELS):
            with self.subTest(choices=choices):
                self.assertEqual(len(choices), len(set(choices)))
                self.assertTrue(all(m and m.strip() for m in choices))

    def test_retired_model_ids_are_gone(self):
        """These all 404 now. Guard against anyone pasting them back in."""
        retired = [
            "gpt-4-turbo-preview",
            "claude-3.5-sonnet",
            "gemini-pro",
            "google/gemma-2-9b-it:free",
        ]
        haystack = " ".join(
            models.OPENAI_MODELS
            + models.ANTHROPIC_MODELS
            + models.GOOGLE_MODELS
            + [models.OPENROUTER_DEFAULT, models.OLLAMA_DEFAULT]
        )
        for dead in retired:
            with self.subTest(model=dead):
                self.assertNotIn(dead, haystack)


class TestInputTypes(unittest.TestCase):
    """The ComfyUI node definition."""

    @classmethod
    def setUpClass(cls):
        cls.spec = PromptEnhancer.INPUT_TYPES()

    def test_required_inputs_are_unchanged(self):
        """Adding a new required input breaks every saved workflow."""
        self.assertEqual(
            set(self.spec["required"]),
            {"clip", "prompt", "llm_provider", "style"},
        )

    def test_prompt_format_is_optional(self):
        self.assertIn("prompt_format", self.spec["optional"])
        self.assertNotIn("prompt_format", self.spec["required"])

    def test_prompt_format_offers_both_modes(self):
        choices, config = self.spec["optional"]["prompt_format"]
        self.assertEqual(choices, ["descriptive", "tags"])
        self.assertEqual(config["default"], "descriptive")

    def test_model_dropdowns_use_shared_lists(self):
        cases = [
            ("openai_model", models.OPENAI_MODELS, models.OPENAI_DEFAULT),
            ("anthropic_model", models.ANTHROPIC_MODELS, models.ANTHROPIC_DEFAULT),
            ("google_model", models.GOOGLE_MODELS, models.GOOGLE_DEFAULT),
        ]
        for name, choices, default in cases:
            with self.subTest(input=name):
                spec_choices, config = self.spec["optional"][name]
                self.assertEqual(spec_choices, choices)
                self.assertEqual(config["default"], default)

    def test_openrouter_default_is_a_live_free_model(self):
        _, config = self.spec["optional"]["openrouter_model"]
        self.assertEqual(config["default"], models.OPENROUTER_DEFAULT)
        self.assertTrue(config["default"].endswith(":free"))


class TestBackwardCompatibility(unittest.TestCase):
    """An old workflow calls enhance_prompt without any of the new inputs."""

    def test_new_inputs_all_have_defaults(self):
        import inspect

        sig = inspect.signature(PromptEnhancer.enhance_prompt)
        new_inputs = [
            "prompt_format",
            "openai_model",
            "anthropic_model",
            "google_model",
        ]
        for name in new_inputs:
            with self.subTest(param=name):
                self.assertIn(name, sig.parameters)
                self.assertIsNot(sig.parameters[name].default, inspect.Parameter.empty)

    def test_provider_none_returns_prompt_untouched(self):
        """The one path that needs no API key and no CLIP work."""
        node = PromptEnhancer()
        sentinel_clip = object()
        clip_out, text_out = node.enhance_prompt(
            clip=sentinel_clip,
            prompt="a red bicycle",
            llm_provider="none",
            style="Basic Styles > none",
        )
        self.assertIs(clip_out, sentinel_clip)
        self.assertEqual(text_out, "a red bicycle")


class TestStyleHandling(unittest.TestCase):
    """Style strings arrive as 'Category > style'."""

    def setUp(self):
        self.node = PromptEnhancer()

    def test_every_offered_style_has_a_prompt(self):
        """A style in the dropdown with no entry in style_prompts is a KeyError."""
        spec = PromptEnhancer.INPUT_TYPES()
        offered = spec["required"]["style"][0]
        for entry in offered:
            style = entry.split(" > ")[-1]
            with self.subTest(style=style):
                self.assertIn(style, self.node.style_prompts)


if __name__ == "__main__":
    unittest.main(verbosity=2)
