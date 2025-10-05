import streamlit as st
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="Miraz's Solution",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="auto",
)

# Small CSS tweaks
st.markdown(
    """
    <style>
    /* hide menu/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Button style */
    div.stButton > button {
        border-radius: 10px;
        padding: 10px 22px;
        font-size: 1rem;
        font-weight: 600;
    }
    /* Card-like padding */
    section.main > div.block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
    }
    /* Make results area stand out */
    .result-box {
        border-radius: 12px;
        padding: 12px;
        background: #ffffff;
        box-shadow: 0 6px 18px rgba(14, 30, 37, 0.06);
        border: 1px solid rgba(15,23,42,0.03);
    }
    </style>
    """, unsafe_allow_html=True
)

# Assets path
ASSETS = "assets"

# Header
col1, col2 = st.columns([1, 5], gap="small")
with col1:
    logo_path = os.path.join(ASSETS, "icons", "logo.png")
    try:
        st.image(logo_path, width=72)
    except:
        st.write("")
with col2:
    st.markdown("<h1 style='margin:0'>Miraz's Solution</h1>", unsafe_allow_html=True)
    st.markdown("<div style='color:#6b7280; margin-top:2px'>Smart Waste Sorter — Demo</div>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    mode = st.selectbox("Mode", ["Demo (Keyword)", "Advanced (future)"])
    show_icons = st.checkbox("Show category icons", value=True)
    st.write("App version: demo-v1")
    st.markdown("---")
    st.markdown("Made with ❤️ for Miraz")

# Main layout
left, right = st.columns([3,1], gap="medium")
with left:
    st.subheader("Analyze an item")
    uploaded = st.file_uploader("Upload an image (jpg/png) — optional", type=["jpg","jpeg","png"])
    desc = st.text_input("Or type a short description (e.g., 'plastic bottle', 'banana peel')")
    analyze = st.button("Analyze")

    if analyze:
        if not uploaded and not desc:
            st.warning("Please upload an image or type a description to analyze.")
        else:
            # show uploaded image preview
            if uploaded:
                try:
                    img = Image.open(uploaded)
                    st.image(img, caption="Preview", use_column_width=True)
                except Exception as e:
                    st.error(f"Could not open image: {e}")
            combined = ""
            if desc:
                combined += desc.strip()
            if uploaded:
                combined += " " + uploaded.name
            # simple keyword mapping
            def keyword_map(text: str):
                t = text.lower()
                mapping = {
                    "Plastic": ["plastic","bottle","wrapper","container","bag","packet"],
                    "Glass": ["glass","bottle","jar","wine"],
                    "Paper": ["paper","newspaper","cardboard","book","envelope"],
                    "Metal": ["metal","can","tin","aluminum","screw","nail"],
                    "Compostable": ["banana","peel","fruit","vegetable","organic","leaf","food"],
                    "Electronic": ["phone","laptop","computer","battery","charger","camera","screen"],
                    "Hazardous": ["battery","needle","syringe","chemical","paint","pesticide","lighter","match"]
                }
                for cat, kws in mapping.items():
                    for k in kws:
                        if k in t:
                            return cat
                return "General / Unknown"
            result = keyword_map(combined)
            # display result box
            st.markdown(f"<div class='result-box'><h3 style='margin:0'>Suggested category: <span style='color:#0b6efd'>{result}</span></h3></div>", unsafe_allow_html=True)
            # show icon and guidance
            icon_map = {
                "Plastic": os.path.join(ASSETS,"icons","plastic.png"),
                "Glass": os.path.join(ASSETS,"icons","glass.png"),
                "Paper": os.path.join(ASSETS,"icons","paper.png"),
                "Metal": os.path.join(ASSETS,"icons","metal.png"),
                "Compostable": os.path.join(ASSETS,"icons","compost.png"),
                "Electronic": os.path.join(ASSETS,"icons","electronic.png"),
                "Hazardous": os.path.join(ASSETS,"icons","hazardous.png"),
                "General / Unknown": os.path.join(ASSETS,"icons","logo.png"),
            }
            if show_icons:
                try:
                    st.image(icon_map.get(result, icon_map["General / Unknown"]), width=110)
                except:
                    pass
            st.markdown("### Disposal guideline (general)")
            st.write("- **Plastic / Glass / Metal / Paper:** Clean & dry, put into recycling if accepted in your area.")
            st.write("- **Compostable / Organic:** Food scraps and garden waste → compost or organics collection.")
            st.write("- **Electronic:** Bring to e‑waste collection or retailer take-back.")
            st.write("- **Hazardous:** Use local hazardous-waste drop-off; do not put in regular bins.")
            # allow download of result
            result_text = f"Description: {combined}\\nSuggestion: {result}\\n"
            st.download_button("Download result", data=result_text, file_name="miraz_solution_result.txt")

with right:
    st.subheader("Quick actions")
    st.write("• Upload an image or write a description, then press **Analyze**.")
    st.markdown("---")
    st.write("Quick categories")
    cols = st.columns(2)
    cat_list = ["Plastic","Glass","Paper","Metal","Compostable","Electronic","Hazardous"]
    icons = [os.path.join(ASSETS,"icons",f"{c.lower()}.png" if c!="Compostable" else "compost.png") for c in ["plastic","glass","paper","metal","compost","electronic","hazardous"]]
    for i, (c, ic) in enumerate(zip(cat_list, icons)):
        try:
            cols[i % 2].image(ic, width=64)
        except:
            pass
        cols[i % 2].caption(c)

st.markdown("---")
with st.expander("Tips to improve accuracy"):
    st.write("""
    - This demo uses simple keyword mapping for instant, lightweight results.
    - To get better accuracy: collect local images, label them, and use a small image model (MobileNet/EfficientNet) to fine-tune.
    - Add translations (e.g., Bangla) for local users.
    """)

st.markdown("<div style='text-align:center; color:#6b7280; padding-top:6px'>Made with ❤️ — Miraz's Solution</div>", unsafe_allow_html=True)