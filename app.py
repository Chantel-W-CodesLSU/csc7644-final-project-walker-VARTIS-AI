"""
app.py

Streamlit web interface for Vartis Care AI.
CSC 7644: Applied LLM Development - Final Project
Author: Chantel Walker

This module provides a user-friendly web interface for healthcare
social workers to extract patient eligibility markers and find
verified community resources.
"""

import streamlit as st
import json
from extractor import extract_info


def display_resource(resource):
    """
    Display a single matched resource as a formatted card.

    Args:
        resource (dict): Resource dictionary containing name,
                        address, website, phone, source, and confidence.
    """
    # Display resource name and confidence score
    confidence_pct = int(resource["confidence"] * 100)
    st.markdown(f"### {resource['name']}")
    st.progress(resource["confidence"])
    st.markdown(f"**Match Confidence:** {confidence_pct}%")

    # Display address if available
    if "address" in resource:
        st.markdown(f"**Address:** {resource['address']}")

    # Display website if available
    if "website" in resource:
        st.markdown(f"**Website:** [{resource['website']}]({resource['website']})")

    # Display phone if available
    if "phone" in resource:
        st.markdown(f"**Phone:** {resource['phone']}")

    # Display source of the match
    source_label = "Internal Corpus" if resource["source"] == "internal_corpus" else "FindHelp API"
    st.markdown(f"**Source:** {source_label}")
    st.divider()


def main():
    """
    Main function to run the Vartis Care AI Streamlit web application.

    Renders the user interface, processes patient intake input,
    and displays matched community resources for advocate review.
    """
    # Page configuration
    st.set_page_config(
        page_title="Vartis Care AI",
        page_icon="🏥",
        layout="wide"
    )

    # Header
    st.title("🏥 Vartis Care AI")
    st.subheader("AI-Powered Patient Resource Matching for Healthcare Advocates")
    st.markdown("---")

    # Two column layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Patient Intake Note")
        st.markdown("Paste the patient intake note below and click Find Resources.")

        # Text input area for intake note
        intake_text = st.text_area(
            label="Patient Intake Note",
            height=350,
            placeholder="Paste patient intake note here...",
            label_visibility="collapsed"
        )

        # Run button
        run_button = st.button(
            "Find Resources",
            type="primary",
            use_container_width=True
        )

    with col2:
        st.markdown("### Matched Community Resources")

        if run_button and intake_text:
            # Show loading spinner while processing
            with st.spinner("Extracting eligibility markers and matching resources..."):
                result = extract_info(intake_text)

            # Display eligibility profile
            st.markdown("#### Patient Eligibility Profile")
            profile_col1, profile_col2 = st.columns(2)

            with profile_col1:
                st.metric("Income Level", result["income_level"])
                st.metric("Zip Code", result["zip_code"])

            with profile_col2:
                st.metric("Diagnosis Code", result["diagnosis_code"])
                st.metric("Insurance Status", result["insurance_status"])

            st.markdown("---")
            st.markdown("#### Recommended Resources")
            st.caption("All recommendations require advocate review before patient delivery.")

            # Display each matched resource
            for resource in result["matched_resources"]:
                display_resource(resource)

        elif run_button and not intake_text:
            st.warning("Please paste a patient intake note before clicking Find Resources.")

        else:
            st.info("Matched resources will appear here after you submit an intake note.")


if __name__ == "__main__":
    main()