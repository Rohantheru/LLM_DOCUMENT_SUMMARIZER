import streamlit as st
import os
import PyPDF2
from transformers import pipeline
import pytesseract
from PIL import Image

# Load pre-trained model and tokenizer
checkpoint = "facebook/bart-large-cnn"
summarization_model = pipeline('summarization', model=checkpoint)
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

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

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdf_file as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to perform OCR on uploaded image
def perform_ocr(image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 3')
    return text

# Function to summarize text
def summarize_text(text):
    summary = summarization_model(text, min_length=256, max_length=512, do_sample=True)[0]['summary_text']
    return summary

# Function to answer questions
def answering(tex):
    question = st.text_input("Enter your question:")
    if st.button("Answer Question"):
        result = question_answerer(question=question, context=tex)
        st.subheader("Answer:")
        st.write(result["answer"])

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
        answering(text)
