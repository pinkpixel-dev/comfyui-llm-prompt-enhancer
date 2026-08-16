<p align="center">
  <img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1738065925/promptenhancelogo_kql6qa.svg" width="200" height="200">
</p>

# ComfyUI LLM Prompt Enhancer

A ComfyUI node that rewrites your prompt with an LLM before it reaches the CLIP encoder. You type something short, pick a style, and the node hands your image model a fuller prompt to work with.

It takes a CLIP input and returns conditioning plus the enhanced prompt as text, so you can drop it straight into an existing workflow or chain it with other nodes.

## What it does

- **Five providers**: OpenAI, Anthropic, Google, OpenRouter, and Ollama for local models
- **Two output formats**:
  - `descriptive` writes flowing sentences describing the image
  - `tags` writes comma separated SDXL and Danbooru style tags
- **47 enhancement styles** across 9 categories, from `photorealistic` to `ukiyo-e` to `vaporwave`
- **Model picker per provider**, so you can trade cost against quality without editing code
- **Runs fully local through Ollama** if you would rather not send prompts to an API
- **Falls back to your original prompt** if the API call fails, so a bad key or a rate limit doesn't break the run
- Works with Flux and Stable Diffusion, including SDXL and custom fine-tunes

## Example gallery

Two Cloudinary collections with more than fits here:

- [Node usage examples](https://collection.cloudinary.com/di7ctlowx/9fcb39a68533169bad5f827c2f5af279) shows the node wired into ComfyUI workflows
- [Generated image examples](https://collection.cloudinary.com/di7ctlowx/f5a8d0a031bae9e113af3d487f802bb8) shows output across different styles

### Anime Style
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794108/anime_fhcwcj.png" width="512" alt="Anime style example">

### Bauhaus Style
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794108/bauhaus_jmh9yf.png" width="512" alt="Bauhaus style example">

### Charcoal Drawing
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794110/charcoal_vul1ao.png" width="512" alt="Charcoal drawing example">

### Cyberpunk Style
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794109/cyberpunk_cp6eli.png" width="512" alt="Cyberpunk style example">

### Low Poly Art
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794108/lowpoly_gdsyrc.png" width="512" alt="Low poly art example">

### Pixel Art
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794108/pixelart_k0qw1c.png" width="512" alt="Pixel art example">

### Steampunk Style
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794110/steampunk_qs1b63.png" width="512" alt="Steampunk style example">

### Street Art
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794110/streetart_spy0va.png" width="512" alt="Street art example">

### Surreal Art
<img src="https://res.cloudinary.com/di7ctlowx/image/upload/v1737794111/surreal_sizr42.png" width="512" alt="Surreal art example">

## Prerequisites

- ComfyUI installed and working
- Python 3.10 or higher
- pip
- An API key for at least one provider, or Ollama running locally

## Installation

Navigate to your ComfyUI custom nodes directory:

```bash
cd ComfyUI/custom_nodes/
```

Clone the repository:

```bash
git clone https://github.com/pinkpixel-dev/comfyui-llm-prompt-enhancer.git
```

Install the dependencies:

```bash
pip install openai anthropic google-generativeai torch requests
```

Restart ComfyUI. The node shows up as **Prompt Enhancer LLM ✨** under `conditioning/prompt`.

You only need the packages for providers you actually use. The node imports each one in a try block and logs a message if it is missing, so a missing `anthropic` package will not stop the other providers from working.

## Provider setup

### OpenAI

Grab a key from the [OpenAI Platform](https://platform.openai.com/api-keys) and paste it into the node's `openai_key` input.

Models available in the `openai_model` dropdown:

| Model | Notes |
|---|---|
| `gpt-5.6-sol` | Flagship, most expensive |
| `gpt-5.6-terra` | Middle tier |
| `gpt-5.6-luna` | Cost optimized, the default |

### Anthropic

Create a key in the [Anthropic Console](https://console.anthropic.com/) and paste it into `anthropic_key`.

| Model | Notes |
|---|---|
| `claude-opus-5` | Flagship |
| `claude-sonnet-5` | Middle tier |
| `claude-haiku-4-5` | Fastest and cheapest, the default |

### Google

Create a key in [Google AI Studio](https://aistudio.google.com/app/apikey) and paste it into `google_key`. There is a free tier before it moves to pay as you go.

| Model | Notes |
|---|---|
| `gemini-3.1-pro-preview` | Flagship, 2M context |
| `gemini-3.7-flash` | Newest workhorse |
| `gemini-3.6-flash` | Previous workhorse |
| `gemini-3.5-flash-lite` | Low latency, the default |
| `gemini-3.1-flash-lite` | Cheapest |

### OpenRouter

Create a key at [openrouter.ai/keys](https://openrouter.ai/keys) and paste it into `openrouter_key`.

OpenRouter exposes thousands of models, so `openrouter_model` is a plain text field rather than a dropdown. Type any model ID from their catalog. The default is `google/gemma-4-26b-a4b-it:free`, which costs nothing to run.

Model IDs ending in `:free` have no token cost but are usually rate limited.

### Ollama

For local models with no API key and no per token cost. Install Ollama from [ollama.com](https://ollama.com), then start it:

```bash
ollama serve
```

Pull a model:

```bash
ollama pull llama3.2:1b
```

Then set `ollama_host` (default `http://localhost:11434`) and `ollama_model` (default `llama3.2:1b`) in the node. Other small models that work well here: `gemma2:2b`, `qwen2.5:1.5b`, `llama3.2:3b`.

The node checks the connection before sending anything, so if Ollama is not running you get a clear error instead of a timeout.

## Usage

1. Add the **Prompt Enhancer LLM ✨** node to your workflow
2. Connect your CLIP model to the `clip` input
3. Type your prompt into the `prompt` field
4. Pick a provider in `llm_provider`
5. Pick a style from the `style` dropdown
6. Set `prompt_format` to `descriptive` or `tags`
7. Fill in the API key and model for your chosen provider
8. Connect the `conditioning` output to your sampler, and `enhanced_prompt` anywhere you want to see the text

If you want to compare against an unenhanced prompt, select the `Basic Styles > none` style. That skips the style instructions, though the format enhancement still runs.

### A note on model defaults

Every provider defaults to its cheap tier. Prompt enhancement is a short task with maybe 200 tokens of output, and the small models handle it well, so there is usually no reason to pay flagship rates. Move up if you want richer output.

Providers rename and retire models fairly often. If one starts returning a 404, the lists live in [`models.py`](models.py) and are easy to edit.

### About your API keys

Keys are entered as normal node inputs, which means ComfyUI saves them into the workflow JSON. If you share a workflow file or post a screenshot, your key goes with it. Clear the key fields before sharing anything, or use Ollama, which needs no key at all.

## Style categories

47 styles across 9 categories. Pick one from the `style` dropdown, where they appear as `Category > style`.

- **Basic Styles**: none, detailed, photorealistic, cinematic, artistic, minimalist, vibrant
- **Fantasy & Horror**: fantasy, horror, dark fantasy, heavenly
- **Traditional Art**: oil painting, watercolor, abstract expressionist, hyperrealist, cubist
- **Art Movements**: art nouveau, art deco, baroque, renaissance, pop art, bauhaus, romanticist, dada
- **Asian Art Styles**: anime, studio ghibli, ukiyo-e, sumi-e
- **Traditional Media**: oil painting, watercolor, pencil sketch, charcoal drawing, pastel art
- **Digital & Contemporary**: 3d render, digital art, concept art, comic book, pixel art, low poly, isometric
- **Genre & Theme**: cyberpunk, steampunk, gothic, vaporwave, retro, vintage
- **Decorative Arts**: stained glass, mosaic, street art

Each style carries its own set of technical instructions that get prepended to your prompt. Selecting `none` skips the style layer and just runs the format enhancement.

## Troubleshooting

The node logs to the ComfyUI console under the `prompt_enhancer` logger, so start there when something looks off.

**The node doesn't appear in the menu.** Check the ComfyUI startup log for import errors. Missing Python packages are the usual cause.

**Enhancement silently does nothing.** When an API call fails the node returns your original prompt rather than erroring the whole run. The reason is in the console log.

### OpenAI
- "Authentication failed": check the key
- "Rate limit exceeded": wait, or check your plan
- "Invalid model": confirm your account has access to the selected model

### Anthropic
- "Invalid API key": check the key
- "Rate limit reached": check your usage limits
- "Model not found": confirm the model ID is still current

### Google
- "API key not valid": check the key and project setup
- "Quota exceeded": review your usage limits
- "API not enabled": enable the Gemini API for your project

### OpenRouter
- "Authentication failed": check the key
- "Model not available": confirm the model ID exists and your account has credits
- Rate limits on `:free` models are common. Switch to a paid model if you hit them often

### Ollama
- "Connection failed": make sure `ollama serve` is running, check the host URL, check your firewall
- "Model not found": pull it first with `ollama pull llama3.2:1b`, and see what you have with `ollama list`
- "Empty response from Ollama": usually a resource problem. Check the Ollama logs and try a smaller model

## Contributing

Pull requests are welcome. For anything large, open an issue first so we can talk it through.

There is a test suite that runs without any API keys:

```bash
python3 test_prompt_enhancer.py
```

It covers prompt format routing, the model lists, and the node's input definitions. Please run it before opening a PR. Adding a required input to `INPUT_TYPES` will break every saved workflow, so new inputs belong in `optional` with a default.

## License

MIT. See [LICENSE](LICENSE).

## Support

- GitHub Issues: [Report a bug](https://github.com/pinkpixel-dev/comfyui-llm-prompt-enhancer/issues)
- Email: admin@pinkpixel.dev
- Discord: @sizzlebop

Made with 💖 by Pink Pixel
