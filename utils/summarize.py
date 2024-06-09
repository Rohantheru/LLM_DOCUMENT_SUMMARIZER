from transformers import pipeline

# Load pre-trained model and tokenizer
checkpoint = "facebook/bart-large-cnn"
summarization_model = pipeline('summarization', model=checkpoint)

def summarize_text(text):
    summary = summarization_model(text, min_length=256, max_length=512, do_sample=True)[0]['summary_text']
    return summary
