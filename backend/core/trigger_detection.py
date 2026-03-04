import spacy
from triggers import EVENT_TRIGGERS

nlp = spacy.load("en_core_web_md")


def detect_triggers(sentence):
    """
    Detect event triggers in a sentence.
    Handles:
    - Multi-word triggers (exact phrase match)
    - Single-word triggers (lemma-based match)
    """

    doc = nlp(sentence)
    sentence_lower = sentence.lower()

    detected = []

    # multi-word triggers first
    for event_type, trigger_list in EVENT_TRIGGERS.items():
        for trigger in trigger_list:
            if " " in trigger:  # multi-word trigger
                if trigger in sentence_lower:
                    detected.append((event_type, trigger))

   # single-word triggers using lemma
   
from triggers import EVENT_TRIGGERS

nlp = spacy.load("en_core_web_md")


def detect_triggers(sentence):
    doc = nlp(sentence)
    sentence_lower = sentence.lower()

    detected = []

    # 1️⃣ Multi-word triggers first
    for event_type, trigger_list in EVENT_TRIGGERS.items():
        for trigger in trigger_list:
            if " " in trigger:
                if trigger in sentence_lower:
                    detected.append((event_type, trigger))

    # 2️⃣ Single-word triggers
    for token in doc:
        word = token.text.lower()
        lemma = token.lemma_.lower()

        for event_type, trigger_list in EVENT_TRIGGERS.items():
            for trigger in trigger_list:
                if " " not in trigger:

                    # Special case for born
                    if trigger == "born":
                        if word == "born":
                            detected.append((event_type, token.text))

                    # Normal verbs use lemma
                    elif lemma == trigger:
                        detected.append((event_type, token.text))
            
    return detected





if __name__ == "__main__":
    test_sentences = [
        "He was born in 1937.",
        "He received the Padma Bhushan in 2000.",
        "He passed away in 2012.",
        "He passed the exam."
    ]

    for s in test_sentences:
        print(s)
        print(detect_triggers(s))
        print("-----")