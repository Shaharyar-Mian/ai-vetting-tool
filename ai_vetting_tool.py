import streamlit as st
from fpdf import FPDF  # For PDF export; install with pip install fpdf

# Define the checklist questions
checklist = {
    "Usage Rights and Data Retention Terms": [
        "Does the tool clearly outline user rights, such as data access, deletion, and portability?",
        "Are there explicit terms on data retention periods?",
        "Does it specify opt-out options for data collection or processing?",
        "Are there clauses on data sharing with third parties?",
        "Is there a mechanism for users to request data erasure or export?"
    ],
    "Model Training Sources and Ownership Transparency": [
        "Does the tool disclose the sources of training data?",
        "Is there transparency on data curation methods?",
        "Are model ownership and intellectual property rights clearly stated?",
        "Does it provide details on model updates and versioning?",
        "Are there audits or reports on training data quality?"
    ],
    "Server Location and Data Handling": [
        "Is the server location disclosed and compliant with laws?",
        "Does the tool use encryption for data in transit and at rest?",
        "Are there guarantees on data isolation?",
        "Is there information on backup and disaster recovery?",
        "Does it adhere to standards like SOC 2 or ISO 27001?"
    ],
    "Legal and Compliance Review for Client-Facing Work": [
        "Has the tool undergone legal review for compliance?",
        "Does it include indemnification clauses?",
        "Are there certifications for industry standards?",
        "Does it restrict use in regulated industries?",
        "Is there a process for reporting compliance issues?"
    ],
    "Risk Level for Uploading Confidential Materials": [
        "Does the tool state it does not retain confidential data?",
        "Are there options for local processing?",
        "What is the risk of data leakage?",
        "Does it offer watermarking or access controls?",
        "Is there a policy on handling data breaches?"
    ]
}

# Function to calculate risk score
def calculate_risk(responses):
    no_unclear_count = sum(1 for resp in responses.values() if resp in ["No", "Unclear"])
    if no_unclear_count < 3:
        return "Low"
    elif no_unclear_count <= 5:
        return "Medium"
    else:
        return "High"

# Function to generate PDF report
def generate_pdf(responses, notes, risk):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Tool Vetting Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Overall Risk Level: {risk}", ln=True)
    pdf.ln(10)
    for category, questions in checklist.items():
        pdf.cell(200, 10, txt=category, ln=True)
        for i, q in enumerate(questions):
            resp = responses.get(f"{category}_{i}", "N/A")
            note = notes.get(f"{category}_{i}", "")
            pdf.cell(200, 10, txt=f"Q: {q}", ln=True)
            pdf.cell(200, 10, txt=f"Response: {resp} | Notes: {note}", ln=True)
        pdf.ln(5)
    return pdf

# Streamlit app
st.title("AI Tool Vetting Checklist Tool")
st.write("Answer the questions below for the AI tool you're evaluating. This will generate a risk assessment.")

responses = {}
notes = {}

for category, questions in checklist.items():
    st.header(category)
    for i, q in enumerate(questions):
        key = f"{category}_{i}"
        responses[key] = st.radio(q, ["Yes", "No", "Unclear"], key=f"resp_{key}")
        notes[key] = st.text_area(f"Notes/Evidence for Q{i+1}", key=f"note_{key}")

# Calculate and display risk
if st.button("Calculate Risk"):
    risk = calculate_risk(responses)
    st.success(f"Overall Risk Level: {risk}")
    st.write("Low: <3 'No' or 'Unclear' responses. Medium: 3-5. High: >5.")

# Export report
if st.button("Generate Report"):
    risk = calculate_risk(responses)
    pdf = generate_pdf(responses, notes, risk)
    pdf_output = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="Download PDF Report",
        data=pdf_output,
        file_name="ai_vetting_report.pdf",
        mime="application/pdf"
    )
