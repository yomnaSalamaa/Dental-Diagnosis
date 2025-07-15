import streamlit as st
import os
from auth import login_ui, signup_ui
from model_inference import save_uploaded_image, run_teeth_model, run_disease_model, run_both_models
from db import init_db, log_image, get_user_logs
from report import generate_pdf_report


# Initialize DB on first run
init_db()

# Session state for user login
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = "login"

# Sidebar Navigation
st.sidebar.title("Navigation")
if st.session_state.username:
    st.sidebar.write(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.username = None
        st.session_state.page = "login"
else:
    st.sidebar.write("Not logged in")

# Main App Routing
if st.session_state.page == "login":
    st.title("🦷 Dental Diagnosis System")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        user = login_ui()
        if user:
            st.session_state.username = user
            st.session_state.page = "home"
            st.rerun()

    with tab2:
        signup_ui()

elif st.session_state.page == "home":
    st.title("Welcome to the Dental Diagnosis System")
    st.write("Choose an option below:")

    uploaded_file = st.file_uploader("Upload a dental X-ray image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        option = st.radio("Select analysis type:", ["Teeth Detection", "Disease Detection", "Both"])

        if st.button("Run Diagnosis"):
            image_path = save_uploaded_image(uploaded_file)
            st.session_state.image_path = image_path
            st.session_state.analysis_type = option

            if option == "Teeth Detection":
                output_path, missing_teeth = run_teeth_model(image_path)
                st.session_state.output_paths = {"teeth": output_path}
                st.session_state.missing_teeth = missing_teeth
                log_image(st.session_state.username, image_path, output_path, "teeth")
                st.image(output_path, caption=f"Teeth Detection Result (Missing: {missing_teeth})", use_container_width=True)


            elif option == "Disease Detection":
                output_path, detected_diseases = run_disease_model(image_path)
                st.session_state.output_paths = {"disease": output_path}
                st.session_state.detected_diseases = detected_diseases
                log_image(st.session_state.username, image_path, output_path, "disease")
                st.image(output_path, caption="Disease Detection Result", use_container_width=True)


            else:
                (teeth_out, missing_teeth), (disease_out, detected_diseases) = run_both_models(image_path)
                st.session_state.output_paths = {"teeth": teeth_out, "disease": disease_out}
                st.session_state.missing_teeth = missing_teeth
                st.session_state.detected_diseases = detected_diseases
                log_image(st.session_state.username, image_path, teeth_out, "teeth")
                log_image(st.session_state.username, image_path, disease_out, "disease")
                st.image(teeth_out, caption="Teeth Detection Result", use_container_width=True)
                st.image(disease_out, caption="Disease Detection Result", use_container_width=True)


    if "analysis_type" in st.session_state and "output_paths" in st.session_state:
        if st.button("🧾 Generate Report"):
            analysis_type = st.session_state.analysis_type
            image_path = st.session_state.image_path
            username = st.session_state.username

            if analysis_type == "Teeth Detection":
                pdf_path = generate_pdf_report(
                    username=username,
                    input_image=image_path,
                    output_image=st.session_state.output_paths["teeth"],
                    report_type="teeth",
                    missing_teeth=st.session_state.get("missing_teeth", None)
                )
                st.success("Teeth Detection Report generated!")

            elif analysis_type == "Disease Detection":
                pdf_path = generate_pdf_report(
                    username=username,
                    input_image=image_path,
                    output_image=st.session_state.output_paths["disease"],
                    report_type="disease",
                    missing_teeth=None,
                    detected_diseases=st.session_state.get("detected_diseases", [])
                )
                st.success("Disease Detection Report generated!")

            else:  # Both
                teeth_out = st.session_state.output_paths["teeth"]
                disease_out = st.session_state.output_paths["disease"]
                missing_teeth = st.session_state.missing_teeth
                detected_diseases = st.session_state.detected_diseases

                pdf_path = generate_pdf_report(
                    username=username,
                    input_image=image_path,
                    output_image=[teeth_out, disease_out],
                    report_type="both",
                    missing_teeth=missing_teeth,
                    detected_diseases=detected_diseases
                )

                st.image(teeth_out, caption="Teeth Detection Result", use_container_width=True)
                st.image(disease_out, caption="Disease Detection Result", use_container_width=True)

                if detected_diseases:
                    st.subheader("Detected Diseases:")
                    for disease in set(detected_diseases):
                        st.markdown(f"- {disease}")

                st.success("Combined Report generated!")

            st.session_state.generated_pdf = pdf_path

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )


    # 🧾 Show user history
    with st.expander("📜 View My Diagnosis History"):
        logs = get_user_logs(st.session_state.username)
        if logs:
            for input_img, output_img, model in logs:
                st.markdown(f"Model: {model}")
                st.image(output_img, caption=f"Result from: {os.path.basename(output_img)}", use_container_width=True)
                st.markdown("---")
        else:
            st.info("No diagnosis history yet.")