# Changelog

All notable changes to this project will be documented in this file.

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
