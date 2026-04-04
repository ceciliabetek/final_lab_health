import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="EA Macro Early Warning", page_icon="📉", layout="wide")

# -------- Load final bundle --------
@st.cache_resource
def load_bundle(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)

BUNDLE_PATH = os.path.join("models", "final_bundle.pkl")

st.title("📉 EA Macro Deceleration Early Warning System")
st.caption("Risk score = predicted probability of a growth deceleration event. Classification uses a decision threshold.")

if not os.path.exists(BUNDLE_PATH):
    st.error(f"Bundle not found: {os.path.abspath(BUNDLE_PATH)}")
    st.stop()

bundle = load_bundle(BUNDLE_PATH)
model = bundle["model"]
model_name = bundle.get("model_name", "Final model")
thr_default = float(bundle.get("threshold", 0.5))
features = list(bundle.get("features", []))

# -------- Sidebar settings --------
st.sidebar.title("⚙️ Settings")
use_custom_thr = st.sidebar.checkbox("Use custom threshold", value=False)
thr = st.sidebar.slider("Threshold", 0.05, 0.95, thr_default, 0.01) if use_custom_thr else thr_default
st.sidebar.write(f"**Model:** {model_name}")
st.sidebar.write(f"**Default threshold:** {thr_default:.2f}")

# -------- Input form --------
st.subheader("1) Enter macro indicators")
if not features:
    st.error("No 'features' found in bundle. Re-save bundle with features=list(feature_cols).")
    st.stop()

# Suggested defaults (edit anytime)
SUGGESTED_DEFAULTS = {
    "IMF_WEO_NGDP_RPCH": 2.0,
    "IMF_WEO_LUR": 7.0,
    "IMF_WEO_LP": 1.0,
    "IMF_WEO_PCPIPCH": 2.0,
    "IMF_WEO_TM_RPCH": 3.0,
    "IMF_WEO_TX_RPCH": 3.0,
    "IMF_WEO_BCA_NGDPD": -2.0,
    "IMF_WEO_NGAP_NPGDP": 0.0,
    "IMF_WEO_NGSD_NGDP": 20.0,
}

cols = st.columns(3)
inputs = {}
for i, feat in enumerate(features):
    with cols[i % 3]:
        val0 = float(SUGGESTED_DEFAULTS.get(feat, 0.0))
        inputs[feat] = st.number_input(feat, value=val0, step=0.1, format="%.3f")

x = pd.DataFrame([inputs], columns=features)

# -------- Predict --------
st.subheader("2) Risk score & classification")

try:
    proba = float(model.predict_proba(x)[:, 1][0])
except Exception as e:
    st.error(f"Prediction error: {e}")
    st.stop()

proba = max(0.0, min(1.0, proba))
pred = int(proba >= thr)

left, mid, right = st.columns([1.2, 1.0, 1.2])

with left:
    st.metric("Risk score (probability)", f"{proba:.3f}")
    st.progress(int(round(proba * 100)))

with mid:
    st.markdown("#### Classification")
    if pred == 1:
        st.error(f"⚠️ DECELERATION RISK = 1  (p ≥ {thr:.2f})")
    else:
        st.success(f"✅ DECELERATION RISK = 0  (p < {thr:.2f})")

with right:
    st.markdown("#### Risk bucket")
    if proba < 0.20:
        st.success("🟢 Low")
    elif proba < 0.50:
        st.warning("🟠 Medium")
    else:
        st.error("🔴 High")

with st.expander("Show input vector"):
    st.dataframe(x, use_container_width=True)
# notebook/app.py
import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="EA Macro Early Warning", page_icon="📉", layout="wide")

# -----------------------------
# Helpers
# -----------------------------
def clamp01(x: float) -> float:
    return float(max(0.0, min(1.0, x)))

def risk_bucket(p: float) -> str:
    if p < 0.20:
        return "Low"
    if p < 0.50:
        return "Medium"
    return "High"

def bucket_badge(p: float) -> str:
    # emoji badge for quick visual
    if p < 0.20:
        return "🟢 Low"
    if p < 0.50:
        return "🟠 Medium"
    return "🔴 High"

# Streamlit cache: load model bundle once
@st.cache_resource
def load_bundle(path: str) -> dict:
    with open(path, "rb") as f:
        return pickle.load(f)

# -----------------------------
# Paths
# -----------------------------
# Run command used: py -m streamlit run notebook\app.py
# That means CWD is project root, so models/ is found here.
BUNDLE_PATH = os.path.join("models", "final_bundle.pkl")

# -----------------------------
# Header
# -----------------------------
st.title("📉 EA Macro Deceleration Early Warning System")
st.caption(
    "This app computes a **Risk Score** (predicted probability of a growth deceleration event) "
    "and a **binary classification** using a decision threshold."
)

# -----------------------------
# Load bundle
# -----------------------------
if not os.path.exists(BUNDLE_PATH):
    st.error(f"Model bundle not found: {os.path.abspath(BUNDLE_PATH)}")
    st.info(
        "Fix:\n"
        "1) Make sure `final_bundle.pkl` exists inside your project `models/` folder.\n"
        "2) Example copy:\n"
        "   copy C:\\Users\\Kelvin\\Downloads\\models\\final_bundle.pkl .\\models\\final_bundle.pkl"
    )
    st.stop()

bundle = load_bundle(BUNDLE_PATH)

model = bundle.get("model", None)
model_name = bundle.get("model_name", "Final model")
thr_default = float(bundle.get("threshold", 0.5))
features = list(bundle.get("features", []))
saved_at = bundle.get("saved_at", "")

if model is None:
    st.error("Bundle loaded but does not contain a 'model' key.")
    st.stop()

if not features:
    st.error("Bundle loaded but does not contain a non-empty 'features' list.")
    st.stop()

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.title("⚙️ Settings")
st.sidebar.write(f"**Model:** {model_name}")
if saved_at:
    st.sidebar.write(f"**Saved at:** {saved_at}")
st.sidebar.write(f"**Default threshold:** {thr_default:.2f}")

use_custom_thr = st.sidebar.checkbox("Use custom threshold", value=False)
thr = (
    st.sidebar.slider("Decision threshold", 0.05, 0.95, thr_default, 0.01)
    if use_custom_thr
    else thr_default
)

st.sidebar.divider()
st.sidebar.caption("Tip: Keep feature definitions consistent with training for reliable predictions.")

# -----------------------------
# Suggested defaults (edit anytime)
# -----------------------------
SUGGESTED_DEFAULTS = {
    "IMF_WEO_NGDP_RPCH": 2.0,    # GDP growth %
    "IMF_WEO_LUR": 7.0,          # Unemployment %
    "IMF_WEO_LP": 1.0,           # (as in your dataset)
    "IMF_WEO_PCPIPCH": 2.0,      # Inflation %
    "IMF_WEO_TM_RPCH": 3.0,      # Imports growth %
    "IMF_WEO_TX_RPCH": 3.0,      # Exports growth %
    "IMF_WEO_BCA_NGDPD": -2.0,   # Current account balance % GDP
    "IMF_WEO_NGAP_NPGDP": 0.0,   # Output gap %
    "IMF_WEO_NGSD_NGDP": 20.0,   # Gross national savings % GDP
}

# -----------------------------
# Input section
# -----------------------------
st.subheader("1) Enter macro indicators")
st.write("Fill the input values below. Then the app returns risk score + classification.")

cols = st.columns(3)
inputs = {}

for i, feat in enumerate(features):
    with cols[i % 3]:
        default_val = float(SUGGESTED_DEFAULTS.get(feat, 0.0))
        inputs[feat] = st.number_input(
            label=feat,
            value=default_val,
            step=0.1,
            format="%.3f",
            help="Enter the value for this feature."
        )

x = pd.DataFrame([inputs], columns=features)

# -----------------------------
# Predict
# -----------------------------
st.subheader("2) Risk score & classification")

try:
    proba = float(model.predict_proba(x)[:, 1][0])
except Exception as e:
    st.error("Prediction failed. Common causes:")
    st.write("- Feature names/order mismatch with training")
    st.write("- Model was trained with a preprocessing pipeline but inputs are not matching")
    st.code(str(e))
    st.stop()

proba = clamp01(proba)
pred = int(proba >= thr)

left, mid, right = st.columns([1.2, 1.0, 1.2])

with left:
    st.metric("Risk score (probability)", f"{proba:.3f}")
    st.progress(int(round(proba * 100)))

with mid:
    st.markdown("#### Classification")
    if pred == 1:
        st.error(f"⚠️ DECELERATION RISK = 1  (p ≥ {thr:.2f})")
    else:
        st.success(f"✅ DECELERATION RISK = 0  (p < {thr:.2f})")

with right:
    st.markdown("#### Risk bucket")
    bucket = risk_bucket(proba)
    if bucket == "Low":
        st.success(bucket_badge(proba))
    elif bucket == "Medium":
        st.warning(bucket_badge(proba))
    else:
        st.error(bucket_badge(proba))

# -----------------------------
# Show input vector
# -----------------------------
with st.expander("Show input vector used for prediction"):
    st.dataframe(x, width="stretch")

# -----------------------------
# Optional: quick explainability for Logistic Regression
# -----------------------------
with st.expander("Explainability (if Logistic Regression)"):
    if hasattr(model, "coef_") and hasattr(model, "intercept_"):
        coefs = pd.Series(model.coef_[0], index=features).sort_values(key=np.abs, ascending=False)
        st.write("Top coefficients by absolute magnitude (sign indicates direction of risk):")
        st.dataframe(coefs.to_frame("coef").head(15), width="stretch")
        st.caption("Note: Interpretation assumes the same feature scaling/processing as during training.")
    else:
        st.info("Loaded model does not expose coefficients (not a plain LogisticRegression).")

# -----------------------------
# Footer
# -----------------------------
st.caption(
    "Output: Risk score is a probability (0..1). Classification uses threshold. "
    "For early-warning systems, threshold is often chosen to favor Recall (missed events minimized)."
)