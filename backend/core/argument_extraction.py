import spacy

nlp = spacy.load("en_core_web_md")


def extract_arguments(event, main_person):

    sentence = event["sentence"]
    doc = nlp(sentence)

    
    # PERSON (FINAL FIX)
    
    # Always use main person for biography timeline
    person = [main_person]

   
    # ORGANIZATION (FILTERED)
    
    organization = []

    for ent in doc.ents:
        if ent.label_ == "ORG":

           
            if len(ent.text.split()) == 1:
                continue

            # remove if it's actually part of a PERSON name
            if any(ent.text in p for p in person):
                continue

            organization.append(ent.text)

    organization = list(set(organization))

   
    # DATE
   
    date = []

    for ent in doc.ents:
        if ent.label_ == "DATE":
            date.append(ent.text)

    date = list(set(date))

   
    #  LOCATION
    
    location = []

    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            location.append(ent.text)

    location = list(set(location))

   
    #  FINAL STRUCTURE
    
    result = {
        "event_type": event["event_type"],
        "trigger": event["trigger"],
        "span": event["span"],
        "sentence": sentence,
        "year": event.get("year"),
        "person": person
    }

    if organization:
        result["organization"] = organization

    if date:
        result["date"] = date

    if location:
        result["location"] = location

    return result