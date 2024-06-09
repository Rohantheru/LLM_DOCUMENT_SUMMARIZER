from rouge_score import rouge_scorer

def calculate_rouge(reference_text, summarized_text):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_text, summarized_text)

    formatted_scores = {}
    for key, value in scores.items():
        formatted_scores[key] = {
            "precision": value.precision,
            "recall": value.recall,
            "f1_score": value.fmeasure
        }

    return formatted_scores
