import uuid
from fpdf import FPDF
import datetime
import os

def generate_pdf_report(username, input_image, report_type, output_image=None, output_image_teeth=None, output_image_disease=None, missing_teeth=None, detected_diseases=None):

    output_dir = "report_output/"
    os.makedirs(output_dir, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt=f"Dental {report_type.title()} Report", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Username: {username}", ln=True, align="L")

    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    pdf.ln(0)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Input Image:", ln=True)
    pdf.image(input_image, x=10, y=50, w=100)

    if report_type == "teeth" and output_image:

        pdf.ln(80)
        pdf.cell(200, 10, txt="Teeth Detection Result:", ln=True)
        pdf.image(output_image, x=10, y=140, w=100)
        pdf_path = os.path.join(output_dir, f"{username}_teeth_report.pdf")

        if missing_teeth is not None:
            pdf.ln(80)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Number of missing teeth: {missing_teeth}", ln=True)
        pdf_path = os.path.join(output_dir, f"{username}_teeth_report.pdf")

    elif report_type == "disease" and output_image:
        pdf.ln(80)
        pdf.cell(200, 10, txt="Disease Detection Result:", ln=True)
        pdf.image(output_image, x=10, y=140, w=100)
        if detected_diseases:
            pdf.ln(80)
            pdf.set_font("Arial", size=12)
            unique_diseases = list(set(detected_diseases))
            diseases_text = ", ".join(unique_diseases)
            pdf.multi_cell(180, 10, txt=f"Diseases Detected: {diseases_text}")

        pdf_path = os.path.join(output_dir, f"{username}_disease_report.pdf")


    elif report_type == "both":
        pdf.ln(80)
        pdf.cell(200, 10, txt="Teeth Detection Result:", ln=True)
        pdf.image(output_image[0], x=10, y=140,w=100)
        pdf.ln(60)
        pdf.cell(200, 10, txt=f"Missing Teeth: {missing_teeth}", ln=True)
        pdf.ln(70)
        pdf.cell(200, 10, txt="Detected Diseases:", ln=True)
        pdf.ln(80)
        for disease in detected_diseases:
            pdf.cell(200, 10, txt=f"- {disease}", ln=True)
        pdf.image(output_image[1], x=10, y=30,w=120)

    # Save report
    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", f"{username}_{uuid.uuid4().hex}.pdf")
    pdf.output(report_path)
    
    return report_path
