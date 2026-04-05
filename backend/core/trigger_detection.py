import spacy
from triggers import EVENT_TRIGGERS

nlp = spacy.load("en_core_web_md")

IGNORE_LEMMAS = {"pass"}  # avoid false positives like "passed exam"


def detect_triggers(sentence):

    doc = nlp(sentence)
    sentence_lower = sentence.lower()

    detected = set()

    #  MULTI-WORD TRIGGERS
    for event, triggers in EVENT_TRIGGERS.items():
        for t in triggers:
            if " " in t and t in sentence_lower:
                detected.add((event, t))

    #  SINGLE-WORD TRIGGERS
    for token in doc:
        lemma = token.lemma_.lower()
        word = token.text.lower()

        if lemma in IGNORE_LEMMAS:
            continue

        for event, triggers in EVENT_TRIGGERS.items():
            for t in triggers:
                if " " not in t:
                    if lemma == t or word == t:
                        detected.add((event, t))

    return list(detected)