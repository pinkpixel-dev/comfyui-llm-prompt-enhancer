import { app } from "/scripts/app.js";

// Style categories and their corresponding styles
const styleCategories = {
    "No Style": ["none"],
    "Core Styles": ["detailed", "photorealistic", "cinematic", "artistic", "minimal"],
    "Fantasy & Horror": ["fantasy", "horror", "dark fantasy", "heavenly"],
    "Modern Aesthetics": ["cyberpunk", "steampunk", "street art", "vaporwave"],
    "Art Movements": ["abstract", "expressionist", "abstract expressionist", "futurist", "surrealist", 
                    "art nouveau", "art deco", "baroque", "renaissance", "pop art", "bauhaus", 
                    "romanticist", "dada"],
    "Asian Art Styles": ["anime", "studio ghibli", "ukiyo-e", "sumi-e", "howls castle"],
    "Traditional Media": ["oil painting", "watercolor", "gouache", "pencil sketch", 
                        "charcoal drawing", "pastel art"],
    "Digital & Contemporary": ["3d render", "digital art", "concept art", "comic book", 
                             "pixel art", "low poly", "isometric"],
    "Photography & Studio": ["studio photography", "vibrant"],
    "Decorative Arts": ["stained glass", "mosaic", "gothic"],
    "Period & Style": ["retro", "vintage"]
};

app.registerExtension({
    name: "pinkpixel.prompt_enhancer",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "PromptEnhancer") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                // Get widget indices
                const categoryIndex = this.widgets.findIndex(w => w.name === "style_category");
                const styleIndex = this.widgets.findIndex(w => w.name === "style");

                if (categoryIndex === -1 || styleIndex === -1) return r;

                // Add callback to category widget
                const categoryWidget = this.widgets[categoryIndex];
                const styleWidget = this.widgets[styleIndex];

                categoryWidget.callback = function(value) {
                    // Update style widget options based on selected category
                    const styles = styleCategories[value] || ["none"];
                    styleWidget.options.values = styles;
                    styleWidget.value = styles[0];
                    app.graph.setDirtyCanvas(true);
                };

                return r;
            };
        }
    }
});
