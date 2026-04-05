import spacy
from collections import defaultdict
import re

nlp = spacy.load("en_core_web_md")

def normalize_name(name):
    titles = ["mr", "mrs", "ms", "dr", "prof", "sir", "shri", "smt"]

    name = name.lower()

    for title in titles:
        name = name.replace(title + ".", "")
        name = name.replace(title + " ", "")

    name = name.replace(".", "")
    name = re.sub(r"\s+", " ", name).strip()

    return name


def identify_main_person(text):

    doc = nlp(text)
    frequency = defaultdict(int)
    first_occurrence = {}
    original_form = {}

    # Collect PERSON entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            normalized = normalize_name(ent.text)

            frequency[normalized] += 1

            if normalized not in first_occurrence:
                first_occurrence[normalized] = ent.start
                original_form[normalized] = ent.text

    if not frequency:
        return None

    # Merge short names into long names
    names = list(frequency.keys())

    for short_name in names:
        short_tokens = short_name.split()

        for long_name in names:
            if short_name == long_name:
                continue

            long_tokens = long_name.split()

            if len(long_tokens) > len(short_tokens):
                if long_tokens[-len(short_tokens):] == short_tokens:

                    matches = [
                        other for other in names
                        if other != short_name
                        and len(other.split()) > len(short_tokens)
                        and other.split()[-len(short_tokens):] == short_tokens
                    ]

                    if len(matches) == 1:
                        frequency[long_name] += frequency[short_name]

                        frequency.pop(short_name, None)
                        first_occurrence.pop(short_name, None)
                        original_form.pop(short_name, None)

                    break

    main_person = max(
        frequency.keys(),
        key=lambda name: (frequency[name], -first_occurrence[name])
    )

    return original_form[main_person]




if __name__ == "__main__":
    name = identify_main_person("""
    Dr. A.P.J. Abdul Kalam was born in 1931 in Rameswaram.
    Kalam served as the President of India.
    He received the Bharat Ratna in 1997.
    """)

    print("Main Person:", name)