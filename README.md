# UC-Allergen-Scanner
 
An AI-powered app that scans a food label or meal photo and flags **allergens** and **trigger ingredients for Ulcerative Colitis and Crohn's disease**, personalized to the user's profile.
 
> ⚠️ Educational prototype, not medical advice. AI can misread labels. Always check the real label and talk to your GI doctor or dietitian.
 
## The problem
Reading ingredient labels with UC or Crohn's is stressful. Standard allergen apps only flag the top major allergens, and miss common IBD irritants like carrageenan, polysorbate 80, cellulose gum, artificial sweeteners and high-FODMAP ingredients.
 
## What it does
- **Photo or text input:** upload a label (OCR) or a meal photo (vision), or type in ingredients.
- **Personal profile:** condition, remission vs. active flare, allergies, strictures, and custom triggers. Flare mode is stricter.
- **Traffic-light risk:** 🟢 low, 🟡 caution, 🔴 high, with a short reason for every flagged ingredient.
- **Confidence score** so users know when the AI is unsure.
- **Safer swaps** for flagged foods.
## Screenshots
![Profile sidebar](screenshots/profile.png)
![Upload a label](screenshots/upload.png)
![Result](screenshots/result.png)
![IBD triggers and swaps](screenshots/triggers.png)
 
## How AI is used
A multimodal Gemini model reads the image, extracts ingredients, and reasons over them against the user's profile. The model returns structured JSON, which the app turns into the badge, triggers and swaps.
 
## Run it yourself
1. Install Python 3.9+.
2. Install packages: `pip install streamlit google-genai`
3. Get a free API key at https://aistudio.google.com
4. Start the app: `python -m streamlit run app_gemini.py`
5. Paste your key in the sidebar. **Never commit your key to GitHub.**
(`app.py` is an equivalent version that uses the Anthropic API instead.)
 
## Roadmap
- More conditions (celiac disease, IBS, GERD) and custom trigger lists saved between sessions
- Figma design for a mobile experience (see `PLAN.md`)
- Short video pitch
 
