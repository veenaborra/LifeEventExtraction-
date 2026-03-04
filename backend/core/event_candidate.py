import spacy

nlp = spacy.load("en_core_web_md")

BOUNDARY_WORDS = {"and", "but", "then", "later"}
BOUNDARY_PUNCT = {",", ";","."}


def extract_event_candidates(sentence, triggers):
    """
    Extract clause spans around trigger words.
    """

    doc = nlp(sentence)
    tokens = list(doc)

    event_candidates = []

    for event_type, trigger_word in triggers:

        # find trigger token index
        trigger_index = None
        for i, token in enumerate(tokens):
            if token.text.lower() == trigger_word.lower():
                trigger_index = i
                break

        if trigger_index is None:
            continue

        # -------- find left boundary --------
        left = trigger_index
        while left > 0:
            if tokens[left].text in BOUNDARY_PUNCT:
                break
            if tokens[left].text.lower() in BOUNDARY_WORDS:
                break
            left -= 1

        # -------- find right boundary --------
        right = trigger_index
        while right < len(tokens) - 1:
            if tokens[right].text in BOUNDARY_PUNCT:
                break
            if tokens[right].text.lower() in BOUNDARY_WORDS:
                break
            right += 1

        span_tokens = tokens[left:right+1]

        # remove boundary tokens at start
        while span_tokens and (
            span_tokens[0].text.lower() in BOUNDARY_WORDS
            or span_tokens[0].text in BOUNDARY_PUNCT
        ):
            span_tokens = span_tokens[1:]

        # remove boundary tokens at end
        while span_tokens and (
            span_tokens[-1].text.lower() in BOUNDARY_WORDS
            or span_tokens[-1].text in BOUNDARY_PUNCT
        ):
            span_tokens = span_tokens[:-1]

        span_text = " ".join([t.text for t in span_tokens]).strip()

        event_candidates.append({
            "event_type": event_type,
            "trigger": trigger_word,
            "span": span_text,
            "sentence": sentence
        })

    return event_candidates


if __name__ == "__main__":

    sentence = "He was born in 1937, married in 1960, and died in 2015."

    triggers = [
        ("Birth", "born"),
        ("Marriage", "married"),
        ("Death", "died")
    ]

    candidates = extract_event_candidates(sentence, triggers)

    for c in candidates:
        print(c)