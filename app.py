"""
app.py

Vartis Care AI — Streamlit Application
CSC 7644: Applied LLM Development - Final Project
Author: Chantel Walker

Main Streamlit interface for the Vartis Care AI resource navigator.
Handles patient info entry, file upload, text input, pipeline
orchestration, results display, and care note generation.
"""

import os
import io
import datetime
import streamlit as st
from dotenv import load_dotenv
from extractor import extract_info

load_dotenv()

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vartis Care AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── NEED TYPE META ────────────────────────────────────────────────────────────
NEED_META = {
    "MEDICATION":  {"icon": "💊", "label": "Medication Assistance",  "color": "#F5A623"},
    "MEDICAL":     {"icon": "🏥", "label": "Medical Care",           "color": "#1B5FA8"},
    "FOOD":        {"icon": "🍎", "label": "Food Assistance",        "color": "#2E8B57"},
    "UTILITY":     {"icon": "⚡", "label": "Utility Assistance",     "color": "#8B4513"},
    "RENT":        {"icon": "🏠", "label": "Rent Assistance",        "color": "#6A0DAD"},
    "HOUSING":     {"icon": "🏘️", "label": "Housing & Shelter",      "color": "#1B5FA8"},
    "EMPLOYMENT":  {"icon": "💼", "label": "Employment Services",    "color": "#C0392B"},
    "CLOTHING":    {"icon": "👗", "label": "Clothing Assistance",    "color": "#16A085"},
}

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Source+Sans+3:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #F0F4FA; }

.vartis-hero {
    background: linear-gradient(135deg, #0D3B7A 0%, #1B5FA8 50%, #2176C7 100%);
    position: relative; overflow: hidden;
}
.vartis-hero::before {
    content:''; position:absolute; top:-40px; right:-40px;
    width:320px; height:320px; background:rgba(245,166,35,0.12); border-radius:50%;
}
.hero-inner {
    display:flex; align-items:center; justify-content:space-between;
    padding:28px 48px; position:relative; z-index:2;
}
.hero-left { display:flex; align-items:center; gap:18px; }
.hero-logo-circle {
    width:60px; height:60px;
    background:linear-gradient(135deg,#F5A623,#F0C040);
    border-radius:50%; display:flex; align-items:center; justify-content:center;
    font-size:26px; box-shadow:0 4px 16px rgba(245,166,35,0.4); flex-shrink:0;
}
.hero-title { font-family:'Playfair Display',serif; font-size:2.1rem; font-weight:700; color:#fff; line-height:1.1; margin:0; }
.hero-subtitle { font-size:0.78rem; font-weight:600; letter-spacing:0.18em; color:#F5A623; text-transform:uppercase; margin:4px 0 0 0; }
.hero-tagline { font-style:italic; color:rgba(255,255,255,0.75); font-size:0.85rem; margin:0; }
.hero-badge { background:rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.25); border-radius:24px; padding:8px 20px; color:#fff; font-size:0.82rem; font-weight:600; display:inline-block; margin-bottom:6px; }
.hero-course { color:rgba(255,255,255,0.55); font-size:0.73rem; letter-spacing:0.08em; text-transform:uppercase; }
.gold-bar { height:5px; background:linear-gradient(90deg,#F5A623 0%,#F0C040 50%,#F5A623 100%); }
.stats-bar { background:#0D3B7A; padding:14px 48px; display:flex; gap:48px; align-items:center; }
.stat-item { text-align:center; }
.stat-number { font-family:'Playfair Display',serif; font-size:1.5rem; font-weight:700; color:#F5A623; display:block; }
.stat-label { font-size:0.72rem; color:rgba(255,255,255,0.65); text-transform:uppercase; letter-spacing:0.08em; }
.stat-divider { width:1px; height:40px; background:rgba(255,255,255,0.15); }

.section-header {
    background:linear-gradient(90deg,#0D3B7A,#1B5FA8); color:white;
    padding:14px 32px; font-size:0.8rem; font-weight:700; letter-spacing:0.15em;
    text-transform:uppercase; display:flex; align-items:center; gap:10px;
}
.section-header-gold {
    background:linear-gradient(90deg,#C47D00,#F5A623); color:white;
    padding:14px 32px; font-size:0.8rem; font-weight:700; letter-spacing:0.15em;
    text-transform:uppercase; display:flex; align-items:center; gap:10px;
}
.profile-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:14px; padding:24px 32px; background:#F5F8FF; }
.profile-card { background:white; border-radius:12px; padding:16px 18px; border-left:4px solid #1B5FA8; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
.profile-card-label { font-size:0.7rem; font-weight:700; color:#8A9AB0; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px; }
.profile-card-value { font-size:1.05rem; font-weight:700; color:#0D3B7A; }
.need-badge { display:inline-flex; align-items:center; gap:5px; background:linear-gradient(135deg,#1B5FA8,#2176C7); color:white; border-radius:20px; padding:5px 14px; font-size:0.75rem; font-weight:700; margin:3px; letter-spacing:0.04em; }
.resource-section-title { display:flex; align-items:center; gap:10px; padding:16px 32px 8px; font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:700; border-bottom:2px solid #E8EFF8; }
.no-results { text-align:center; padding:48px; color:#8A9AB0; font-size:1rem; }
.vartis-footer { background:#0D3B7A; padding:20px 48px; display:flex; justify-content:space-between; align-items:center; margin-top:40px; }
.footer-left { font-family:'Playfair Display',serif; color:white; font-size:1rem; }
.footer-right { color:rgba(255,255,255,0.5); font-size:0.75rem; }

.stTextArea textarea { border:2px solid #E2E8F0 !important; border-radius:10px !important; font-family:'Source Sans 3',sans-serif !important; font-size:0.88rem !important; padding:14px !important; background:#FAFCFF !important; }
.stTextArea textarea:focus { border-color:#1B5FA8 !important; }
.stButton > button { background:linear-gradient(135deg,#1B5FA8 0%,#0D3B7A 100%) !important; color:white !important; border:none !important; border-radius:8px !important; font-weight:700 !important; font-size:1rem !important; padding:14px 0 !important; width:100% !important; box-shadow:0 4px 15px rgba(13,59,122,0.3) !important; }
.stButton > button:hover { background:linear-gradient(135deg,#2176C7 0%,#1B5FA8 100%) !important; transform:translateY(-1px) !important; }
</style>
""", unsafe_allow_html=True)


# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vartis-hero">
  <div class="hero-inner">
    <div class="hero-left">
      <div class="hero-logo-circle">🏥</div>
      <div>
        <p class="hero-title">Vartis Care AI</p>
        <p class="hero-subtitle">Resource Navigator — Patient Advocacy Platform</p>
        <p class="hero-tagline">Connecting patients to verified community resources</p>
      </div>
    </div>
    <div style="text-align:right;">
      <div class="hero-badge">👤 Chantel Walker</div>
      <p class="hero-course">CSC 7644 · Applied LLM Development · LSU</p>
    </div>
  </div>
</div>
<div class="gold-bar"></div>
<div class="stats-bar">
  <div class="stat-item"><span class="stat-number">29+</span><span class="stat-label">Verified Resources</span></div>
  <div class="stat-divider"></div>
  <div class="stat-item"><span class="stat-number">8</span><span class="stat-label">Need Categories</span></div>
  <div class="stat-divider"></div>
  <div class="stat-item"><span class="stat-number">3</span><span class="stat-label">Pipeline Stages</span></div>
  <div class="stat-divider"></div>
  <div class="stat-item"><span class="stat-number">95%</span><span class="stat-label">Faithfulness Target</span></div>
  <div class="stat-divider"></div>
  <div class="stat-item"><span class="stat-number">RAG</span><span class="stat-label">+ Agentic Fallback</span></div>
</div>
""", unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PATIENT INFORMATION FORM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header" style="margin-top:20px;">
  <span>👤</span> PATIENT INFORMATION
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='background:white;padding:24px 32px 28px;'>", unsafe_allow_html=True)
    pi_col1, pi_col2, pi_col3 = st.columns(3)

    with pi_col1:
        st.text_input("Case ID",               placeholder="e.g. VC-2025-0042",          key="pi_case_id")
        st.text_input("Patient Full Name",     placeholder="e.g. Jane Doe",              key="pi_patient_name")
        st.text_input("Date of Birth",         placeholder="MM/DD/YYYY",                 key="pi_dob")

    with pi_col2:
        st.text_input("ZIP Code",              placeholder="e.g. 30318",                 key="pi_zip_code")
        st.text_input("Insurance Name",        placeholder="e.g. Medicaid, Aetna, None", key="pi_insurance_name")
        st.text_input("Insurance ID / Member #", placeholder="Optional",                 key="pi_insurance_id")

    with pi_col3:
        st.text_input("Navigator / Social Worker", placeholder="Your name",              key="pi_navigator")
        st.text_input("Facility / Clinic",         placeholder="e.g. Grady Memorial Hospital", key="pi_facility")
        st.text_input("Visit Date",                placeholder="MM/DD/YYYY",             key="pi_visit_date")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — INTAKE NOTE INPUT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header" style="margin-top:4px;">
  <span>📋</span> UPLOAD PATIENT INTAKE NOTE
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='background:white;padding:24px 32px 8px;'>", unsafe_allow_html=True)
    col_upload, col_paste = st.columns([1, 1], gap="large")

    with col_upload:
        st.markdown(
            "<p style='font-weight:700;color:#0D3B7A;font-size:0.85rem;"
            "text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;'>"
            "📤 Upload .txt or .pdf Intake Note</p>",
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            label="", type=["txt", "pdf"],
            help="Upload a plain text or PDF intake note",
            label_visibility="collapsed"
        )

    with col_paste:
        st.markdown(
            "<p style='font-weight:700;color:#0D3B7A;font-size:0.85rem;"
            "text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;'>"
            "✏️ Or Paste Intake Note Directly</p>",
            unsafe_allow_html=True
        )
        pasted_text = st.text_area(
            label="", height=160,
            placeholder=(
                "Example: Patient is a 42-year-old uninsured female. "
                "Monthly income ~$1,100. ZIP 30318. Cannot afford medications. "
                "Two months behind on rent. Requesting food assistance..."
            ),
            label_visibility="collapsed"
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='padding:16px 32px 24px;background:#F0F4FA;'>", unsafe_allow_html=True)
run_clicked = st.button("🔵  Run Pipeline — Extract & Match Resources")
st.markdown("</div>", unsafe_allow_html=True)


# ── PIPELINE EXECUTION ────────────────────────────────────────────────────────
if run_clicked:
    intake_text = ""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
                intake_text = "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception:
                st.error("Could not read PDF. Please paste the note directly instead.")
        else:
            intake_text = uploaded_file.read().decode("utf-8", errors="ignore")
    elif pasted_text.strip():
        intake_text = pasted_text.strip()

    if not intake_text:
        st.warning("⚠️  Please upload a file or paste an intake note before running the pipeline.")
    else:
        with st.spinner("🔍  Running three-stage pipeline..."):
            try:
                result = extract_info(intake_text)
                st.session_state.result = result
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                st.session_state.result = None


# ══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.result:
    result    = st.session_state.result
    profile   = result.get("profile", {})
    resources = result.get("matched_resources", [])
    mean_conf = result.get("mean_confidence", 0.0)
    fallback  = result.get("fallback_triggered", False)

    # ── EXTRACTED PROFILE ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header" style="margin-top:24px;">
      <span>🧠</span> EXTRACTED PATIENT PROFILE
    </div>
    """, unsafe_allow_html=True)

    ins = (profile.get("insurance_status") or "unknown").title()
    ins_color = {"Uninsured": "#C0392B", "Medicaid": "#2E8B57",
                 "Medicare": "#1B5FA8", "Private": "#8B4513"}.get(ins, "#64748B")

    profile_items = [
        ("Age",            str(profile.get("age") or "—")),
        ("Gender",         (profile.get("gender") or "—").title()),
        ("Monthly Income", f"${profile['income_monthly_usd']:,.0f}"
                           if profile.get("income_monthly_usd") else "—"),
        ("ZIP Code",       profile.get("zip_code")
                           or st.session_state.patient_info.get("zip_code") or "—"),
        ("Household Size", str(profile.get("household_size") or "—")),
        ("Insurance",      ins),
    ]

    cards_html = '<div class="profile-grid">'
    for label, value in profile_items:
        bc = ins_color if label == "Insurance" else "#1B5FA8"
        vc = "#C0392B" if (label == "Insurance" and ins == "Uninsured") else "#0D3B7A"
        cards_html += (
            f'<div class="profile-card" style="border-left-color:{bc};">'
            f'<div class="profile-card-label">{label}</div>'
            f'<div class="profile-card-value" style="color:{vc};">{value}</div>'
            f'</div>'
        )
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    needs = profile.get("needs") or []
    if needs:
        badges = "".join(
            f'<span class="need-badge">'
            f'{NEED_META.get(n.upper(), {}).get("icon","•")} '
            f'{NEED_META.get(n.upper(), {}).get("label", n)}'
            f'</span>'
            for n in needs
        )
        st.markdown(
            f'<div style="padding:12px 32px 20px;background:#F5F8FF;">'
            f'<p style="font-size:0.72rem;font-weight:700;color:#8A9AB0;'
            f'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Identified Needs</p>'
            f'{badges}</div>',
            unsafe_allow_html=True
        )

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Resources Matched", len(resources))
    with col_m2:
        st.metric("Mean Confidence", f"{mean_conf:.0%}")
    with col_m3:
        st.metric("Agentic Fallback", "✅ Triggered" if fallback else "⬜ Not needed")

    # ── MATCHED RESOURCES ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header" style="margin-top:20px;">
      <span>🔍</span> MATCHED COMMUNITY RESOURCES
    </div>
    """, unsafe_allow_html=True)

    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 2, 2, 2])
    with f_col1:
        all_types = sorted(set(r["need_type"] for r in resources))
        type_opts = ["All Need Types"] + [
            f'{NEED_META.get(t,{}).get("icon","•")} {NEED_META.get(t,{}).get("label",t)}'
            for t in all_types
        ]
        sel_type_label = st.selectbox("Filter by Need Type", type_opts)
        sel_type = None
        if sel_type_label != "All Need Types":
            icon_part = sel_type_label.split(" ")[0]
            sel_type = next(
                (t for t in all_types if NEED_META.get(t, {}).get("icon", "") == icon_part), None
            )
    with f_col2:
        sel_source = st.selectbox("Filter by Source", ["All Sources", "Internal Corpus", "FindHelp / 211"])
    with f_col3:
        conf_min = st.slider("Min Confidence", 0.0, 1.0, 0.0, 0.05, format="%.0f%%")
    with f_col4:
        keyword = st.text_input("Search by keyword", placeholder="e.g. food, shelter...")

    filtered = resources
    if sel_type:
        filtered = [r for r in filtered if r["need_type"] == sel_type]
    if sel_source == "Internal Corpus":
        filtered = [r for r in filtered if r.get("source") == "internal_corpus"]
    elif sel_source == "FindHelp / 211":
        filtered = [r for r in filtered if r.get("source") == "findhelp_api"]
    filtered = [r for r in filtered if r.get("confidence", 0) >= conf_min]
    if keyword.strip():
        kw = keyword.strip().lower()
        filtered = [r for r in filtered
                    if kw in r.get("name","").lower()
                    or kw in r.get("address","").lower()
                    or kw in r.get("need_type","").lower()]

    if not filtered:
        st.markdown(
            '<div class="no-results">🔍 No resources match your filters. Try broadening your search.</div>',
            unsafe_allow_html=True
        )
    else:
        grouped: dict[str, list] = {}
        for r in filtered:
            grouped.setdefault(r["need_type"], []).append(r)

        for need_type, group in grouped.items():
            meta = NEED_META.get(need_type, {"icon": "•", "label": need_type, "color": "#1B5FA8"})
            st.markdown(
                f'<div class="resource-section-title" style="color:{meta["color"]};">'
                f'{meta["icon"]} {meta["label"]}'
                f'<span style="font-size:0.75rem;font-weight:400;color:#8A9AB0;margin-left:8px;">'
                f'({len(group)} resource{"s" if len(group)!=1 else ""})</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Use Streamlit columns + st.link_button to avoid HTML rendering issues
            cols = st.columns(3)
            for i, r in enumerate(group):
                with cols[i % 3]:
                    conf_pct = f'{r.get("confidence", 0):.0%}'
                    source_text = "FindHelp / 211" if r.get("source") == "findhelp_api" else "Internal Corpus"
                    phone_line = f'<div style="font-size:0.78rem;color:#64748B;margin-bottom:6px;">📞 {r["phone"]}</div>' if r.get("phone") else ""

                    st.markdown(
                        f'<div style="background:white;border-radius:14px;padding:18px 18px 12px;'
                        f'border-top:4px solid {meta["color"]};'
                        f'box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:4px;">'
                        f'<div style="display:flex;justify-content:space-between;'
                        f'align-items:flex-start;margin-bottom:10px;">'
                        f'<span style="font-weight:700;color:#0D3B7A;font-size:0.92rem;'
                        f'line-height:1.3;flex:1;margin-right:8px;">{r["name"]}</span>'
                        f'<span style="background:linear-gradient(135deg,#1B5FA8,#2176C7);'
                        f'color:white;border-radius:20px;padding:3px 10px;'
                        f'font-size:0.7rem;font-weight:700;white-space:nowrap;">✓ {conf_pct}</span>'
                        f'</div>'
                        f'<div style="font-size:0.78rem;color:#64748B;margin-bottom:6px;">'
                        f'📍 {r.get("address","N/A")}</div>'
                        f'{phone_line}'
                        f'<div style="font-size:0.63rem;color:#A0AEC0;text-transform:uppercase;'
                        f'letter-spacing:0.06em;margin-bottom:10px;">{source_text}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    st.link_button("🔗 Visit Website", r.get("website", "#"), use_container_width=True)

    # ── HUMAN-IN-THE-LOOP ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header-gold" style="margin-top:24px;">
      <span>✅</span> HUMAN-IN-THE-LOOP REVIEW
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white;padding:24px 32px;border-left:5px solid #F5A623;">
      <p style="font-weight:700;color:#0D3B7A;margin:0 0 8px 0;font-size:0.95rem;">
        ⚠️ Social Worker Review Required Before Referral
      </p>
      <p style="color:#5A6A80;font-size:0.85rem;margin:0;line-height:1.6;">
        All matched resources must be reviewed by a licensed social worker or patient navigator
        before any referral is sent to the patient. Verify availability, eligibility requirements,
        and current contact information before proceeding.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_approve, col_flag = st.columns(2)
    with col_approve:
        if st.button("✅  Approve & Send Referral to Patient"):
            st.success("✅ Referral approved. A navigator will follow up within 24 hours.")
    with col_flag:
        if st.button("🚩  Flag for Additional Review"):
            st.warning("🚩 Case flagged. A senior navigator will review before sending.")

    # ── PATIENT CARE NOTES ────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header" style="margin-top:24px;">
      <span>📝</span> ADD RESOURCES TO PATIENT CARE NOTES
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:white;padding:16px 32px 4px;border-bottom:1px solid #E8EFF8;">
      <p style="color:#5A6A80;font-size:0.85rem;margin:0;line-height:1.6;">
        Select the resources to include, add navigator comments, then generate a formatted
        note ready to paste into the patient record.
      </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div style='background:white;padding:20px 32px;'>", unsafe_allow_html=True)

        resource_options = [r["name"] for r in resources]
        selected_resources = st.multiselect(
            "Select resources to include in care notes:",
            options=resource_options,
            default=resource_options[:min(3, len(resource_options))],
        )

        nav_notes = st.text_area(
            "Navigator Comments / Additional Notes:", height=110,
            placeholder=(
                "e.g. Patient contacted Good Samaritan Health Center — "
                "appointment scheduled for next Tuesday. Will follow up on "
                "LIHEAP application in 5 business days..."
            )
        )

        priority = st.selectbox(
            "Care Note Priority:",
            ["🟢 Routine", "🟡 Elevated", "🔴 Urgent"],
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("📄  Generate Patient Care Note"):
        if not selected_resources:
            st.warning("⚠️ Please select at least one resource.")
        else:
            # Read patient info directly from session_state keys — always current
            pi_case_id       = st.session_state.get("pi_case_id", "") or "Not recorded"
            pi_patient_name  = st.session_state.get("pi_patient_name", "") or "Not recorded"
            pi_dob           = st.session_state.get("pi_dob", "") or "Not recorded"
            pi_zip           = st.session_state.get("pi_zip_code", "") or profile.get("zip_code") or "Not recorded"
            pi_ins_name      = st.session_state.get("pi_insurance_name", "") or "Not recorded"
            pi_ins_id        = st.session_state.get("pi_insurance_id", "") or "Not recorded"
            pi_navigator     = st.session_state.get("pi_navigator", "") or "Not recorded"
            pi_facility      = st.session_state.get("pi_facility", "") or "Not recorded"
            pi_visit_date    = st.session_state.get("pi_visit_date", "") or "Not recorded"

            now  = datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
            prio = priority.split(" ", 1)[1] if " " in priority else priority
            sel_r = [r for r in resources if r["name"] in selected_resources]

            # Build income string safely
            income_str = (
                f"${profile['income_monthly_usd']:,.0f}"
                if profile.get("income_monthly_usd") else "Not recorded"
            )

            lines = [
                "VARTIS CARE AI — PATIENT CARE NOTE",
                f"Generated : {now}",
                f"Priority  : {prio}",
                "=" * 60,
                "",
                "PATIENT INFORMATION",
                "-" * 40,
                f"  Case ID          : {pi_case_id}",
                f"  Patient Name     : {pi_patient_name}",
                f"  Date of Birth    : {pi_dob}",
                f"  ZIP Code         : {pi_zip}",
                f"  Insurance Name   : {pi_ins_name}",
                f"  Insurance ID     : {pi_ins_id}",
                f"  Navigator        : {pi_navigator}",
                f"  Facility         : {pi_facility}",
                f"  Visit Date       : {pi_visit_date}",
                "",
                "EXTRACTED ELIGIBILITY PROFILE",
                "-" * 40,
                f"  Age              : {profile.get('age') or 'Not recorded'}",
                f"  Gender           : {(profile.get('gender') or 'Not recorded').title()}",
                f"  Monthly Income   : {income_str}",
                f"  Insurance Status : {(profile.get('insurance_status') or 'unknown').title()}",
                f"  Household Size   : {profile.get('household_size') or 'Not recorded'}",
                f"  Identified Needs : {', '.join(profile.get('needs') or []) or 'None identified'}",
                "",
                "REFERRED COMMUNITY RESOURCES",
                "-" * 40,
            ]

            for i, r in enumerate(sel_r, 1):
                m = NEED_META.get(r["need_type"], {})
                lines += [
                    f"  {i}. {r['name']}",
                    f"     Category  : {m.get('label', r['need_type'])}",
                    f"     Address   : {r.get('address', 'N/A')}",
                    f"     Phone     : {r.get('phone') or 'N/A'}",
                    f"     Website   : {r.get('website', 'N/A')}",
                    f"     Confidence: {r.get('confidence', 0):.0%}",
                    "",
                ]

            if nav_notes.strip():
                lines += [
                    "NAVIGATOR COMMENTS",
                    "-" * 40,
                    f"  {nav_notes.strip()}",
                    "",
                ]

            lines += [
                "=" * 60,
                "Note generated by Vartis Care AI and reviewed by a licensed",
                "social worker prior to patient delivery.",
                "CSC 7644: Applied LLM Development — Chantel Walker, LSU",
            ]

            final_note = "\n".join(lines)
            st.success("✅ Care note generated successfully!")
            st.text_area(
                "Patient Care Note — copy and paste into patient record:",
                value=final_note, height=420
            )
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            st.download_button(
                label="⬇️  Download Care Note (.txt)",
                data=final_note,
                file_name=f"vartis_care_note_{ts}.txt",
                mime="text/plain",
            )


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vartis-footer">
  <div class="footer-left">Vartis Care AI &nbsp;·&nbsp; Resource Navigator</div>
  <div class="footer-right">
    CSC 7644: Applied LLM Development &nbsp;·&nbsp; Louisiana State University &nbsp;·&nbsp; Chantel Walker
  </div>
</div>
""", unsafe_allow_html=True)
  <div class="footer-left">Vartis Care AI &nbsp;·&nbsp; Resource Navigator</div>
  <div class="footer-right">
    CSC 7644: Applied LLM Development &nbsp;·&nbsp; Louisiana State University &nbsp;·&nbsp; Chantel Walker
  </div>
</div>
""", unsafe_allow_html=True)
