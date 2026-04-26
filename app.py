"""
app.py

Streamlit web interface for Vartis Care AI.
CSC 7644: Applied LLM Development - Final Project
Author: Chantel Walker

This module provides a user-friendly web interface for healthcare
social workers to extract patient eligibility markers and find
verified community resources organized by patient need type.
"""

import streamlit as st
from datetime import date
from extractor import extract_info

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vartis Care AI",
    page_icon="🌿",
    layout="wide"
)

# ── GLOBAL STYLES ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cormorant+Garamond:wght@400;600&family=DM+Sans:wght@400;500;600&display=swap');

  #MainMenu, footer, header { visibility: hidden; }
  .stApp { background-color: #fafaf7; }

  .vartis-header {
    background: linear-gradient(135deg, #1a4d2e 0%, #1e5c35 60%, #143d26 100%);
    padding: 20px 32px 16px;
    border-bottom: 3px solid #e6a91a;
    border-radius: 12px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
  }
  .vartis-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(230,169,26,0.08);
  }
  .header-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }
  .logo-cursive {
    font-family: 'Great Vibes', cursive;
    font-size: 52px;
    color: #f5c842;
    line-height: 1.0;
    text-shadow: 0 2px 12px rgba(201,146,10,0.5);
  }
  .logo-sub {
    font-family: 'Cormorant Garamond', serif;
    font-size: 11px;
    color: rgba(245,200,66,0.85);
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: -6px;
    margin-left: 4px;
  }
  .header-tagline {
    font-family: 'Cormorant Garamond', serif;
    font-size: 13px;
    color: rgba(255,255,255,0.55);
    font-style: italic;
    margin-top: 6px;
  }
  .header-meta { text-align: right; }
  .badge-name {
    display: inline-block;
    background: rgba(201,146,10,0.25);
    border: 1px solid rgba(230,169,26,0.5);
    color: #f5c842;
    font-size: 14px;
    font-weight: 500;
    padding: 5px 16px;
    border-radius: 20px;
    font-family: 'Cormorant Garamond', serif;
    letter-spacing: 0.5px;
  }
  .badge-course {
    display: block;
    color: rgba(255,255,255,0.55);
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 5px;
  }

  .patient-panel {
    background: linear-gradient(135deg, #1a4d2e 0%, #1e5c35 100%);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
    border: 1px solid #2d7a4f;
  }
  .patient-panel-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 13px;
    font-weight: 600;
    color: #f5c842;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
    border-bottom: 1px solid rgba(245,200,66,0.25);
    padding-bottom: 8px;
  }
  .profile-summary {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(245,200,66,0.2);
    border-radius: 8px;
    padding: 10px 16px;
    margin-top: 14px;
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    font-size: 13px;
    color: rgba(255,255,255,0.85);
  }
  .prof-key {
    font-weight: 700;
    color: #f5c842;
    margin-right: 5px;
  }
  .prof-sep { color: rgba(245,200,66,0.3); }

  .search-panel {
    background: white;
    border: 1px solid #e0ede5;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(26,77,46,0.06);
  }
  .search-panel-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 13px;
    font-weight: 600;
    color: #1a4d2e;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
  }

  .notes-panel {
    background: white;
    border: 1.5px solid #e0ede5;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 20px;
    box-shadow: 0 2px 12px rgba(26,77,46,0.06);
  }
  .notes-panel-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 13px;
    font-weight: 600;
    color: #1a4d2e;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
    border-bottom: 1px solid #e0ede5;
    padding-bottom: 8px;
  }

  .resource-card {
    background: white;
    border-radius: 12px;
    border: 1.5px solid #e0ede5;
    padding: 16px 18px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
  }
  .card-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
  }
  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
  }
  .need-badge {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 20px;
  }
  .match-pct {
    font-size: 12px;
    font-weight: 700;
    color: #2d7a4f;
    background: #e8f5ee;
    border-radius: 8px;
    padding: 2px 10px;
  }
  .card-name {
    font-size: 15px;
    font-weight: 600;
    color: #1a2e1f;
    margin-bottom: 5px;
  }
  .card-address {
    font-size: 12px;
    color: #7a9882;
    margin-bottom: 8px;
  }
  .card-link {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    color: #2d7a4f;
    text-decoration: none;
    padding: 4px 12px;
    border: 1px solid #c0dcc8;
    border-radius: 6px;
    margin-right: 8px;
  }
  .card-phone { font-size: 11px; color: #7a9882; font-weight: 500; }
  .source-label { font-size: 10px; color: #7a9882; margin-top: 8px; }
  .source-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #e6a91a;
    margin-right: 5px;
    vertical-align: middle;
  }

  .results-count {
    font-size: 13px;
    color: #7a9882;
    font-weight: 500;
    margin-bottom: 14px;
  }
  .results-count strong { color: #1a4d2e; font-weight: 700; }

  .no-results {
    text-align: center;
    padding: 40px 20px;
    color: #7a9882;
    font-size: 14px;
    background: white;
    border-radius: 12px;
    border: 1.5px dashed #c8e0d0;
  }

  .stSelectbox label, .stTextInput label, .stDateInput label {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #7a9882 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
  }

  .upload-success {
    background: #e8f5ee;
    border: 1.5px solid #2d7a4f;
    border-radius: 8px;
    padding: 14px 18px;
    color: #1a4d2e;
    font-size: 14px;
    font-weight: 500;
    margin-top: 12px;
  }
</style>
""", unsafe_allow_html=True)

# ── NEED TYPE CONFIG ──────────────────────────────────────────────────────────
NEED_TYPES = {
    "MEDICATION": {
        "icon": "💊", "label": "Medication Assistance",
        "bg": "#eeebff", "text": "#5a4fb0",
        "bar": "linear-gradient(90deg,#6b5bb8,#9b8de0)"
    },
    "MEDICAL": {
        "icon": "🏥", "label": "Medical Care",
        "bg": "#e8f5ee", "text": "#1a4d2e",
        "bar": "linear-gradient(90deg,#2d7a4f,#4caf78)"
    },
    "FOOD": {
        "icon": "🍎", "label": "Food Assistance",
        "bg": "#fef0e6", "text": "#c05c1a",
        "bar": "linear-gradient(90deg,#e07b39,#f5a55e)"
    },
    "UTILITY": {
        "icon": "⚡", "label": "Utility Assistance",
        "bg": "#e6f1fb", "text": "#185fa5",
        "bar": "linear-gradient(90deg,#2a7ab8,#5baade)"
    },
    "RENT": {
        "icon": "🏠", "label": "Rent Assistance",
        "bg": "#fef9e7", "text": "#8a6200",
        "bar": "linear-gradient(90deg,#c9920a,#f5c842)"
    },
    "HOUSING": {
        "icon": "🏘️", "label": "Housing & Shelter",
        "bg": "#fdeaea", "text": "#9b2828",
        "bar": "linear-gradient(90deg,#c94040,#e07070)"
    },
    "EMPLOYMENT": {
        "icon": "💼", "label": "Employment Services",
        "bg": "#e1f5f2", "text": "#155a52",
        "bar": "linear-gradient(90deg,#1a7a6e,#3ab8a8)"
    },
    "CLOTHING": {
        "icon": "👗", "label": "Clothing Assistance",
        "bg": "#fce8f3", "text": "#9b3070",
        "bar": "linear-gradient(90deg,#c45090,#e085b8)"
    },
}

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vartis-header">
  <div class="header-inner">
    <div>
      <div class="logo-cursive">Vartis</div>
      <div class="logo-sub">Care AI &mdash; Resource Navigator</div>
      <div class="header-tagline">Connecting patients to verified community resources</div>
    </div>
    <div class="header-meta">
      <span class="badge-name">Chantel Walker</span>
      <span class="badge-course">CSC 7644 &bull; Applied LLM Development</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── PATIENT PROFILE INPUT PANEL ───────────────────────────────────────────────
st.markdown(
    '<div class="patient-panel">'
    '<div class="patient-panel-title">👤 Patient Profile</div>',
    unsafe_allow_html=True
)

# Row 1: Name, DOB, ZIP, Insurance
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1:
    patient_name = st.text_input(
        "Patient Name (De-identified)",
        placeholder="e.g. Maria G."
    )

with row1_col2:
    patient_dob = st.date_input(
        "Date of Birth",
        value=None,
        min_value=date(1920, 1, 1),
        max_value=date.today()
    )

with row1_col3:
    zip_code = st.text_input("ZIP Code", placeholder="e.g. 30301")

with row1_col4:
    insurance_status = st.selectbox(
        "Insurance Status",
        [
            "-- Select --",
            "Uninsured",
            "Medicaid",
            "Medicare",
            "Medicaid & Medicare (Dual)",
            "Marketplace / ACA Plan",
            "Employer-Sponsored",
            "CHIP",
            "VA / TRICARE",
            "Underinsured"
        ]
    )

# Row 2: Income Level, Household Size, Urgency
row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

with row2_col1:
    income_level = st.selectbox(
        "Income Level",
        [
            "-- Select --",
            "Below 100% FPL",
            "Below 133% FPL",
            "Below 138% FPL",
            "Below 150% FPL",
            "Below 200% FPL",
            "Below 250% FPL",
            "Below 300% FPL",
            "Above 300% FPL"
        ]
    )

with row2_col2:
    household_size = st.selectbox(
        "Household Size",
        ["-- Select --", "1", "2", "3", "4", "5", "6", "7", "8+"]
    )

with row2_col3:
    urgency = st.selectbox(
        "Urgency Level",
        ["-- Select --", "🔴 High", "🟡 Medium", "🟢 Low"]
    )

with row2_col4:
    case_number = st.text_input(
        "Case Reference Number",
        placeholder="e.g. ATL-2026-0042"
    )

# Profile summary bar
profile_complete = (
    patient_name.strip() != "" and
    patient_dob is not None and
    zip_code.strip() != "" and
    insurance_status != "-- Select --" and
    income_level != "-- Select --"
)

if profile_complete:
    dob_str = patient_dob.strftime("%m/%d/%Y") if patient_dob else "N/A"
    st.markdown(f"""
    <div class="profile-summary">
      <span><span class="prof-key">Patient:</span>{patient_name}</span>
      <span class="prof-sep">|</span>
      <span><span class="prof-key">DOB:</span>{dob_str}</span>
      <span class="prof-sep">|</span>
      <span><span class="prof-key">ZIP:</span>{zip_code.strip()}</span>
      <span class="prof-sep">|</span>
      <span><span class="prof-key">Income:</span>{income_level}</span>
      <span class="prof-sep">|</span>
      <span><span class="prof-key">Insurance:</span>{insurance_status}</span>
      <span class="prof-sep">|</span>
      <span><span class="prof-key">Urgency:</span>{urgency}</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.06);border:1px dashed rgba(245,200,66,0.25);
    border-radius:8px;padding:10px 16px;margin-top:14px;font-size:12px;
    color:rgba(255,255,255,0.4);font-style:italic;">
      Complete patient profile fields above to generate a summary.
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── SEARCH / FILTER PANEL ─────────────────────────────────────────────────────
st.markdown(
    '<div class="search-panel">'
    '<div class="search-panel-title">🔍 Filter Resources</div>',
    unsafe_allow_html=True
)

sc1, sc2, sc3, sc4 = st.columns(4)

with sc1:
    need_filter = st.selectbox(
        "Need Type",
        ["All Categories", "MEDICATION", "MEDICAL", "FOOD",
         "UTILITY", "RENT", "HOUSING", "EMPLOYMENT", "CLOTHING"]
    )

with sc2:
    source_filter = st.selectbox(
        "Source",
        ["All Sources", "internal_corpus", "findhelp_api"]
    )

with sc3:
    conf_options = {
        "Any Match": 0.0,
        "90%+": 0.90,
        "92%+": 0.92,
        "94%+": 0.94,
        "96%+": 0.96
    }
    conf_label = st.selectbox("Min. Match %", list(conf_options.keys()))
    min_conf = conf_options[conf_label]

with sc4:
    phone_filter = st.selectbox(
        "Has Phone",
        ["Any", "Has Phone", "No Phone Listed"]
    )

keyword = st.text_input(
    "Keyword Search",
    placeholder="e.g. shelter, prescription, food bank, job training..."
)

st.markdown('</div>', unsafe_allow_html=True)

# ── LOAD + FILTER RESOURCES ───────────────────────────────────────────────────
data = extract_info("")
resources = data["matched_resources"]

if need_filter != "All Categories":
    resources = [r for r in resources if r["need_type"] == need_filter]

if source_filter != "All Sources":
    resources = [r for r in resources if r["source"] == source_filter]

resources = [r for r in resources if r["confidence"] >= min_conf]

if phone_filter == "Has Phone":
    resources = [r for r in resources if r.get("phone")]
elif phone_filter == "No Phone Listed":
    resources = [r for r in resources if not r.get("phone")]

if keyword.strip():
    kw = keyword.strip().lower()
    resources = [
        r for r in resources
        if kw in r["name"].lower() or kw in r.get("address", "").lower()
    ]

resources = sorted(resources, key=lambda r: r["confidence"], reverse=True)

# ── RESULTS ───────────────────────────────────────────────────────────────────
count = len(resources)
st.markdown(
    f'<div class="results-count"><strong>{count}</strong> '
    f'resource{"s" if count != 1 else ""} matched</div>',
    unsafe_allow_html=True
)

if not resources:
    st.markdown("""
    <div class="no-results">
      No resources matched your criteria.<br>
      <span style="font-size:12px;">Try adjusting the filters above.</span>
    </div>
    """, unsafe_allow_html=True)
else:
    left_col, right_col = st.columns(2)

    for i, resource in enumerate(resources):
        need_type = resource.get("need_type", "GENERAL")
        info = NEED_TYPES.get(need_type, {
            "icon": "📋", "label": need_type,
            "bg": "#f5f5f5", "text": "#444",
            "bar": "linear-gradient(90deg,#888,#aaa)"
        })

        confidence_pct = int(resource["confidence"] * 100)
        phone_html = (
            f'<span class="card-phone">📞 {resource["phone"]}</span>'
            if resource.get("phone") else ""
        )
        source_label = (
            "FindHelp API"
            if resource["source"] == "findhelp_api"
            else "Internal Corpus"
        )

        card_html = f"""
        <div class="resource-card">
          <div class="card-accent" style="background:{info['bar']};"></div>
          <div class="card-top">
            <span class="need-badge"
              style="background:{info['bg']};color:{info['text']};">
              {info['icon']} {need_type}
            </span>
            <span class="match-pct">{confidence_pct}% Match</span>
          </div>
          <div class="card-name">{resource['name']}</div>
          <div class="card-address">📍 {resource['address']}</div>
          <div>
            <a class="card-link" href="{resource['website']}"
              target="_blank">Visit Website</a>
            {phone_html}
          </div>
          <div class="source-label">
            <span class="source-dot"></span>{source_label}
          </div>
        </div>
        """

        if i % 2 == 0:
            with left_col:
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            with right_col:
                st.markdown(card_html, unsafe_allow_html=True)

# ── ADVOCATE NOTES AND CHART UPLOAD ──────────────────────────────────────────
st.markdown(
    '<div class="notes-panel">'
    '<div class="notes-panel-title">📋 Advocate Notes & Patient Chart Upload</div>',
    unsafe_allow_html=True
)

st.caption(
    "Document approved referrals and upload to patient chart. "
    "All referrals must be reviewed and approved before patient delivery."
)

notes_col1, notes_col2 = st.columns([2, 1])

with notes_col1:
    advocate_notes = st.text_area(
        "Advocate Notes",
        height=150,
        placeholder=(
            "Document which resources were approved and referred to the "
            "patient. Include any follow-up actions, patient preferences, "
            "or barriers identified during intake..."
        ),
        label_visibility="visible"
    )

with notes_col2:
    st.markdown("**Referral Status**")
    approved_referral = st.checkbox("Resources reviewed by advocate")
    patient_notified = st.checkbox("Patient notified of referrals")
    chart_ready = st.checkbox("Ready to upload to patient chart")

    st.markdown("")

    if st.button(
        "📤 Upload to Patient Chart",
        type="primary",
        use_container_width=True,
        disabled=not (approved_referral and patient_notified and chart_ready)
    ):
        if profile_complete and advocate_notes.strip():
            st.markdown(
                f"""
                <div class="upload-success">
                  ✅ <strong>Successfully uploaded to patient chart</strong><br>
                  <span style="font-size:12px;">
                  Patient: {patient_name} &nbsp;|&nbsp;
                  Case: {case_number if case_number else "N/A"} &nbsp;|&nbsp;
                  Date: {date.today().strftime("%m/%d/%Y")}
                  </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning(
                "Please complete the patient profile and add advocate "
                "notes before uploading to chart."
            )

st.markdown('</div>', unsafe_allow_html=True)