# Text Summarizer using LLM

This project is a Streamlit web application that allows users to upload text, PDF, or image files, and receive a summarized version of the text using a large language model (LLM). Users can also ask questions related to the uploaded text and get answers.

## Project Structure

text_summarizer/
│
├── app.py
├── requirements.txt
├── static/
│ └── custom.css
├── utils/
│ ├── init.py
│ ├── extract_text.py
│ ├── ocr.py
│ ├── summarize.py
│ ├── question_answer.py
│ └── rouge_score.py
└── README.md

## Setup

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd text_summarizer
2. Install the dependencies:
    pip install -r requirements.txt
3. Run the Streamlit app:
    streamlit run app.py


