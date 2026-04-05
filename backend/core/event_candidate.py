import spacy
import re

nlp = spacy.load("en_core_web_md")

BOUNDARY_WORDS = {
    "and", "but", "then", "later",
    "after", "before", "when", "while"
}

BOUNDARY_PUNCT = {";", "."}



#  DATE EXTRACTION

def extract_dates(doc):
    main_date = None
    all_dates = []

    for ent in doc.ents:
        if ent.label_ == "DATE":
            all_dates.append(ent.text)
            if main_date is None:
                main_date = ent.text

    return main_date, all_dates



#  YEAR EXTRACTION (ROBUST)

def extract_year(date_text, sentence=None):

    #  Try from detected DATE
    if date_text:
        if isinstance(date_text, list):
            date_text = " ".join(date_text)

        match = re.search(r"\b(18|19|20)\d{2}\b", date_text)
        if match:
            return match.group()

    #  Fallback: extract from sentence
    if sentence:
        match = re.search(r"\b(18|19|20)\d{2}\b", sentence)
        if match:
            return match.group()

    return None


#  MAIN FUNCTION

def extract_event_candidates(sentence, triggers):

    doc = nlp(sentence)

    event_candidates = []

    main_date, all_dates = extract_dates(doc)
    year = extract_year(main_date, sentence)

    sentence_lower = sentence.lower()

    for event_type, trigger in triggers:

        trigger_lower = trigger.lower()

        
        #  MULTI-WORD TRIGGERS
       
        if " " in trigger_lower:

            if trigger_lower in sentence_lower:

                # ✅ ALWAYS use full sentence
                span = sentence.strip()

                # optional cleanup
                if span.lower().startswith("after"):
                    span = span.split(",", 1)[-1].strip()

                event_candidates.append({
                    "event_type": event_type,
                    "trigger": trigger_lower,
                    "span": span,
                    "sentence": sentence,
                    "date": main_date,
                    "year": year
                })

            continue

        
        #  SINGLE-WORD TRIGGERS
      
        for token in doc:

            if token.text.lower() == trigger_lower or token.lemma_.lower() == trigger_lower:

                # ALWAYS use full sentence (FIXED)
                span = sentence.strip()

                # optional cleanup
                if span.lower().startswith("after"):
                    span = span.split(",", 1)[-1].strip()

                event_candidates.append({
                    "event_type": event_type,
                    "trigger": trigger_lower,
                    "span": span,
                    "sentence": sentence,
                    "date": main_date,
                    "year": year
                })

                break

    return event_candidates