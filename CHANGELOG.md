# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - August 16, 2026

### ✨ Prompt format toggle
- Added a `prompt_format` input with two modes, contributed by [@MasOverflow](https://github.com/MasOverflow) in [#2](https://github.com/pinkpixel-dev/comfyui-llm-prompt-enhancer/pull/2)
  - `descriptive` keeps the existing flowing-sentence output
  - `tags` produces comma separated SDXL / Danbooru style tags
- Works across all five providers: OpenAI, Anthropic, Google, Ollama, OpenRouter
- The input is optional, so existing saved workflows keep loading and default to `descriptive`

### 🤖 Model selection
- Added `openai_model`, `anthropic_model`, and `google_model` dropdowns so you can pick per provider instead of being stuck on one hardcoded model
- Refreshed every model ID. The old ones were retired and had started returning 404:
  - OpenAI: `gpt-4-turbo-preview` → `gpt-5.6-sol` / `gpt-5.6-terra` / `gpt-5.6-luna` (default `gpt-5.6-luna`)
  - Anthropic: `claude-3.5-sonnet` (never a valid ID) → `claude-opus-5` / `claude-sonnet-5` / `claude-haiku-4-5` (default `claude-haiku-4-5`)
  - Google: `gemini-pro` → `gemini-3.1-pro-preview` / `gemini-3.7-flash` / `gemini-3.6-flash` / `gemini-3.5-flash-lite` / `gemini-3.1-flash-lite` (default `gemini-3.5-flash-lite`)
- Defaults point at each provider's cheap tier, which handles prompt enhancement well at a fraction of the cost

### 🐛 Fixes
- Fixed the OpenRouter default model. `google/gemma-2-9b-it:free` was retired and no longer resolves; the default is now `google/gemma-4-26b-a4b-it:free`
- Ollama keeps its original descriptive wording ("Start with the focus object of the prompt"), which the shared prompt had dropped

### 🧹 Maintenance
- Split system prompts into `prompts.py` and model lists into `models.py` to keep `prompt_enhancer_llm.py` maintainable
- Added `test_prompt_enhancer.py` covering prompt selection, model list integrity, node inputs, and backward compatibility
- Added `__pycache__/` and `*.pyc` to `.gitignore`

## [1.1.0] - 2025-01-24

### Added
- OpenRouter support
  - Added OpenRouter client integration
  - Added OpenRouter API key configuration
  - Added OpenRouter as a new LLM provider option
  - Updated documentation with OpenRouter setup instructions
- Improved style selection interface
  - Added category prefixes to styles (e.g., "Basic Styles > detailed")
  - Simplified style selection to a single dropdown
  - Better organization of styles by category

### Fixed
- Added sumi-e style to "Asian Art Styles" category in style selection dropdown
  - Previously defined but not accessible in the UI
  - Now properly categorized with other Asian art styles
- Moved "howls castle" style to "Asian Art Styles" category
  - Better categorization with other Studio Ghibli-related styles
  - Improved style organization and discoverability
- Fixed style selection UI
  - Removed dependency on JavaScript
  - Implemented more reliable Python-based solution
  - Improved user experience with categorized style list

### Changed
- Updated requirements.txt to include openrouter-client
- Improved LLM provider initialization and handling
- Enhanced error handling for API requests
- Enhanced comic book style instructions
  - Added detailed specifications for line art, coloring, and composition
  - Included technical parameters for comic-specific visual elements
  - Improved clarity and effectiveness of the style generation
- Updated default Ollama model to llama3.2:1b
  - Changed from llama2:latest for better performance
  - Optimized for prompt enhancement tasks
- Simplified style selection architecture
  - Removed JavaScript-based implementation
  - Integrated style categories directly into Python code
  - Improved reliability and maintainability

Made with ❤️ by pinkpixel
