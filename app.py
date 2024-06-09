import streamlit as st
from utils.extract_text import extract_text_from_pdf
from utils.ocr import perform_ocr
from utils.summarize import summarize_text
from utils.question_answer import answering
from utils.rouge_score import calculate_rouge
from PIL import Image

# Customizing Streamlit theme
st.markdown(
"""
<style>
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
</style>
""",
unsafe_allow_html=True
)

# Streamlit UI
st.title("Text Summarizer using LLM")

# Function to read text files from a folder and combine them into a single text
def read_files_from_folder(files):
    combined_text = ""
    for file in files:
        file_type = file.name.split('.')[-1].lower()
        if file_type == "txt":
            combined_text += file.getvalue().decode("utf-8")
            combined_text += "\n"  # Add a newline between files
        elif file_type == "pdf":
            combined_text += extract_text_from_pdf(file)
        elif file_type in ["jpg", "jpeg", "png"]:
            image = Image.open(file)
            combined_text += perform_ocr(image)
    return combined_text

# Radio button for selecting input format
input_format = st.sidebar.radio("Select input format:", ('Text', 'PDF', 'Image', 'Folder'))

# Main content area
if input_format == 'Text':  
    uploaded_file = st.file_uploader("Upload a text document (.txt)", type="txt")
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        st.subheader("Original Text:")
        st.write(text)

        if st.button("Summarize"):
            summary = summarize_text(text)
            st.subheader("Summary:")
            st.write(summary)
            rouge_score = calculate_rouge(text, summary)
            st.subheader("ROUGE Score:")
            st.json(rouge_score)
        answering(text)

elif input_format == 'PDF':
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.subheader("Original Text:")
        st.write(text)

        if st.button("Summarize"):
            summary = summarize_text(text)
            st.subheader("Summary:")
            st.write(summary)
            rouge_score = calculate_rouge(text, summary)
            st.subheader("ROUGE Score:")
            st.json(rouge_score)
        answering(text)

elif input_format == 'Image':
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        text = perform_ocr(image)
        st.subheader("Extracted Text from Image:")
        st.write(text)

        if st.button("Summarize"):
            summary = summarize_text(text)
            st.subheader("Summary:")
            st.write(summary)
            rouge_score = calculate_rouge(text, summary)
            st.subheader("ROUGE Score:")
            st.json(rouge_score)
        answering(text)

elif input_format == 'Folder':
    uploaded_files = st.file_uploader("Upload multiple text files", accept_multiple_files=True)
    if uploaded_files is not None:
        text = read_files_from_folder(uploaded_files)
        st.subheader("Combined Text from Folder:")
        st.write(text)

        if st.button("Summarize"):
            summary = summarize_text(text)
            st.subheader("Summary:")
            st.write(summary)
            rouge_score = calculate_rouge(text, summary)
            st.subheader("ROUGE Score:")
            st.json(rouge_score)
        answering(text)
