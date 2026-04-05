import spacy
import re

nlp = spacy.load("en_core_web_md")


def segment_sentences(text):

    paragraphs = re.split(r'\n\s*\n', text)
    sentences = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        doc = nlp(para)

        for sent in doc.sents:
            cleaned = sent.text.strip()

            if cleaned and len(cleaned.split()) >= 3:
                sentences.append(cleaned)

    return sentences

if __name__ == "__main__":
    test_text = """
 Dr. B.R. Ambedkar (1891–1956) was an Indian jurist, economist, and social reformer. He chaired the committee that drafted the Constitution of India. In 1952, he was elected to the Rajya Sabha. He passed away in Delhi on Dec. 6, 1956.
    """

    result = segment_sentences(test_text)

    for i, sentence in enumerate(result, 1):
        print(f"{i}. {sentence}")