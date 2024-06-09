import streamlit as st
from transformers import pipeline

# Load pre-trained model and tokenizer
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

def answering(tex):
    question = st.text_input("Enter your question:")
    if st.button("Answer Question"):
        result = question_answerer(question=question, context=tex)
        st.subheader("Answer:")
        st.write(result["answer"])
