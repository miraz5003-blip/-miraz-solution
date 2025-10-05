import streamlit as st
from PIL import Image
import numpy as np
import io
import os

st.set_page_config(page_title="Miraz's Solution — Smart Waste Sorter", page_icon="🗑️", layout="centered")
st.title("Miraz's Solution — Smart Waste Sorter")
st.write("Upload a photo of a waste item and get a suggested disposal category (demo).")

uploaded = st.file_uploader("Upload an image (jpg/png)", type=["jpg","jpeg","png"])

# Lightweight keyword-based mapping from filename/labels (fallback if no ML)
CATEGORY_KEYWORDS = {
    "compostable": ["banana","apple","orange","peel","fruit","vegetable","leaf","food","egg"],
    "glass": ["bottle","wine","beer","jar","glass"],
    "metal": ["can","tin","screw","nail","metal","aluminum","aluminium"],
    "paper": ["newspaper","paper","envelope","book","cardboard","box"],
    "plastic": ["plastic","bottle","container","bag","wrapper","package","packet"],
    "electronic": ["phone","laptop","computer","charger","battery","camera","screen","television"],
    "hazardous": ["battery","needle","syringe","chemical","paint","pesticide","lighter","match"],
    "organic": ["wood","branch","log","leaf","compost","soil"],
}

CATEGORY_LABEL = {
    "compostable": "Compostable / Organic",
    "glass": "Glass (Recyclable)",
    "metal": "Metal (Recyclable)",
    "paper": "Paper / Cardboard (Recyclable)",
    "plastic": "Plastic (Recyclable)",
    "electronic": "Electronic waste (E-waste)",
    "hazardous": "Hazardous waste (Special disposal)",
    "organic": "Organic / Compost",
}

def keyword_map(text: str):
    t = text.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        for k in kws:
            if k in t:
                return CATEGORY_LABEL.get(cat)
    return None

if uploaded is None:
    st.info("No image yet — upload a photo (e.g., plastic bottle, banana peel, battery, paper). You can also type a short description below.")
else:
    try:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded image", use_column_width=True)
    except Exception as e:
        st.error(f"Could not open image: {e}")
        st.stop()

desc = st.text_input("(Optional) Type a short description of the item (e.g., 'plastic bottle', 'banana peel', 'old phone')")

if st.button("Analyze"):
    combined = ""
    if desc:
        combined = desc
    if uploaded:
        # include filename as hint
        combined = (combined + " " + uploaded.name) if combined else uploaded.name
    if not combined:
        st.warning("Please upload an image or type a description to analyze.")
    else:
        suggestion = keyword_map(combined)
        if suggestion:
            st.success(f"Suggested category: {suggestion}")
        else:
            st.info("Couldn't confidently map to a category. Suggestions:\n- Try a clearer description (e.g., 'glass bottle')\n- Or check the item manually based on local rules.")
        st.markdown("---")
        st.write("**How to dispose (general guidance):**")
        st.write("- Compostable / Organic: food scraps, garden waste -> compost or organics collection.")
        st.write("- Glass / Metal / Paper / Plastic: clean & rinse where required, put in recycling if your area accepts it.")
        st.write("- Electronic waste: hand over to e-waste collection or take-back programs.")
        st.write("- Hazardous: never put in regular bins; use hazardous waste drop-off.")
        st.markdown("---")
        st.write("This demo uses simple keyword-matching to suggest categories. For higher accuracy, a trained image model and local waste rules are recommended. See README for improvements.")
        # allow download
        result_text = f"Description: {combined}\nSuggestion: {suggestion or 'Unknown'}\n"
        st.download_button("Download result", data=result_text, file_name="miraz_solution_result.txt")