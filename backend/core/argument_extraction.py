import spacy

nlp = spacy.load("en_core_web_md")


def extract_arguments(event_candidate):

    span = event_candidate["span"]

    doc = nlp(span)

    date = None
    location = None
    organization = None

    for ent in doc.ents:

        if ent.label_ == "DATE":
            date = ent.text

        elif ent.label_ == "GPE":
            location = ent.text

        elif ent.label_ == "ORG":
            organization = ent.text

    return {
        "event_type": event_candidate["event_type"],
        "trigger": event_candidate["trigger"],
        "span": span,
        "date": date,
        "location": location,
        "organization": organization
    }
if __name__ == "__main__":

    events = [
        {
            "event_type": "Career",
            "trigger": "joined",
            "span": "He joined Tata Group in 1991"
        },
        {
            "event_type": "Career",
            "trigger": "became",
            "span": "became chairman in 2012"
        }
    ]

    for event in events:
        result = extract_arguments(event)
        print(result)