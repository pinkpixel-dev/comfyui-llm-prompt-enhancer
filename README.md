# ComfyUI LLM Prompt Enhancer

A powerful custom node for ComfyUI that enhances your prompts using various Language Learning Models (LLMs). This node supports multiple LLM providers and offers various enhancement styles to help you create better, more detailed prompts for image generation.

## Features

- 🤖 Multiple LLM Provider Support:
  - OpenAI (GPT models)
  - Anthropic (Claude)
  - Google (Gemini)
  - OpenRouter (Multiple Models)
  - Ollama (Local LLM)
- 🎨 50+ Enhancement Styles organized in categories:
  - No Style
  - Core Styles (detailed, photorealistic, etc.)
  - Fantasy & Horror
  - Modern Aesthetics
  - Art Movements
  - Asian Art Styles (anime, studio ghibli, ukiyo-e, sumi-e)
  - Traditional Media
  - Digital & Contemporary
  - Photography & Studio
  - Decorative Arts
  - Period & Style
- 🔒 Secure API Key Management
- 🚀 Easy Integration with ComfyUI
- 📝 Detailed Prompt Enhancement
- 🛠️ Local LLM Support via Ollama

## Prerequisites

- ComfyUI installed and working
- Python 3.10 or higher
- pip (Python package installer)
- For Ollama: Ollama installed and running locally

## Installation

1. Navigate to your ComfyUI custom nodes directory:

```bash
cd ComfyUI/custom_nodes/
```

2. Clone this repository:

```bash
git clone https://github.com/sizzlebop/ComfyUI-LLM-Prompt-Enhancer.git
```

3. Install required dependencies:

```bash
pip install openai anthropic google-generativeai torch requests
```

## LLM Provider Setup

### 1. OpenAI
- Visit [OpenAI Platform](https://platform.openai.com/api-keys)
- Click "Create new secret key"
- Copy the key and enter it in the node's "openai_key" input
- Uses GPT-4 Turbo Preview model
- Pricing: Pay-as-you-go, varies by model

### 2. Anthropic
- Visit [Anthropic Console](https://console.anthropic.com/)
- Create an account and go to API Keys
- Generate a new API key
- Copy the key and enter it in the node's "anthropic_key" input
- Uses Claude 3.5 Sonnet model
- Pricing: Pay-as-you-go, varies by model

### 3. Google
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new project if needed
- Enable the Gemini API
- Create credentials and copy the API key
- Enter it in the node's "google_key" input
- Uses Gemini Pro model
- Pricing: Free tier available, then pay-as-you-go

### 4. OpenRouter
- Visit [OpenRouter Console](https://console.openrouter.com/)
- Create an account
- Generate a new API key
- Copy the key and enter it in the node's "openrouter_key" input
- Enter your desired model name in the "openrouter_model" input
- Pricing: 
  - Free tier available with some models
  - Other models: Pay-as-you-go, varies by model

### 5. Ollama (Local LLM)
- Install Ollama from [ollama.ai](https://ollama.ai)
- Start the Ollama service:
  ```bash
  # Windows (PowerShell, run as administrator)
  ollama serve
  ```
- Pull your desired model:
  ```bash
  # Default model is llama3.2:1b
  ollama pull llama3.2:1b
  ```
- Configuration in the node:
  - "ollama_host": Default is "http://localhost:11434"
  - "ollama_model": Default is "llama3.2:1b"
  - Other recommended models: gemma2:2b, qwen2.5:1.5b, llama3.2:3b
- No API key required
- Completely free and runs locally

## Usage

1. Add the "LLM Prompt Enhancer" node to your workflow
2. Connect your CLIP model to the "clip" input
3. Enter your prompt in the "prompt" input field
4. Select your preferred LLM provider from:
   - openai (GPT-4 Turbo Preview)
   - anthropic (Claude 3.5 Sonnet)
   - google (Gemini Pro)
   - openrouter (custom models)
   - ollama (local models)
5. Choose an enhancement style from the categorized dropdown
6. Configure your chosen provider:

   **For OpenAI:**
   - Enter your OpenAI API key
   
   **For Anthropic:**
   - Enter your Anthropic API key
   
   **For Google:**
   - Enter your Google API key
   
   **For OpenRouter:**
   - Enter your OpenRouter API key
   - Enter your desired model name (default: google/gemma-2-9b-it:free)
   
   **For Ollama:**
   - Ensure Ollama is running
   - Optionally modify the host URL (default: http://localhost:11434)
   - Choose your model (default: llama3.2:1b)

7. Connect the enhanced prompt output to your image generation node

## Style Categories

The LLM Prompt Enhancer supports various art styles organized into the following categories:

- **Basic Styles**: none, detailed, photorealistic, cinematic, artistic, minimalist, vibrant
- **Fantasy & Horror**: fantasy, horror, dark fantasy, heavenly
- **Traditional Art**: oil painting, watercolor, abstract expressionist, hyperrealist, cubist
- **Art Movements**: art nouveau, art deco, baroque, renaissance, pop art, bauhaus, romanticist, dada
- **Asian Art Styles**: anime, studio ghibli, ukiyo-e, sumi-e, howls castle
- **Traditional Media**: oil painting, watercolor, pencil sketch, charcoal drawing, pastel art
- **Digital & Contemporary**: 3d render, digital art, concept art, comic book, pixel art, low poly, isometric
- **Genre & Theme**: cyberpunk, steampunk, gothic, vaporwave, retro, vintage
- **Decorative Arts**: stained glass, mosaic, street art

Each style comes with specific technical specifications and artistic elements that help guide the AI in enhancing your prompts.

## Troubleshooting

### OpenAI Issues
- Error "Authentication failed": Double-check your API key
- Error "Rate limit exceeded": Wait or upgrade your plan
- Error "Invalid model": Ensure you have access to the requested model

### Anthropic Issues
- Error "Invalid API key": Verify your key is correct
- Error "Rate limit reached": Check your usage limits
- Error "Model not available": Ensure you have access to Claude

### Google Issues
- Error "API key not valid": Check your key and project setup
- Error "Quota exceeded": Review your usage limits
- Error "API not enabled": Enable Gemini API in your project

### OpenRouter Issues
- Error "Authentication failed": Verify your API key
- Error "Model not available": Check model availability and credits
- Error "Rate limit": Review your usage and limits

### Ollama Issues
- Error "Connection failed": 
  - Ensure Ollama is running (`ollama serve`)
  - Check if the host URL is correct
  - Verify your firewall settings
- Error "Model not found":
  - Pull the model first: `ollama pull llama3.2:1b`
  - Check available models: `ollama list`
- Error "Invalid response":
  - Check Ollama logs for details
  - Ensure you have enough system resources

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

- GitHub Issues: [Report a bug](https://github.com/sizzlebop/comfyui-llm-prompt-enhancer/issues)
- Email: admin@pinkpixel.dev
- Discord: @sizzlebop

Made with ❤️ by pinkpixel
