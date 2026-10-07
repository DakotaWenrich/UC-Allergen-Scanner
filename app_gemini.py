"""UC-Allergen-Scanner: AI prototype (Option A).
Upload a photo of a food label or meal (or type ingredients) and get
allergens + Ulcerative Colitis / Crohn's trigger flags with confidence scores.
Not medical advice."""
import json, os
import streamlit as st
from google import genai
from google.genai import types

MODEL = "gemini-3.7-flash"  # if you get a "model not found" error, check ai.google.dev for the current name
ALLERGENS = ["Milk", "Egg", "Fish", "Shellfish", "Tree nuts", "Peanuts", "Wheat/Gluten", "Soy", "Sesame"]
BADGE = {"green": "🟢 Low risk", "yellow": "🟡 Caution", "red": "🔴 High risk"}

st.set_page_config(page_title="UC Allergen Scanner", page_icon="🥗")
st.title("🥗 UC Allergen Scanner")
st.caption("Scan a label or meal for allergens and Ulcerative Colitis / Crohn's triggers.")

# ---- Sidebar: personal profile ----
with st.sidebar:
    st.header("My profile")
    condition = st.selectbox("Condition", ["Ulcerative Colitis", "Crohn's disease", "Both / unsure"])
    phase = st.radio("Current phase", ["Remission", "Active flare"])
    my_allergens = st.multiselect("My allergies", ALLERGENS)
    stricture = st.checkbox("I have strictures / narrowing (avoid high-fiber, seeds, skins)")
    custom = st.text_input("Other personal triggers (comma separated)", "")
    api_key = st.text_input("Gemini API key (free)", type="password",
                            value=os.getenv("GEMINI_API_KEY", ""))

# ---- Input ----
tab1, tab2 = st.tabs(["📷 Photo", "⌨️ Type ingredients"])
with tab1:
    kind = st.radio("What is it?", ["Ingredient label", "Prepared meal"], horizontal=True)
    photo = st.file_uploader("Upload or take a photo", type=["jpg", "jpeg", "png", "webp"])
    if photo:
        st.image(photo, width=300)
with tab2:
    typed = st.text_area("Paste ingredients or describe the food")

PROMPT = f"""You are a food-safety assistant for a person with {condition}, currently in {phase.lower()}.
Their allergies: {my_allergens or 'none listed'}. Strictures: {stricture}. Other triggers: {custom or 'none'}.
Analyze the food (read the label via OCR, or estimate ingredients if it is a meal photo).
Flag the major allergens, plus common IBD triggers: dairy/lactose, gluten, high-FODMAP items, insoluble fiber,
seeds/nuts/skins, spicy food, alcohol, caffeine, artificial sweeteners (sorbitol, sucralose), carrageenan,
polysorbate 80, carboxymethylcellulose, maltodextrin, high-fat/fried foods. Be stricter if in a flare.
Return ONLY JSON, no markdown, in this shape:
{{"food":"name","ingredients":["..."],"allergens":["..."],"personal_allergen_hit":true,
"triggers":[{{"item":"...","why":"short reason","severity":"green|yellow|red"}}],
"overall":"green|yellow|red","confidence":0-100,"summary":"2 sentences","alternatives":["..."]}}"""

if st.button("Scan", type="primary"):
    if not api_key:
        st.error("Add your API key in the sidebar."); st.stop()
    content = []
    if photo:
        content.append(types.Part.from_bytes(data=photo.getvalue(), mime_type=photo.type))
        content.append(f"This is a photo of a {kind.lower()}.")
    elif typed.strip():
        content.append(f"Food/ingredients: {typed}")
    else:
        st.warning("Upload a photo or type ingredients first."); st.stop()
    content.append(PROMPT)
    with st.spinner("Analyzing..."):
        try:
            client = genai.Client(api_key=api_key)
            resp = client.models.generate_content(model=MODEL, contents=content)
            raw = resp.text.replace("```json", "").replace("```", "").strip()
            r = json.loads(raw)
        except Exception as e:
            st.error(f"Something went wrong: {e}"); st.stop()

    # ---- Results ----
    st.subheader(r.get("food", "Result"))
    st.markdown(f"## {BADGE.get(r['overall'], r['overall'])}")
    st.progress(int(r.get("confidence", 0)) / 100, text=f"Confidence: {r.get('confidence', 0)}%")
    if r.get("personal_allergen_hit"):
        st.error("⚠️ Contains one of YOUR listed allergens!")
    st.write(r.get("summary", ""))
    c1, c2 = st.columns(2)
    c1.markdown("**Allergens found**"); c1.write(", ".join(r.get("allergens", [])) or "None detected")
    c2.markdown("**Ingredients seen**"); c2.write(", ".join(r.get("ingredients", [])))
    st.markdown("**IBD triggers**")
    for t in r.get("triggers", []):
        st.markdown(f"- {BADGE.get(t['severity'], '')} **{t['item']}**: {t['why']}")
    if r.get("alternatives"):
        st.markdown("**Safer swaps:** " + "; ".join(r["alternatives"]))

st.divider()
st.caption("⚠️ Educational prototype, not medical advice. AI can misread labels. "
           "Always check the real label and talk to your GI doctor or dietitian.")
