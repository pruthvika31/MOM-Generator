import google.generativeai as genai
import os
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import extract_text_image

# Configure GenAI model
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Sidebar
st.sidebar.title(":orange[Upload your MOM notes here]")
st.sidebar.subheader("Please upload your file in the correct format (pdf, docx, png, jpg, jpeg)")
user_file = st.sidebar.file_uploader("Upload your file", type=['pdf', 'png', 'jpg', 'jpeg', 'docx'])

# Extract text from uploaded file
user_text = None
if user_file is not None:
    if user_file.type == "application/pdf":
        user_text = text_extractor_pdf(user_file)

    elif user_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        user_text = text_extractor_docx(user_file)

    elif user_file.type in ["image/png", "image/jpg", "image/jpeg"]:
        user_text = extract_text_image(user_file)

if user_file:
    st.sidebar.success("✅ File uploaded successfully")

# Main title
st.title(":orange[Meeting MOM Notes]: :green[AI assisted MoM generator in a standardized format]")

tips = """
Tips to use this app:
* Upload your meeting in side bar (Image, PDF or DOCX)
* Click on **Generate MOM** and get the Standardized MoM
"""
st.write(tips)

# Generate button
if st.button('🚀 Generate MOM'):
    if not user_text:
        st.error("❌ No text extracted. Please upload a valid file.")
    else:
        with st.spinner("⏳ Processing your data..."):
            prompt = f"""
            Assume you are an expert in creating minutes of meeting. 
            User has provided notes of a meeting in text format. Using this data you need to create a standardized 
            minutes of meeting. The data provided by user is as follows: {user_text}

            Keep the format strictly as mentioned below:

            **Title:** Title of meeting  
            **Heading:** Meeting Agenda  
            **Subheading:** Name of the attendees (If not present, write NA)  
            **Subheading:** Date and place of meeting (If place not provided, keep it as Online)  

            **Body:** The body must follow this sequence:
            - KEY POINTS DISCUSSED  
            - HIGHLIGHT any decision that has been finalized  
            - Mention actionable items  
            - Any additional notes  
            - Any deadlines that have been discussed  
            - Next meeting date (if mentioned)  
            - 2-3 line summary  

            Use **bullet points** and highlight/format important keywords for clarity.  
            """

            # Call Gemini model
            response = model.generate_content(prompt)

            # Display response
            st.subheader("📜 Generated Minutes of Meeting")
            st.markdown(response.text)

            # Download button
            st.download_button(
                label="💾 Download MoM as TXT",
                data=response.text,
                file_name="generated_minutes_of_meeting.txt",
                mime="text/plain"
            )