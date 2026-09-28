import os
from pathlib import Path

import requests
import streamlit as st

from dotenv import load_dotenv

from backend.document_utils.formatters import (
    as_txt,
    as_docx,
    as_pdf
)


ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / ".env")

API_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="centered"
)


# Logo

logo = ROOT / "assets" / "logo.png"

if logo.exists():
    st.image(str(logo), width=150)


# Main heading

st.title("⚖️ LegalEase AI")

st.caption(
    "AI-Powered Legal Document Generator"
)

st.write(
    "Create, edit, and download legal document drafts."
)


# Document form

with st.form("document_form"):

    st.subheader("Document Details")

    document_type = st.selectbox(
        "Select Document Type",
        [
            "Non-Disclosure Agreement",
            "Service Agreement",
            "Rental Agreement",
            "Employment Agreement",
            "Partnership Agreement",
            "Loan Agreement",
            "Consulting Agreement",
            "Other"
        ]
    )

    language = st.selectbox(
        "Select Language",
        ["English", "Tamil", "Hindi"]
    )

    party_one = st.text_input(
        "First Party / Organization"
    )

    party_two = st.text_input(
        "Second Party / Organization"
    )

    effective_date = st.text_input(
        "Effective Date (Optional)"
    )

    terms = st.text_area(
        "Terms and Conditions",
        height=200,
        placeholder=(
            "Enter the purpose, responsibilities, "
            "payment terms, duration, and other conditions."
        )
    )

    submitted = st.form_submit_button(
        "Generate Legal Document",
        type="primary"
    )


# Generate document

if submitted:

    if (
        not party_one.strip()
        or not party_two.strip()
        or not terms.strip()
    ):

        st.error(
            "Please fill in both parties "
            "and the terms and conditions."
        )

    else:

        payload = {
            "document_type": document_type,
            "language": language,
            "details": (
                f"First Party: {party_one.strip()}\n"
                f"Second Party: {party_two.strip()}\n"
                f"Effective Date: "
                f"{effective_date.strip() or 'Not specified'}\n"
                f"Terms and Conditions: {terms.strip()}"
            )
        }

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/api/generate",
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                st.session_state["draft"] = (
                    result["generated_document"]
                )

                st.success(
                    "Document generated successfully!"
                )

            except requests.RequestException as exc:

                st.error(
                    f"Backend connection failed: {exc}"
                )

            except (KeyError, ValueError) as exc:

                st.error(
                    f"Unexpected backend response: {exc}"
                )


# Preview and downloads

if "draft" in st.session_state:

    st.divider()

    st.subheader("Generated Document")

    edited_content = st.text_area(
        "Review and Edit Your Document",
        value=st.session_state["draft"],
        height=450,
        key="edited_document"
    )

    st.download_button(
        label="Download TXT",
        data=as_txt(edited_content),
        file_name="legalease_document.txt",
        mime="text/plain"
    )

    st.download_button(
        label="Download DOCX",
        data=as_docx(edited_content),
        file_name="legalease_document.docx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )
    )

    st.download_button(
        label="Download PDF",
        data=as_pdf(edited_content),
        file_name="legalease_document.pdf",
        mime="application/pdf"
    )


st.divider()

st.caption(
    "Disclaimer: LegalEase AI creates document drafts "
    "for informational purposes. Consult a qualified "
    "legal professional before signing."
)

