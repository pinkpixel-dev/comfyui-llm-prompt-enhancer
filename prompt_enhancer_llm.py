import os
import json
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('prompt_enhancer')

try:
    from openai import OpenAI
    logger.info("Successfully imported OpenAI")
except ImportError as e:
    logger.error(f"Error importing OpenAI: {e}")
    OpenAI = None

try:
    import anthropic
    logger.info("Successfully imported Anthropic")
except ImportError as e:
    logger.error(f"Error importing Anthropic: {e}")
    anthropic = None

try:
    import google.generativeai as genai_client
    logger.info("Successfully imported Google Generative AI")
except ImportError as e:
    logger.error(f"Error importing Google Generative AI: {e}")
    genai_client = None

try:
    import requests
    
    class OpenRouter:
        def __init__(self, api_key):
            self.api_key = api_key
            self.base_url = "https://openrouter.ai/api/v1"
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://pinkpixel.dev",  # Replace with your site
                "X-Title": "ComfyUI Prompt Enhancer"  # Name of your application
            }
            logger.info("OpenRouter client initialized with API key")
        
        def chat_completions(self, model, messages, temperature=0.7):
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            logger.info(f"Making request to OpenRouter with model: {model}")
            try:
                response = requests.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                logger.info("Successfully received response from OpenRouter")
                return data
            except requests.exceptions.RequestException as e:
                logger.error(f"Error making request to OpenRouter: {str(e)}")
                raise
    
    logger.info("Successfully initialized OpenRouter client")
except ImportError as e:
    logger.error(f"Error initializing OpenRouter client: {e}")
    OpenRouter = None

try:
    import torch
    logger.info("Successfully imported PyTorch")
except ImportError as e:
    logger.error(f"Error importing PyTorch: {e}")

try:
    import requests
    logger.info("Successfully imported requests")
except ImportError as e:
    logger.error(f"Error importing requests: {e}")
    requests = None

class PromptEnhancer:
    def __init__(self):
        logger.info("Initializing PromptEnhancer")
        # Get the path to the current directory and config
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(current_dir, "config", "llm_config.json")
        logger.info(f"Config path: {self.config_path}")
        self.clients = {}
        self.api_keys = {}
        self.ollama_host = "http://localhost:11434"  # Default Ollama host
        self.enhanced_prompt = ""  # Store the enhanced prompt
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        
        # Define style prompts
        self.style_prompts = {
            "none": "",  # Empty prompt for no style modification
            "detailed": "Start prompt with detailed. Convert this into a hyper-detailed visual description with precise technical specifications...",
            "photorealistic": "Start prompt with photorealistic. Convert this into a hyperdetailed photorealistic description with sharp focus, precise technical and visual details...",
            "cinematic": "Start prompt with cinematic. Convert this into a cinematic shot with cincematic composition, hyperdetailed, sharp focus, dynamic lighting, precise film techniques...",
            "artistic": "Start prompt with artistic. Convert this into a sophisticated artwork emphasizing advanced artistic techniques...",
            "minimalist": "Start prompt with minimalist. Convert this into a minimalist artwork with precise reductive elements...",
            "fantasy": "Start prompt with fantasy. Convert this into a fantasy-themed artwork with precise magical specifications...",
            "horror": "Start prompt with horror. Convert this into dark horror with precise unsettling specifications...",
            "dark fantasy": "Start prompt with dark fantasy. Convert this into dark fantasy with precise gothic and supernatural specifications...",
            "vibrant": "Start prompt with vibrant. Convert this into a vibrant artwork with precise color specifications...",
            "heavenly": "Start prompt with heavenly. Convert this into a celestial, ethereal artwork with precise divine specifications...",
            "oil painting": "Start prompt with oil painting. Convert this into a classical oil painting with precise traditional specifications...",
            "watercolor": "Start prompt with watercolor. Convert this into a watercolor artwork with precise aqueous specifications...",
            "abstract expressionist": "Start prompt with abstract expressionist. Convert this into an abstract expressionist artwork with precise gestural specifications...",
            "hyperrealist": "Start prompt with hyperrealist. Convert this into a hyperrealistic artwork with extreme precision...",
            "cubist": "Start prompt with cubist. Convert this into a cubist artwork with specific geometric deconstruction...",
            "bauhaus": "Start prompt with Bauhaus. Convert this into a Bauhaus style artwork with specific design principles...",
            "romanticist": "Start prompt with romanticist. Convert this into a romanticist artwork with emotional and natural elements...",
            "dada": "Start the prompt with the word dada. Convert this into a Dada artwork with specific anti-art elements...",
            "street art": "Start prompt with street art. Convert this into street art with specific urban art techniques...",
            "anime": "Start the prompt with the word anime. Convert this into an anime-style artwork with precise animation techniques. Detail the character elements (large expressive eyes with 3-4 highlight points at 100% opacity, simplified facial features with strong emotional expressions, dynamic hair with wind physics and 20-30 distinct strands, color palette with 4-5 tonal values per element), shading techniques (cel-shading with hard edges at 85% opacity, ambient occlusion at 40% strength for depth, rim lighting at 90% intensity for edge definition), action elements (speed lines at 45-degree angles with 70% opacity, impact frames with radial blur at 25% strength, motion smears for quick movements), and background treatment (detailed establishing shots with 3-point perspective, simplified backgrounds during character focus with 20% detail retention). Include standard anime visual elements (dramatic lighting effects with stark shadows, sweat drops and anger veins for emotion, sparkles and floating petals for atmosphere), facial features (eyes at 1/3 head height, small nose and mouth with minimal detail, varied expressions from chibi to serious), and costume dynamics (flowing fabric with secondary motion, dramatic poses with foreshortening, cloth folds following form)...",
            "studio ghibli": "Start the prompt with the words studio ghibli. Convert this into a Studio Ghibli inspired artwork with their signature animation style. Detail the environmental elements (layered clouds with cumulus structure and 30% opacity variation, grass plains with individual blade definition and wind animation patterns, trees with organic movement and dappled light effects), character design (rounded, soft features with minimal sharp angles, expressive faces with 2-3 highlight points in eyes, natural hair movement with subtle physics), color treatment (pastel base palette with 80% saturation, warm sunlight tones #FFE5B4 to #FFB347, natural color gradients with 10% steps between values), and atmospheric effects (floating particles with 2-second fade cycle, gentle wind effects at 5mph affecting foliage and fabric, dynamic skies with 3-5 cloud layers). Include signature elements (food scenes with exaggerated texture and steam effects, flying sequences with dynamic camera movements, cozy interior spaces with lived-in details), lighting techniques (soft diffused sunlight at 30-degree angle, ambient occlusion at 15% strength for depth, warm interior lighting with 2700K color temperature), and background details (European-inspired architecture with weathered textures, detailed mechanical designs with functional components, natural environments with ecological accuracy)...",
            "3d render": "Start prompt with 3d render. Convert this into a 3D render with precise technical specifications...",
            "digital art": "Start prompt with digital art. Convert this into digital art with precise contemporary techniques...",
            "studio photography": "Start prompt with studio photography. Convert this into a studio photograph with precise technical setup...",
            "concept art": "Start prompt with concept art. Convert this into concept art with precise production art techniques...",
            "comic book": "Start the prompt with comic book. Convert this into a comic book illustration with precise stylistic elements. Detail the line art (bold outlines at 3-4px thickness, dynamic speed lines for motion, dramatic perspective with exaggerated foreshortening), coloring technique (flat colors with cel-shading, 4-color limited palette reminiscent of vintage comics, high contrast shadows at 80% opacity), panel composition (dramatic angles, extreme close-ups mixed with wide shots, Dutch angles for tension), and comic-specific elements (halftone dot patterns at 15-30% density, action effects like impact lines and motion blur, bold onomatopoeia text effects). Include signature comic art features (heroic poses with exaggerated proportions, dramatic facial expressions with heavy shadows, muscle definition with cross-hatching at 45-degree angles), background treatment (detailed in action scenes, simplified in character moments, speed lines at 60-degree angles), and classic comic book printing aesthetics (slight color misalignment, Ben-Day dots at 20% opacity, paper texture overlay at 10% strength)...",
            "pixel art": "Start the prompt with pixel art. Convert this into precise pixel art with specific technical constraints...",
            "cyberpunk": "Start the prompt with cyberpunk. Convert this into a cyberpunk artwork with specific futuristic elements...",
            "steampunk": "Start the prompt with steampunk. Convert this into a steampunk artwork with specific Victorian-industrial elements...",
            "gothic": "Start the prompt with gothic. Convert this into a gothic artwork with specific architectural and atmospheric elements...",
            "art nouveau": "Start the prompt with art nouveau. Convert this into an art nouveau artwork with specific decorative elements...",
            "art deco": "Start the prompt with art deco. Convert this into an art deco artwork with specific geometric elements...",
            "impressionist": "Start the prompt with impressionist. Convert this into an impressionist artwork with specific light-capturing techniques...",
            "surrealist": "Start the prompt with surrealist. Convert this into a surrealist artwork with specific dreamlike elements...",
            "baroque": "Start the prompt with baroque. Convert this into a baroque artwork with elaborate dramatic elements...",
            "renaissance": "Start the prompt with renaissance. Convert this into a renaissance style artwork with precise classical elements...",
            "pop art": "Start the prompt with pop art. Convert this into a pop art artwork with precise commercial art elements...",
            "ukiyo-e": "Start the prompt with ukiyo-e. Convert this into a Japanese ukiyo-e style artwork with precise woodblock print elements...",
            "pencil sketch": "Start the prompt with pencil sketch. Convert this into a detailed pencil sketch with specific traditional drawing techniques...",
            "charcoal drawing": "Start the prompt with charcoal drawing. Convert this into a dramatic charcoal drawing with specific medium characteristics...",
            "pastel art": "Start the prompt with pastel art. Convert this into a vibrant pastel artwork with specific medium techniques...",
            "stained glass": "Start the prompt with stained glass. Convert this into a stained glass artwork with specific technical and design elements...",
            "mosaic": "Start the prompt with mosaic. Convert this into a detailed mosaic artwork with specific tessellation techniques...",
            "isometric": "Start the prompt with isometric. Convert this into a precise isometric artwork with specific technical parameters...",
            "low poly": "Start prompt with low poly. Convert this into a low poly artwork with specific geometric optimization techniques...",
            "vaporwave": "Start prompt with vaporwave. Convert this into a vaporwave aesthetic with precise retro-digital elements...",
            "retro": "Start prompt with retro. Convert this into a retro style artwork with precise period-specific elements...",
            "vintage": "Start prompt with vintage. Convert this into a vintage artwork with precise aging and period effects...",
            "sumi-e": "Start prompt with sumi-e. Convert this into a Japanese ink wash (sumi-e) artwork with precise traditional techniques. Detail the brushwork characteristics (bamboo brush techniques with varying pressure from 0% to 100%, four basic strokes: horizontal 'yan', vertical 'shu', diagonal 'pie', dot 'dian'), ink gradation methods (five distinct ink values: darkest 'nōboku' at 100% concentration, dark 'nōhitsu' at 80%, medium 'chūboku' at 60%, light 'usuboku' at 40%, palest 'usuhitsu' at 20%), paper interaction (washi paper with 30% cotton content, controlled water absorption rates, intentional bleeding effects), and compositional elements (asymmetrical balance with 70/30 rule, negative space 'ma' occupying 60-70% of composition, rhythmic brush movement 'keisei' with varying speeds 1-5 cm/second). Include traditional techniques (dry brush 'kasure' for texture, splashed ink 'hatsuboku' with 15-degree angle throws, pooled ink 'tamari' with 3-5mm depth), atmospheric effects (mist achieved through diluted ink at 10% concentration, rain with diagonal strokes at 75-degree angles, wind suggested through directional brushwork), and subject treatment (simplified forms with maximum 3-5 brushstrokes, captured essence 'sēshin' through minimal detail, dynamic tension through line weight variation 0.5mm to 5mm)..."
        }
        
        # Define style categories for organization
        self.style_categories = {
            "Basic Styles": ["none", "detailed", "photorealistic", "cinematic", "artistic", 
                           "minimalist", "vibrant"],
            "Fantasy & Horror": ["fantasy", "horror", "dark fantasy", "heavenly"],
            "Traditional Art": ["oil painting", "watercolor", "abstract expressionist", 
                              "hyperrealist", "cubist"],
            "Art Movements": ["art nouveau", "art deco", "baroque", "renaissance", "pop art", "bauhaus", 
                            "romanticist", "dada"],
            "Asian Art Styles": ["anime", "studio ghibli", "ukiyo-e", "sumi-e"],
            "Traditional Media": ["oil painting", "watercolor", "pencil sketch", 
                                "charcoal drawing", "pastel art"],
            "Digital & Contemporary": ["3d render", "digital art", "concept art", "comic book", 
                                     "pixel art", "low poly", "isometric"],
            "Genre & Theme": ["cyberpunk", "steampunk", "gothic", "vaporwave", "retro", "vintage"],
            "Decorative Arts": ["stained glass", "mosaic", "street art"]
        }
        
        self._load_config()
    
    @classmethod
    def INPUT_TYPES(cls):
        providers = ["openai", "anthropic", "google", "ollama", "openrouter"]
            
        # Define categories and their styles
        style_categories = {
            "Basic Styles": ["none", "detailed", "photorealistic", "cinematic", "artistic", 
                           "minimalist", "vibrant"],
            "Fantasy & Horror": ["fantasy", "horror", "dark fantasy", "heavenly"],
            "Traditional Art": ["oil painting", "watercolor", "abstract expressionist", 
                              "hyperrealist", "cubist"],
            "Art Movements": ["art nouveau", "art deco", "baroque", "renaissance", "pop art", "bauhaus", 
                            "romanticist", "dada"],
            "Asian Art Styles": ["anime", "studio ghibli", "ukiyo-e", "sumi-e"],
            "Traditional Media": ["oil painting", "watercolor", "pencil sketch", 
                                "charcoal drawing", "pastel art"],
            "Digital & Contemporary": ["3d render", "digital art", "concept art", "comic book", 
                                     "pixel art", "low poly", "isometric"],
            "Genre & Theme": ["cyberpunk", "steampunk", "gothic", "vaporwave", "retro", "vintage"],
            "Decorative Arts": ["stained glass", "mosaic", "street art"]
        }

        # Create a flattened list of all styles with category prefixes
        all_styles = []
        for category, styles in style_categories.items():
            all_styles.extend([f"{category} > {style}" for style in styles])
        
        return {
            "required": {
                "clip": ("CLIP", ),
                "prompt": ("STRING", {"multiline": True, "default": "", "dynamicPrompts": False}),
                "llm_provider": (providers, {"default": "openai"}),
                "style": (all_styles, {"default": "Basic Styles > none"}),
            },
            "optional": {
                "openai_key": ("STRING", {"multiline": False, "default": ""}),
                "anthropic_key": ("STRING", {"multiline": False, "default": ""}),
                "google_key": ("STRING", {"multiline": False, "default": ""}),
                "openrouter_key": ("STRING", {"multiline": False, "default": ""}),
                "openrouter_model": ("STRING", {"multiline": False, "default": "google/gemma-2-9b-it:free"}),
                "ollama_host": ("STRING", {"multiline": False, "default": ""}),
                "ollama_model": ("STRING", {"multiline": False, "default": "llama3.2:1b"})
            }
        }

    CATEGORY = "conditioning/prompt"
    FUNCTION = "enhance_prompt"
    OUTPUT_NODE = True
    RETURN_TYPES = ("CONDITIONING", "STRING",)
    RETURN_NAMES = ("conditioning", "enhanced_prompt",)
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False, False)

    @classmethod
    def DISPLAY_NAME(cls):
        return "Prompt Enhancer LLM "

    def enhance_prompt(self, clip, prompt, llm_provider, style, 
                      openai_key="", anthropic_key="", google_key="",
                      openrouter_key="", openrouter_model="google/gemma-2-9b-it:free",
                      ollama_host="http://localhost:11434", ollama_model="llama3.2:1b"):
        """Enhance the input prompt using the specified LLM provider and style."""
        try:
            if llm_provider == "none":
                return (clip, prompt)

            # Extract the actual style from the category > style format
            enhancement_style = style.split(" > ")[-1]
            
            # Skip if it's a category header
            if enhancement_style.startswith('[') and enhancement_style.endswith(']'):
                enhancement_style = "detailed"  # Use default if category header is somehow selected
            
            # Handle each provider
            if llm_provider == "openai":
                if not openai_key:
                    raise ValueError("OpenAI API key is required")
                client = OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": "You are an expert at writing image generation prompts. Convert the input into a clear, descriptive prompt that directly describes the desired image. Focus on nouns, adjectives, and visual elements. Do not reference specific characters, shows, movies or books unless asked to do so. Do not include instructions like 'create', 'make', or 'generate'. Do not start the prompt with imagine or create.Format the output as a simple description. Keep it to 5 sentences. Set descriptiveness to medium. Plain text output only. No formatting. Only the prompt itself no additional text. Do not use quotations. Output to stable diffusion."},
                        {"role": "user", "content": f"{self.style_prompts[enhancement_style]} {prompt}"}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                enhanced_prompt = response.choices[0].message.content.strip()
                
            elif llm_provider == "anthropic":
                if not anthropic_key:
                    raise ValueError("Anthropic API key is required")
                client = anthropic.Client(api_key=anthropic_key)
                response = client.messages.create(
                    model="claude-3.5-sonnet",
                    max_tokens=200,
                    messages=[
                        {"role": "user", "content": f"You are an expert at writing image generation prompts. Convert the input into a clear, descriptive prompt that directly describes the desired image. Focus on nouns, adjectives, and visual elements. Do not reference specific characters, shows, movies or books unless asked to do so. Do not include instructions like 'create', 'make', or 'generate'. Do not start the prompt with imagine or create.Format the output as a simple description. Keep it to 5 sentences. Set descriptiveness to medium. Plain text output only. No formatting. Only the prompt itself no additional text. Do not use quotations. Output to stable diffusion.\n\n{self.style_prompts[enhancement_style]} {prompt}"}
                    ]
                )
                enhanced_prompt = response.content[0].text.strip()
                
            elif llm_provider == "google":
                if not google_key:
                    raise ValueError("Google API key is required")
                genai_client.configure(api_key=google_key)
                model = genai_client.GenerativeModel('gemini-pro')
                response = model.generate_content(
                    f"You are an expert at writing image generation prompts. Convert the input into a clear, descriptive prompt that directly describes the desired image. Focus on nouns, adjectives, and visual elements. Do not reference specific characters, shows, movies or books unless asked to do so. Do not include instructions like 'create', 'make', or 'generate'. Do not start the prompt with imagine or create.Format the output as a simple description. Keep it to 5 sentences. Set descriptiveness to medium. Plain text output only. No formatting. Only the prompt itself no additional text. Do not use quotations. Output to stable diffusion.\n\n{self.style_prompts[enhancement_style]} {prompt}"
                )
                enhanced_prompt = response.text.strip()
                
            elif llm_provider == "ollama":
                if not requests:
                    raise ValueError("Requests package is required for Ollama support")
                
                # Use provided host or default
                host = ollama_host.strip() if ollama_host.strip() else "http://localhost:11434"
                model_name = ollama_model.strip() if ollama_model.strip() else "llama3.2:1b"
                
                logger.info(f"Using Ollama host: {host}, model: {model_name}")
                
                # Test Ollama connection
                success, message = self._test_ollama_connection(host, model_name)
                if not success:
                    raise ValueError(f"Ollama connection failed: {message}")
                
                system_prompt = "You are an expert at writing image generation prompts. Convert the input into a clear, descriptive prompt that directly describes the desired image. Focus on nouns, adjectives, and visual elements. Do not include instructions like 'create', 'make', or 'generate'. Format the output as a simple description. Start with the focus object of the prompt. Use no more than 5 sentences. Set descriptiveness to medium. Plain text output only. No formatting. Only the prompt itself no additional text. Do not use quotations. Output to stable diffusion."
                user_prompt = f"{self.style_prompts[enhancement_style]} {prompt}"
                
                url = f"{host}/api/generate"
                payload = {
                    "model": model_name,
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False
                }
                
                try:
                    response = requests.post(url, json=payload, timeout=30)
                    response.raise_for_status()
                    response_data = response.json()
                    enhanced_prompt = response_data.get("response", "").strip()
                    
                    if not enhanced_prompt:
                        raise ValueError("Empty response from Ollama")
                        
                except requests.exceptions.RequestException as e:
                    raise ValueError(f"Ollama API error: {str(e)}")
                    
            elif llm_provider == "openrouter":
                if not openrouter_key:
                    raise ValueError("OpenRouter API key is required")
                
                if llm_provider not in self.clients:
                    self._initialize_client(llm_provider, openrouter_key)
                
                try:
                    response = self.clients[llm_provider].chat_completions(
                        model=openrouter_model,
                        messages=[
                            {"role": "system", "content": "You are an expert at writing image generation prompts. Convert the input into a clear, descriptive prompt that directly describes the desired image. Focus on nouns, adjectives, and visual elements. Do not reference specific characters, shows, movies or books unless asked to do so. Do not include instructions like 'create', 'make', or 'generate'. Do not start the prompt with imagine or create.Format the output as a simple description. Keep it to 5 sentences. Set descriptiveness to medium. Plain text output only. No formatting. Only the prompt itself no additional text. Do not use quotations. Output to stable diffusion."},
                            {"role": "user", "content": f"{self.style_prompts[enhancement_style]} {prompt}"}
                        ],
                        temperature=0.7
                    )
                    
                    if 'choices' not in response or not response['choices']:
                        raise ValueError("No choices in OpenRouter response")
                    
                    enhanced_prompt = response['choices'][0]['message']['content'].strip()
                    logger.info(f"Enhanced prompt from OpenRouter: {enhanced_prompt}")
                except Exception as e:
                    logger.error(f"Error processing OpenRouter response: {str(e)}")
                    raise RuntimeError(f"Failed to enhance prompt with OpenRouter: {str(e)}")
            
            # Store the enhanced prompt for display
            self.enhanced_prompt = enhanced_prompt

            # Create CLIP conditioning
            tokens = clip.tokenize(enhanced_prompt)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)

            # Return conditioning and enhanced prompt
            conditioning = [[cond, {"pooled_output": pooled}]]
            return (conditioning, enhanced_prompt)
            
        except Exception as e:
            logger.error(f"Error enhancing prompt with {llm_provider}: {e}")
            # Return original prompt if enhancement fails
            tokens = clip.tokenize(prompt)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            conditioning = [[cond, {"pooled_output": pooled}]]
            return (conditioning, prompt)

    @classmethod
    def WIDGETS(cls):
        return {
            "text": {
                "widget": "textarea",
                "multiline": True,
                "readonly": True,
                "width": 1000,  # Width in pixels
                "height": 400   # Height in pixels
            }
        }

    def get_full_style_instructions(self):
        """Returns a formatted string of all style instructions."""
        formatted_instructions = []
        
        # Get all categories from INPUT_TYPES
        style_categories = {
            "Basic Styles": ["none", "detailed", "photorealistic", "cinematic", "artistic", 
                           "minimalist", "vibrant"],
            "Fantasy & Horror": ["fantasy", "horror", "dark fantasy", "heavenly"],
            "Traditional Art": ["oil painting", "watercolor", "abstract expressionist", 
                              "hyperrealist", "cubist"],
            "Art Movements": ["art nouveau", "art deco", "baroque", "renaissance", "pop art", "bauhaus", 
                            "romanticist", "dada"],
            "Asian Art Styles": ["anime", "studio ghibli", "ukiyo-e", "sumi-e"],
            "Traditional Media": ["oil painting", "watercolor", "pencil sketch", 
                                "charcoal drawing", "pastel art"],
            "Digital & Contemporary": ["3d render", "digital art", "concept art", "comic book", 
                                     "pixel art", "low poly", "isometric"],
            "Genre & Theme": ["cyberpunk", "steampunk", "gothic", "vaporwave", "retro", "vintage"],
            "Decorative Arts": ["stained glass", "mosaic", "street art"]
        }
        
        # Format instructions by category
        for category, styles in style_categories.items():
            formatted_instructions.append(f"\n=== {category} ===\n")
            for style in styles:
                if style in self.style_prompts:
                    formatted_instructions.append(f"\n{style}:\n{self.style_prompts[style]}")
        
        return "\n".join(formatted_instructions)

    def display_style_instructions(self):
        """Prints the full style instructions to the console."""
        print(self.get_full_style_instructions()) 

    def _load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.api_keys = json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.api_keys = {
                "openai": "",
                "anthropic": "",
                "google": "",
                "openrouter": ""
            }

    def _save_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.api_keys, f)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def _initialize_client(self, provider, api_key=None):
        """Initialize the client for the specified provider."""
        try:
            if api_key:
                self.api_keys[provider] = api_key
            
            if provider == "openai" and OpenAI:
                self.clients[provider] = OpenAI(api_key=self.api_keys[provider])
            elif provider == "anthropic" and anthropic:
                self.clients[provider] = anthropic.Anthropic(api_key=self.api_keys[provider])
            elif provider == "google" and genai_client:
                genai_client.configure(api_key=self.api_keys[provider])
                self.clients[provider] = genai_client
            elif provider == "openrouter":
                self.api_keys[provider] = api_key or self.api_keys.get(provider)
                self.clients[provider] = OpenRouter(api_key=self.api_keys[provider])
            else:
                raise ValueError(f"Provider {provider} not available or not properly imported")
        except Exception as e:
            logger.error(f"Error initializing {provider} client: {e}")
            raise

    def test_google_connection(self, api_key):
        """Test the connection to Google's Generative AI."""
        try:
            if not genai_client:
                logger.error("Google Generative AI package not imported")
                return False, "Google Generative AI package not imported"
            
            genai_client.configure(api_key=api_key)
            model = genai_client.GenerativeModel('gemini-pro')
            
            # Test with a simple prompt
            response = model.generate_content("Test connection.")
            if response and response.text:
                logger.info("Successfully connected to Google Generative AI")
                return True, "Connection successful"
            else:
                logger.error("Failed to get response from Google Generative AI")
                return False, "No response received"
                
        except Exception as e:
            logger.error(f"Error testing Google connection: {e}")
            return False, str(e)

    def _test_ollama_connection(self, host, model):
        """Test the connection to Ollama server."""
        try:
            if not requests:
                return False, "Requests package not installed"
            
            # Validate host URL
            if not host.startswith(('http://', 'https://')):
                return False, f"Invalid Ollama host URL: {host}. Must start with http:// or https://"
                
            url = f"{host}/api/generate"
            try:
                response = requests.post(url, json={
                    "model": model,
                    "prompt": "test",
                    "stream": False
                }, timeout=5)
                
                if response.status_code == 404 and "model not found" in response.text.lower():
                    return False, f"Model {model} not found. Please run 'ollama pull {model}' first."
                elif response.status_code != 200:
                    return False, f"Failed to connect to Ollama server at {host}: {response.text}"
                
                return True, "Connection successful"
                
            except requests.exceptions.RequestException as e:
                return False, f"Failed to connect to Ollama server at {host}: {str(e)}"
            
        except Exception as e:
            return False, f"Error connecting to Ollama server: {str(e)}"