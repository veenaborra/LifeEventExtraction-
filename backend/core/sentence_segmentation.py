import spacy

nlp = spacy.load("en_core_web_md")


def segment_sentences(text):
    """
    Splits input text into sentences using spaCy.
    Returns a list of sentence strings.
    """
    doc = nlp(text)

    sentences = []

    for sent in doc.sents:
        cleaned_sentence = sent.text.strip()
        if cleaned_sentence:
            sentences.append(cleaned_sentence)

    return sentences



if __name__ == "__main__":
    test_text = """
 Dr. B.R. Ambedkar (1891–1956) was an Indian jurist, economist, and social reformer. He chaired the committee that drafted the Constitution of India. In 1952, he was elected to the Rajya Sabha. He passed away in Delhi on Dec. 6, 1956.
    """

    result = segment_sentences(test_text)

    for i, sentence in enumerate(result, 1):
        print(f"{i}. {sentence}")